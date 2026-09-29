from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import polars as pl


SCHEMA_VERSION = 1
BINANCE_SPOT = "https://api.binance.com"
BINANCE_FUTURES = "https://fapi.binance.com"
OKX = "https://www.okx.com"

COMMON_SCHEMA = {
    "exchange": pl.String,
    "instrument_id": pl.String,
    "market_type": pl.String,
    "event_ts": pl.Int64,
    "receive_ts": pl.Int64,
    "available_ts": pl.Int64,
    "source": pl.String,
    "schema_version": pl.Int64,
    "quality_flag": pl.String,
    "raw_record_id": pl.String,
    "download_ts": pl.Int64,
    "source_time_unit": pl.String,
}
BAR_SCHEMA = {
    **COMMON_SCHEMA,
    "interval": pl.String,
    "open_ts": pl.Int64,
    "close_ts": pl.Int64,
    "open": pl.Decimal(38, 18),
    "high": pl.Decimal(38, 18),
    "low": pl.Decimal(38, 18),
    "close": pl.Decimal(38, 18),
    "base_volume": pl.Decimal(38, 18),
    "quote_volume": pl.Decimal(38, 18),
    "taker_buy_base_volume": pl.Decimal(38, 18),
    "taker_buy_quote_volume": pl.Decimal(38, 18),
    "is_closed": pl.Boolean,
}
FUNDING_SCHEMA = {
    **COMMON_SCHEMA,
    "settlement_ts": pl.Int64,
    "realized_rate": pl.Decimal(38, 18),
    "indicative_rate": pl.Decimal(38, 18),
    "mark_price_at_settlement": pl.Decimal(38, 18),
    "actual_interval_hours": pl.Decimal(38, 12),
    "first_seen_ts": pl.Int64,
    "available_ts_method": pl.String,
}
OI_SCHEMA = {
    **COMMON_SCHEMA,
    "interval": pl.String,
    "bucket_start_ts": pl.Int64,
    "bucket_end_ts": pl.Int64,
    "oi_contracts": pl.Decimal(38, 18),
    "oi_base_qty": pl.Decimal(38, 18),
    "oi_quote_notional": pl.Decimal(38, 18),
}
META_SCHEMA = {
    **COMMON_SCHEMA,
    "base_asset": pl.String,
    "quote_asset": pl.String,
    "settle_asset": pl.String,
    "contract_multiplier": pl.Decimal(38, 18),
    "multiplier_unit": pl.String,
    "tick_size": pl.Decimal(38, 18),
    "lot_size": pl.Decimal(38, 18),
    "min_notional": pl.Decimal(38, 18),
    "status": pl.String,
    "effective_from": pl.Int64,
    "effective_to": pl.Int64,
    "rule_observed_ts": pl.Int64,
}


class FetchError(RuntimeError):
    pass


def timestamp_ns(value: int | str, unit: str) -> int:
    multipliers = {"ms": 1_000_000, "us": 1_000, "ns": 1}
    if unit not in multipliers:
        raise ValueError(f"unsupported timestamp unit: {unit}")
    return int(value) * multipliers[unit]


def usable_at(row: dict[str, Any], decision_ts: int) -> bool:
    return row.get("available_ts") is not None and row["available_ts"] <= decision_ts


def book_sample_tradable(*, connected: bool, synchronized: bool) -> bool:
    return connected and synchronized


def _record_id(record: Any) -> str:
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def _quality(*flags: str) -> str:
    values = [flag for flag in flags if flag]
    return "|".join(values) if values else "ok"


def _common(
    exchange: str,
    instrument_id: str,
    market_type: str,
    event_ts: int,
    available_ts: int,
    source: str,
    raw: Any,
    downloaded_ts_ns: int | None,
    quality_flag: str = "ok",
    source_time_unit: str = "ms",
) -> dict[str, Any]:
    return {
        "exchange": exchange,
        "instrument_id": instrument_id,
        "market_type": market_type,
        "event_ts": event_ts,
        "receive_ts": None,
        "available_ts": available_ts,
        "source": source,
        "schema_version": SCHEMA_VERSION,
        "quality_flag": quality_flag,
        "raw_record_id": _record_id(raw),
        "download_ts": downloaded_ts_ns,
        "source_time_unit": source_time_unit,
    }


def normalize_okx_funding(
    pages: Iterable[Iterable[dict[str, Any]]],
    instrument_id: str,
    *,
    downloaded_ts_ns: int | None,
    source: str = f"{OKX}/api/v5/public/funding-rate-history",
) -> list[dict[str, Any]]:
    deduped: dict[int, dict[str, Any]] = {}
    for page in pages:
        for raw in page:
            settlement_ts = timestamp_ns(raw["fundingTime"], "ms")
            previous = deduped.get(settlement_ts)
            if previous is None or (
                not previous.get("realizedRate") and raw.get("realizedRate")
            ):
                deduped[settlement_ts] = raw

    rows: list[dict[str, Any]] = []
    previous_ts: int | None = None
    for settlement_ts, raw in sorted(deduped.items()):
        realized = raw.get("realizedRate")
        quality = _quality(
            "missing_realized_rate" if realized in (None, "") else "",
            "missing_mark_price_at_settlement",
            "download_time_unknown" if downloaded_ts_ns is None else "",
        )
        row = _common(
            "okx",
            instrument_id,
            "perpetual",
            settlement_ts,
            settlement_ts,
            source,
            raw,
            downloaded_ts_ns,
            quality,
        )
        row.update(
            settlement_ts=settlement_ts,
            realized_rate=Decimal(realized) if realized not in (None, "") else None,
            indicative_rate=(
                Decimal(raw["fundingRate"])
                if raw.get("fundingRate") not in (None, "")
                else None
            ),
            mark_price_at_settlement=None,
            actual_interval_hours=(
                Decimal(settlement_ts - previous_ts) / Decimal(3_600_000_000_000)
                if previous_ts is not None
                else None
            ),
            first_seen_ts=downloaded_ts_ns,
            available_ts_method="exchange settlement timestamp; no pre-settlement availability",
        )
        rows.append(row)
        previous_ts = settlement_ts
    return rows


def normalize_binance_funding(
    pages: Iterable[Iterable[dict[str, Any]]],
    instrument_id: str,
    *,
    downloaded_ts_ns: int,
    source: str = f"{BINANCE_FUTURES}/fapi/v1/fundingRate",
) -> list[dict[str, Any]]:
    deduped: dict[int, dict[str, Any]] = {}
    for page in pages:
        for raw in page:
            deduped[timestamp_ns(raw["fundingTime"], "ms")] = raw

    rows: list[dict[str, Any]] = []
    previous_ts: int | None = None
    for settlement_ts, raw in sorted(deduped.items()):
        rate = raw.get("fundingRate")
        mark = raw.get("markPrice")
        row = _common(
            "binance",
            instrument_id,
            "perpetual",
            settlement_ts,
            settlement_ts,
            source,
            raw,
            downloaded_ts_ns,
            _quality(
                "missing_realized_rate" if rate in (None, "") else "",
                "missing_mark_price_at_settlement" if mark in (None, "") else "",
            ),
        )
        row.update(
            settlement_ts=settlement_ts,
            realized_rate=Decimal(rate) if rate not in (None, "") else None,
            indicative_rate=None,
            mark_price_at_settlement=(
                Decimal(mark) if mark not in (None, "") else None
            ),
            actual_interval_hours=(
                Decimal(settlement_ts - previous_ts) / Decimal(3_600_000_000_000)
                if previous_ts is not None
                else None
            ),
            first_seen_ts=downloaded_ts_ns,
            available_ts_method="exchange settlement timestamp; no pre-settlement availability",
        )
        rows.append(row)
        previous_ts = settlement_ts
    return rows


def normalize_binance_open_interest(
    pages: Iterable[Iterable[dict[str, Any]]],
    instrument_id: str,
    *,
    interval: str,
    downloaded_ts_ns: int,
    source: str = f"{BINANCE_FUTURES}/futures/data/openInterestHist",
) -> list[dict[str, Any]]:
    if interval.lower() != "1h":
        raise ValueError("only 1h open-interest history is supported")
    bucket_ns = 3_600_000_000_000
    deduped = {
        timestamp_ns(raw["timestamp"], "ms"): raw
        for page in pages
        for raw in page
    }
    rows: list[dict[str, Any]] = []
    for bucket_end_ts, raw in sorted(deduped.items()):
        bucket_start_ts = bucket_end_ts - bucket_ns
        if bucket_end_ts > downloaded_ts_ns:
            continue
        base_qty = raw.get("sumOpenInterest")
        quote_notional = raw.get("sumOpenInterestValue")
        row = _common(
            "binance",
            instrument_id,
            "perpetual",
            bucket_end_ts,
            bucket_end_ts,
            source,
            raw,
            downloaded_ts_ns,
            _quality(
                "missing_oi_base_qty" if base_qty in (None, "") else "",
                "missing_oi_quote_notional" if quote_notional in (None, "") else "",
            ),
        )
        row.update(
            interval="1h",
            bucket_start_ts=bucket_start_ts,
            bucket_end_ts=bucket_end_ts,
            oi_contracts=None,
            oi_base_qty=Decimal(base_qty) if base_qty not in (None, "") else None,
            oi_quote_notional=(
                Decimal(quote_notional) if quote_notional not in (None, "") else None
            ),
        )
        rows.append(row)
    return rows


def normalize_okx_open_interest(
    pages: Iterable[Iterable[list[Any]]],
    instrument_id: str,
    *,
    interval: str,
    downloaded_ts_ns: int | None,
    source: str = f"{OKX}/api/v5/rubik/stat/contracts/open-interest-history",
) -> list[dict[str, Any]]:
    if interval.lower() != "1h":
        raise ValueError("only 1h open-interest history is supported")
    bucket_ns = 3_600_000_000_000
    deduped = {
        timestamp_ns(raw[0], "ms"): raw
        for page in pages
        for raw in page
    }
    rows: list[dict[str, Any]] = []
    for bucket_start_ts, raw in sorted(deduped.items()):
        bucket_end_ts = bucket_start_ts + bucket_ns
        if downloaded_ts_ns is not None and bucket_end_ts > downloaded_ts_ns:
            continue
        row = _common(
            "okx",
            instrument_id,
            "perpetual",
            bucket_start_ts,
            bucket_end_ts,
            source,
            raw,
            downloaded_ts_ns,
            _quality("download_time_unknown" if downloaded_ts_ns is None else ""),
        )
        row.update(
            interval="1h",
            bucket_start_ts=bucket_start_ts,
            bucket_end_ts=bucket_end_ts,
            oi_contracts=Decimal(raw[1]) if raw[1] not in (None, "") else None,
            oi_base_qty=Decimal(raw[2]) if raw[2] not in (None, "") else None,
            oi_quote_notional=Decimal(raw[3]) if raw[3] not in (None, "") else None,
        )
        rows.append(row)
    return rows


def normalize_binance_klines(
    records: Iterable[list[Any]],
    *,
    exchange: str,
    instrument_id: str,
    market_type: str,
    downloaded_ts_ns: int,
    source: str = "binance kline REST",
) -> list[dict[str, Any]]:
    rows = []
    for raw in records:
        open_ts = timestamp_ns(raw[0], "ms")
        close_ts = timestamp_ns(raw[6], "ms")
        available_ts = close_ts + 1_000_000
        if available_ts > downloaded_ts_ns:
            continue
        row = _common(
            exchange,
            instrument_id,
            market_type,
            close_ts,
            available_ts,
            source,
            raw,
            downloaded_ts_ns,
        )
        row.update(
            interval="1m",
            open_ts=open_ts,
            close_ts=close_ts,
            open=Decimal(raw[1]),
            high=Decimal(raw[2]),
            low=Decimal(raw[3]),
            close=Decimal(raw[4]),
            base_volume=Decimal(raw[5]) if raw[5] not in (None, "") else None,
            quote_volume=Decimal(raw[7]) if raw[7] not in (None, "") else None,
            taker_buy_base_volume=(
                Decimal(raw[9]) if raw[9] not in (None, "") else None
            ),
            taker_buy_quote_volume=(
                Decimal(raw[10]) if raw[10] not in (None, "") else None
            ),
            is_closed=True,
        )
        rows.append(row)
    return sorted({row["open_ts"]: row for row in rows}.values(), key=lambda x: x["open_ts"])


def normalize_okx_klines(
    records: Iterable[list[Any]],
    *,
    instrument_id: str,
    market_type: str,
    downloaded_ts_ns: int | None,
    source: str,
    mark_price: bool = False,
) -> list[dict[str, Any]]:
    rows = []
    for raw in records:
        if str(raw[-1]) != "1":
            continue
        open_ts = timestamp_ns(raw[0], "ms")
        available_ts = open_ts + 60_000_000_000
        close_ts = available_ts - 1
        row = _common(
            "okx",
            instrument_id,
            market_type,
            close_ts,
            available_ts,
            source,
            raw,
            downloaded_ts_ns,
            _quality("download_time_unknown" if downloaded_ts_ns is None else ""),
        )
        if mark_price:
            base_volume = quote_volume = None
        elif market_type == "spot":
            base_volume = Decimal(raw[5])
            quote_volume = Decimal(raw[7])
        else:
            base_volume = Decimal(raw[6])
            quote_volume = Decimal(raw[7])
        row.update(
            interval="1m",
            open_ts=open_ts,
            close_ts=close_ts,
            open=Decimal(raw[1]),
            high=Decimal(raw[2]),
            low=Decimal(raw[3]),
            close=Decimal(raw[4]),
            base_volume=base_volume,
            quote_volume=quote_volume,
            is_closed=True,
        )
        rows.append(row)
    return sorted({row["open_ts"]: row for row in rows}.values(), key=lambda x: x["open_ts"])


def _binance_meta(
    raw: dict[str, Any], market_type: str, downloaded_ts_ns: int
) -> dict[str, Any]:
    filters = {item["filterType"]: item for item in raw.get("filters", [])}
    price_filter = filters.get("PRICE_FILTER", {})
    lot_filter = filters.get("LOT_SIZE", {})
    notional_filter = filters.get("MIN_NOTIONAL", filters.get("NOTIONAL", {}))
    instrument_id = raw["symbol"] + ("-PERP" if market_type == "perpetual" else "")
    row = _common(
        "binance",
        instrument_id,
        market_type,
        downloaded_ts_ns,
        downloaded_ts_ns,
        (f"{BINANCE_FUTURES}/fapi/v1/exchangeInfo" if market_type == "perpetual" else f"{BINANCE_SPOT}/api/v3/exchangeInfo"),
        raw,
        downloaded_ts_ns,
        "current_rule_effective_start_unknown",
    )
    row.update(
        base_asset=raw.get("baseAsset"),
        quote_asset=raw.get("quoteAsset"),
        settle_asset=raw.get("marginAsset", raw.get("quoteAsset")),
        contract_multiplier=Decimal("1"),
        multiplier_unit=raw.get("baseAsset"),
        tick_size=Decimal(price_filter["tickSize"]) if price_filter.get("tickSize") else None,
        lot_size=Decimal(lot_filter["stepSize"]) if lot_filter.get("stepSize") else None,
        min_notional=(
            Decimal(notional_filter.get("notional", notional_filter.get("minNotional")))
            if notional_filter.get("notional", notional_filter.get("minNotional"))
            else None
        ),
        status=raw.get("status"),
        effective_from=None,
        effective_to=None,
        rule_observed_ts=downloaded_ts_ns,
    )
    return row


def _okx_meta(
    raw: dict[str, Any], market_type: str, downloaded_ts_ns: int | None
) -> dict[str, Any]:
    instrument_id = raw["instId"]
    observed = downloaded_ts_ns
    row = _common(
        "okx",
        instrument_id,
        market_type,
        observed or 0,
        observed or 0,
        f"{OKX}/api/v5/public/instruments",
        raw,
        observed,
        _quality(
            "current_rule_effective_start_unknown",
            "download_time_unknown" if observed is None else "",
        ),
    )
    row.update(
        base_asset=raw.get("baseCcy") or raw.get("ctValCcy"),
        quote_asset=raw.get("quoteCcy") or raw.get("settleCcy"),
        settle_asset=raw.get("settleCcy") or raw.get("quoteCcy"),
        contract_multiplier=(Decimal(raw["ctVal"]) if raw.get("ctVal") else Decimal("1")),
        multiplier_unit=raw.get("ctValCcy") or raw.get("baseCcy"),
        tick_size=Decimal(raw["tickSz"]) if raw.get("tickSz") else None,
        lot_size=Decimal(raw["lotSz"]) if raw.get("lotSz") else None,
        min_notional=None,
        status=raw.get("state"),
        effective_from=None,
        effective_to=None,
        rule_observed_ts=observed,
    )
    return row


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("time must include Z or a UTC offset")
    return parsed.astimezone(timezone.utc)


def _append_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(value, ensure_ascii=False, default=str, separators=(",", ":")) + "\n")


def _request_json(url: str, params: dict[str, Any], raw_path: Path) -> tuple[Any, int]:
    clean = {key: value for key, value in params.items() if value is not None}
    full_url = f"{url}?{urlencode(clean)}" if clean else url
    if url.startswith(OKX):
        curl = shutil.which("curl.exe") or shutil.which("curl")
        if curl is None:
            raise FetchError("curl is required for bounded OKX HTTP requests")
        try:
            result = subprocess.run(
                [curl, "--silent", "--show-error", "--max-time", "8", "--write-out", "\n%{http_code}", full_url],
                capture_output=True,
                text=True,
                timeout=12,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            downloaded_ts_ns = time.time_ns()
            _append_json(raw_path, {"downloaded_ts": downloaded_ts_ns, "url": full_url, "error": "request process timeout"})
            raise FetchError(f"request process timeout: {url}") from error
        downloaded_ts_ns = time.time_ns()
        body_text, _, status_text = result.stdout.rpartition("\n")
        status = int(status_text) if status_text.isdigit() else 0
        try:
            body = json.loads(body_text) if body_text else ""
        except json.JSONDecodeError:
            body = body_text
        envelope = {
            "downloaded_ts": downloaded_ts_ns,
            "url": full_url,
            "http_status": status or None,
            "body": body,
            "error": result.stderr.strip() or None,
        }
        _append_json(raw_path, envelope)
        if result.returncode or status >= 400:
            detail = f"HTTP {status}" if status else result.stderr.strip() or f"curl exit {result.returncode}"
            raise FetchError(f"{detail}: {url}")
        return body, downloaded_ts_ns
    downloaded_ts_ns = time.time_ns()
    request = Request(full_url, headers={"User-Agent": "usdt-quant-data/0.1"})
    try:
        with urlopen(request, timeout=8) as response:
            text = response.read().decode("utf-8")
            body = json.loads(text)
            status = response.status
            downloaded_ts_ns = time.time_ns()
    except HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(text)
        except json.JSONDecodeError:
            body = text
        _append_json(raw_path, {
            "downloaded_ts": downloaded_ts_ns,
            "url": full_url,
            "http_status": error.code,
            "body": body,
        })
        raise FetchError(f"HTTP {error.code}: {url}") from error
    except (URLError, TimeoutError, OSError) as error:
        reason = getattr(error, "reason", error)
        _append_json(raw_path, {
            "downloaded_ts": downloaded_ts_ns,
            "url": full_url,
            "error": str(reason),
        })
        raise FetchError(f"network error: {url}: {reason}") from error
    _append_json(raw_path, {
        "downloaded_ts": downloaded_ts_ns,
        "url": full_url,
        "http_status": status,
        "body": body,
    })
    return body, downloaded_ts_ns


def _write_parquet(path: Path, rows: list[dict[str, Any]]) -> Path | None:
    if not rows:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    if "close_ts" in rows[0]:
        schema = BAR_SCHEMA
    elif "settlement_ts" in rows[0]:
        schema = FUNDING_SCHEMA
    elif "oi_base_qty" in rows[0]:
        schema = OI_SCHEMA
    else:
        schema = META_SCHEMA
    pl.DataFrame(rows, schema=schema, strict=False).write_parquet(path)
    return path


def _coverage(
    dataset: str,
    rows: list[dict[str, Any]],
    raw_path: Path,
    parquet_path: Path | None,
    *,
    status: str = "ok",
    error: str | None = None,
    expected_minutes: int | None = None,
) -> dict[str, Any]:
    times = [row["event_ts"] for row in rows if row.get("event_ts") is not None]
    qualities: dict[str, int] = {}
    for row in rows:
        qualities[row["quality_flag"]] = qualities.get(row["quality_flag"], 0) + 1
    sources = sorted({row["source"] for row in rows if row.get("source")})
    if not sources and raw_path.exists():
        try:
            envelope = json.loads(raw_path.read_text(encoding="utf-8").splitlines()[0])
            sources = [envelope["url"].split("?", 1)[0]] if envelope.get("url") else []
        except (json.JSONDecodeError, IndexError):
            pass
    result = {
        "dataset": dataset,
        "status": status,
        "sources": sources,
        "rows": len(rows),
        "actual_start_ts": min(times) if times else None,
        "actual_end_ts": max(times) if times else None,
        "raw_path": raw_path.as_posix(),
        "parquet_path": parquet_path.as_posix() if parquet_path else None,
        "source_time_unit": "ms",
        "normalized_time_unit": "ns",
        "quality": qualities,
        "error": error,
    }
    if expected_minutes is not None:
        result["expected_closed_minutes"] = expected_minutes
        result["missing_closed_minutes"] = max(expected_minutes - len(rows), 0)
    return result


def _open_interest_window(
    rows: list[dict[str, Any]],
    *,
    requested_start_ts: int,
    requested_end_ts: int,
    provider_start_ts: int | None,
    provider_end_ts: int | None,
) -> dict[str, Any]:
    collected_start_ts = min((row["bucket_start_ts"] for row in rows), default=None)
    collected_end_ts = max((row["bucket_end_ts"] for row in rows), default=None)
    if not rows:
        status = "unavailable"
    elif (
        collected_start_ts > requested_start_ts
        or collected_end_ts < requested_end_ts
        or (provider_start_ts is not None and provider_start_ts > requested_start_ts)
        or (provider_end_ts is not None and provider_end_ts < requested_end_ts)
    ):
        status = "partial"
    else:
        status = "ok"
    return {
        "status": status,
        "requested_start_ts": requested_start_ts,
        "requested_end_ts": requested_end_ts,
        "provider_start_ts": provider_start_ts,
        "provider_end_ts": provider_end_ts,
        "collected_window_start_ts": collected_start_ts,
        "collected_window_end_ts": collected_end_ts,
    }


def _binance_pages(
    url: str,
    raw_path: Path,
    params: dict[str, Any],
    start_ms: int,
    end_ms: int,
    *,
    time_field: str | int,
    step_ms: int,
    limit: int = 1000,
) -> tuple[list[list[Any]], int]:
    pages: list[list[Any]] = []
    cursor = start_ms
    last_download = time.time_ns()
    while cursor < end_ms:
        query = {**params, "startTime": cursor, "endTime": end_ms - 1, "limit": limit}
        body, last_download = _request_json(url, query, raw_path)
        if not body:
            break
        pages.append(body)
        value = body[-1][time_field] if isinstance(time_field, str) else body[-1][time_field]
        next_cursor = int(value) + step_ms
        if next_cursor <= cursor:
            raise FetchError(f"pagination did not advance: {url}")
        cursor = next_cursor
        if len(body) < limit:
            break
    return pages, last_download


def _binance_open_interest_pages(
    raw_path: Path,
    symbol: str,
    start_ms: int,
    end_ms: int,
    *,
    limit: int = 500,
) -> tuple[list[list[Any]], int]:
    url = f"{BINANCE_FUTURES}/futures/data/openInterestHist"
    pages: list[list[Any]] = []
    seen: set[int] = set()
    cursor = end_ms - 1
    last_download = time.time_ns()
    while cursor >= start_ms:
        body, last_download = _request_json(
            url,
            {
                "symbol": symbol,
                "period": "1h",
                "startTime": start_ms,
                "endTime": cursor,
                "limit": limit,
            },
            raw_path,
        )
        if not body:
            break
        page = [row for row in body if int(row["timestamp"]) not in seen]
        for row in page:
            seen.add(int(row["timestamp"]))
        if page:
            pages.append(page)
        oldest = min(int(row["timestamp"]) for row in body)
        next_cursor = oldest - 1
        if next_cursor >= cursor:
            raise FetchError(f"pagination did not retreat: {url}")
        cursor = next_cursor
        if oldest <= start_ms or len(body) < limit:
            break
    return pages, last_download


def _okx_pages(
    url: str,
    raw_path: Path,
    params: dict[str, Any],
    start_ms: int,
    end_ms: int,
    *,
    time_field: str | int,
) -> tuple[list[list[Any]], int]:
    pages: list[list[Any]] = []
    cursor = end_ms
    last_download = time.time_ns()
    while cursor > start_ms:
        body, last_download = _request_json(
            url, {**params, "after": cursor, "limit": 100}, raw_path
        )
        if body.get("code") != "0":
            raise FetchError(f"OKX returned code {body.get('code')}: {body.get('msg')}")
        data = body.get("data", [])
        if not data:
            break
        pages.append(data)
        value = data[-1][time_field] if isinstance(time_field, str) else data[-1][time_field]
        next_cursor = int(value)
        if next_cursor >= cursor:
            raise FetchError(f"pagination did not retreat: {url}")
        cursor = next_cursor
        if cursor <= start_ms or len(data) < 100:
            break
    return pages, last_download


def _okx_open_interest_pages(
    raw_path: Path,
    instrument_id: str,
    start_ms: int,
    end_ms: int,
) -> tuple[list[list[Any]], int]:
    url = f"{OKX}/api/v5/rubik/stat/contracts/open-interest-history"
    pages: list[list[Any]] = []
    cursor = end_ms
    last_download = time.time_ns()
    while cursor > start_ms:
        body, last_download = _request_json(
            url,
            {"instId": instrument_id, "period": "1H", "end": cursor, "limit": 100},
            raw_path,
        )
        if body.get("code") != "0":
            raise FetchError(f"OKX returned code {body.get('code')}: {body.get('msg')}")
        data = body.get("data", [])
        if not data:
            break
        pages.append(data)
        next_cursor = int(data[-1][0])
        if next_cursor >= cursor:
            raise FetchError(f"pagination did not retreat: {url}")
        cursor = next_cursor
        if cursor <= start_ms or len(data) < 100:
            break
    return pages, last_download


def collect_history(
    exchange: str,
    base: str,
    start: datetime,
    end: datetime,
    out: Path,
) -> Path:
    if start >= end:
        raise ValueError("start must be earlier than end")
    base = base.upper()
    if base not in {"BTC", "ETH"}:
        raise ValueError("base must be BTC or ETH")
    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)
    requested_minutes = (end_ms - start_ms) // 60_000
    data_version = f"{exchange}_{base}_{start:%Y%m%dT%H%M%SZ}_{end:%Y%m%dT%H%M%SZ}_{int(time.time())}"
    raw_dir = out / "raw" / exchange / base / data_version
    normalized_dir = out / "normalized" / exchange / base / data_version
    report_items: list[dict[str, Any]] = []

    if exchange == "binance":
        symbol = f"{base}USDT"
        jobs = [
            ("spot_bars", f"{BINANCE_SPOT}/api/v3/klines", {"symbol": symbol, "interval": "1m"}, 0, 60_000, "spot", symbol),
            ("perp_bars", f"{BINANCE_FUTURES}/fapi/v1/klines", {"symbol": symbol, "interval": "1m"}, 0, 60_000, "perpetual", f"{symbol}-PERP"),
            ("mark_bars", f"{BINANCE_FUTURES}/fapi/v1/markPriceKlines", {"symbol": symbol, "interval": "1m"}, 0, 60_000, "mark", f"{symbol}-PERP"),
        ]
        for name, url, params, time_field, step, market_type, instrument_id in jobs:
            raw_path = raw_dir / f"{name}.jsonl"
            try:
                pages, downloaded = _binance_pages(url, raw_path, params, start_ms, end_ms, time_field=time_field, step_ms=step)
                records = [record for page in pages for record in page if start_ms <= int(record[0]) < end_ms]
                rows = normalize_binance_klines(
                    records,
                    exchange="binance",
                    instrument_id=instrument_id,
                    market_type=market_type,
                    downloaded_ts_ns=downloaded,
                    source=url,
                )
                parquet = _write_parquet(normalized_dir / f"{name}.parquet", rows)
                report_items.append(_coverage(name, rows, raw_path, parquet, expected_minutes=requested_minutes))
            except FetchError as error:
                report_items.append(_coverage(name, [], raw_path, None, status="blocked", error=str(error), expected_minutes=requested_minutes))

        funding_name = "funding_settlement"
        raw_path = raw_dir / f"{funding_name}.jsonl"
        try:
            pages, downloaded = _binance_pages(
                f"{BINANCE_FUTURES}/fapi/v1/fundingRate",
                raw_path,
                {"symbol": symbol},
                start_ms,
                end_ms,
                time_field="fundingTime",
                step_ms=1,
            )
            rows = normalize_binance_funding(pages, f"{symbol}-PERP", downloaded_ts_ns=downloaded)
            rows = [row for row in rows if timestamp_ns(start_ms, "ms") <= row["settlement_ts"] < timestamp_ns(end_ms, "ms")]
            parquet = _write_parquet(normalized_dir / f"{funding_name}.parquet", rows)
            report_items.append(_coverage(funding_name, rows, raw_path, parquet))
        except FetchError as error:
            report_items.append(_coverage(funding_name, [], raw_path, None, status="blocked", error=str(error)))

        oi_name = "open_interest"
        raw_path = raw_dir / f"{oi_name}.jsonl"
        now_ms = int(time.time() * 1000)
        api_start_ms = now_ms - 30 * 24 * 3_600_000
        oi_start_ms = max(start_ms, api_start_ms)
        oi_end_ms = min(end_ms, now_ms)
        rows: list[dict[str, Any]] = []
        if oi_start_ms >= oi_end_ms:
            reason = "Binance open-interest history is limited to the latest 30 days; requested window does not intersect"
            _append_json(raw_path, {"downloaded_ts": time.time_ns(), "url": f"{BINANCE_FUTURES}/futures/data/openInterestHist", "error": reason})
            item = _coverage(oi_name, [], raw_path, None, status="unavailable", error=reason)
        else:
            try:
                pages, downloaded = _binance_open_interest_pages(
                    raw_path,
                    symbol,
                    oi_start_ms,
                    oi_end_ms,
                )
                rows = normalize_binance_open_interest(
                    pages,
                    f"{symbol}-PERP",
                    interval="1h",
                    downloaded_ts_ns=downloaded,
                )
                rows = [
                    row
                    for row in rows
                    if timestamp_ns(oi_start_ms, "ms") <= row["event_ts"] < timestamp_ns(oi_end_ms, "ms")
                ]
                parquet = _write_parquet(normalized_dir / f"{oi_name}.parquet", rows)
                item = _coverage(
                    oi_name,
                    rows,
                    raw_path,
                    parquet,
                )
            except FetchError as error:
                item = _coverage(oi_name, [], raw_path, None, status="blocked", error=str(error))
        window = _open_interest_window(
            rows,
            requested_start_ts=timestamp_ns(start_ms, "ms"),
            requested_end_ts=timestamp_ns(end_ms, "ms"),
            provider_start_ts=timestamp_ns(api_start_ms, "ms"),
            provider_end_ts=timestamp_ns(now_ms, "ms"),
        )
        if item["status"] == "blocked":
            window["status"] = "blocked"
        item.update(window)
        report_items.append(item)

        cross_name = "cross_funding_settlement"
        raw_path = raw_dir / f"{cross_name}.jsonl"
        try:
            pages, downloaded = _okx_pages(
                f"{OKX}/api/v5/public/funding-rate-history",
                raw_path,
                {"instId": f"{base}-USDT-SWAP"},
                start_ms,
                end_ms,
                time_field="fundingTime",
            )
            rows = normalize_okx_funding(
                pages,
                f"{base}-USDT-SWAP",
                downloaded_ts_ns=downloaded,
            )
            rows = [row for row in rows if timestamp_ns(start_ms, "ms") <= row["settlement_ts"] < timestamp_ns(end_ms, "ms")]
            parquet = _write_parquet(normalized_dir / f"{cross_name}.parquet", rows)
            report_items.append(_coverage(cross_name, rows, raw_path, parquet))
        except FetchError as error:
            report_items.append(_coverage(cross_name, [], raw_path, None, status="blocked", error=str(error)))

        for name, url, market_type in [
            ("spot_instrument_meta", f"{BINANCE_SPOT}/api/v3/exchangeInfo", "spot"),
            ("perp_instrument_meta", f"{BINANCE_FUTURES}/fapi/v1/exchangeInfo", "perpetual"),
        ]:
            raw_path = raw_dir / f"{name}.jsonl"
            try:
                body, downloaded = _request_json(url, {"symbol": symbol}, raw_path)
                selected = [item for item in body.get("symbols", []) if item.get("symbol") == symbol]
                rows = [_binance_meta(item, market_type, downloaded) for item in selected]
                parquet = _write_parquet(normalized_dir / f"{name}.parquet", rows)
                report_items.append(_coverage(name, rows, raw_path, parquet))
            except FetchError as error:
                report_items.append(_coverage(name, [], raw_path, None, status="blocked", error=str(error)))

    elif exchange == "okx":
        spot = f"{base}-USDT"
        swap = f"{base}-USDT-SWAP"
        okx_blocked: str | None = None
        try:
            _request_json(
                f"{OKX}/api/v5/public/instruments",
                {"instType": "SPOT", "instId": spot},
                raw_dir / "host_probe.jsonl",
            )
        except FetchError as error:
            okx_blocked = f"OKX host probe failed; remaining endpoints not attempted: {error}"
        jobs = [
            ("spot_bars", f"{OKX}/api/v5/market/history-candles", {"instId": spot, "bar": "1m"}, 0, "spot", spot, False),
            ("perp_bars", f"{OKX}/api/v5/market/history-candles", {"instId": swap, "bar": "1m"}, 0, "perpetual", swap, False),
            ("mark_bars", f"{OKX}/api/v5/market/history-mark-price-candles", {"instId": swap, "bar": "1m"}, 0, "mark", swap, True),
        ]
        for name, url, params, time_field, market_type, instrument_id, mark_price in jobs:
            raw_path = raw_dir / f"{name}.jsonl"
            try:
                if okx_blocked:
                    _append_json(raw_path, {"downloaded_ts": time.time_ns(), "url": url, "error": okx_blocked})
                    raise FetchError(okx_blocked)
                pages, downloaded = _okx_pages(url, raw_path, params, start_ms, end_ms, time_field=time_field)
                records = [record for page in pages for record in page if start_ms <= int(record[0]) < end_ms]
                rows = normalize_okx_klines(records, instrument_id=instrument_id, market_type=market_type, downloaded_ts_ns=downloaded, source=url, mark_price=mark_price)
                parquet = _write_parquet(normalized_dir / f"{name}.parquet", rows)
                report_items.append(_coverage(name, rows, raw_path, parquet, expected_minutes=requested_minutes))
            except FetchError as error:
                report_items.append(_coverage(name, [], raw_path, None, status="blocked", error=str(error), expected_minutes=requested_minutes))

        raw_path = raw_dir / "funding_settlement.jsonl"
        try:
            if okx_blocked:
                funding_url = f"{OKX}/api/v5/public/funding-rate-history"
                _append_json(raw_path, {"downloaded_ts": time.time_ns(), "url": funding_url, "error": okx_blocked})
                raise FetchError(okx_blocked)
            pages, downloaded = _okx_pages(
                f"{OKX}/api/v5/public/funding-rate-history",
                raw_path,
                {"instId": swap},
                start_ms,
                end_ms,
                time_field="fundingTime",
            )
            rows = normalize_okx_funding(pages, swap, downloaded_ts_ns=downloaded)
            rows = [row for row in rows if timestamp_ns(start_ms, "ms") <= row["settlement_ts"] < timestamp_ns(end_ms, "ms")]
            parquet = _write_parquet(normalized_dir / "funding_settlement.parquet", rows)
            report_items.append(_coverage("funding_settlement", rows, raw_path, parquet))
        except FetchError as error:
            report_items.append(_coverage("funding_settlement", [], raw_path, None, status="blocked", error=str(error)))

        oi_name = "open_interest"
        raw_path = raw_dir / f"{oi_name}.jsonl"
        rows: list[dict[str, Any]] = []
        provider_rows: list[dict[str, Any]] = []
        try:
            if okx_blocked:
                oi_url = f"{OKX}/api/v5/rubik/stat/contracts/open-interest-history"
                _append_json(raw_path, {"downloaded_ts": time.time_ns(), "url": oi_url, "error": okx_blocked})
                raise FetchError(okx_blocked)
            pages, downloaded = _okx_open_interest_pages(raw_path, swap, start_ms, end_ms)
            provider_rows = normalize_okx_open_interest(
                pages,
                swap,
                interval="1H",
                downloaded_ts_ns=downloaded,
            )
            rows = [row for row in provider_rows if timestamp_ns(start_ms, "ms") <= row["event_ts"] < timestamp_ns(end_ms, "ms")]
            parquet = _write_parquet(normalized_dir / f"{oi_name}.parquet", rows)
            item = _coverage(oi_name, rows, raw_path, parquet)
        except FetchError as error:
            item = _coverage(oi_name, [], raw_path, None, status="blocked", error=str(error))
        window = _open_interest_window(
            rows,
            requested_start_ts=timestamp_ns(start_ms, "ms"),
            requested_end_ts=timestamp_ns(end_ms, "ms"),
            provider_start_ts=min((row["bucket_start_ts"] for row in provider_rows), default=None),
            provider_end_ts=max((row["bucket_end_ts"] for row in provider_rows), default=None),
        )
        if item["status"] == "blocked":
            window["status"] = "blocked"
        item.update(window)
        report_items.append(item)

        cross_name = "cross_funding_settlement"
        raw_path = raw_dir / f"{cross_name}.jsonl"
        try:
            pages, downloaded = _binance_pages(
                f"{BINANCE_FUTURES}/fapi/v1/fundingRate",
                raw_path,
                {"symbol": f"{base}USDT"},
                start_ms,
                end_ms,
                time_field="fundingTime",
                step_ms=1,
            )
            rows = normalize_binance_funding(
                pages,
                f"{base}USDT-PERP",
                downloaded_ts_ns=downloaded,
            )
            rows = [row for row in rows if timestamp_ns(start_ms, "ms") <= row["settlement_ts"] < timestamp_ns(end_ms, "ms")]
            parquet = _write_parquet(normalized_dir / f"{cross_name}.parquet", rows)
            report_items.append(_coverage(cross_name, rows, raw_path, parquet))
        except FetchError as error:
            report_items.append(_coverage(cross_name, [], raw_path, None, status="blocked", error=str(error)))

        for name, inst_type, instrument_id, market_type in [
            ("spot_instrument_meta", "SPOT", spot, "spot"),
            ("perp_instrument_meta", "SWAP", swap, "perpetual"),
        ]:
            raw_path = raw_dir / f"{name}.jsonl"
            try:
                if okx_blocked:
                    meta_url = f"{OKX}/api/v5/public/instruments"
                    _append_json(raw_path, {"downloaded_ts": time.time_ns(), "url": meta_url, "error": okx_blocked})
                    raise FetchError(okx_blocked)
                body, downloaded = _request_json(f"{OKX}/api/v5/public/instruments", {"instType": inst_type, "instId": instrument_id}, raw_path)
                if body.get("code") != "0":
                    raise FetchError(f"OKX returned code {body.get('code')}: {body.get('msg')}")
                rows = [_okx_meta(item, market_type, downloaded) for item in body.get("data", [])]
                parquet = _write_parquet(normalized_dir / f"{name}.parquet", rows)
                report_items.append(_coverage(name, rows, raw_path, parquet))
            except FetchError as error:
                report_items.append(_coverage(name, [], raw_path, None, status="blocked", error=str(error)))
    else:
        raise ValueError("exchange must be binance or okx")

    report = {
        "data_version": data_version,
        "exchange": exchange,
        "base": base,
        "requested_start": start.isoformat(),
        "requested_end_exclusive": end.isoformat(),
        "generated_ts": time.time_ns(),
        "raw_time_unit": "milliseconds",
        "normalized_time_unit": "nanoseconds",
        "historical_receive_ts": None,
        "rule_effective_time": "current rules observed at download; original effective start unavailable",
        "datasets": report_items,
        "known_unavailable": {
            "historical_funding_quotes": "strict pre-settlement funding prediction history is unavailable",
            "historical_orderbook": "not synthesized",
        },
    }
    report_path = out / "coverage" / f"{data_version}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


def _read_okx_raw(path: Path) -> tuple[list[list[Any]], int | None]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return [], None
    try:
        values = [json.loads(text)]
    except json.JSONDecodeError:
        values = [json.loads(line) for line in text.splitlines()]
    pages: list[list[Any]] = []
    downloaded: list[int] = []
    for value in values:
        if "downloaded_ts" in value:
            downloaded.append(int(value["downloaded_ts"]))
        body = value.get("body", value)
        data = body.get("data", body) if isinstance(body, dict) else body
        if isinstance(data, list):
            pages.append(data)
    return pages, max(downloaded) if downloaded else None


def import_okx(kind: str, base: str, raw: Path, out: Path) -> Path:
    pages, downloaded = _read_okx_raw(raw)
    base = base.upper()
    records = [record for page in pages for record in page]
    spot = f"{base}-USDT"
    swap = f"{base}-USDT-SWAP"
    if kind == "funding":
        rows = normalize_okx_funding(pages, swap, downloaded_ts_ns=downloaded)
    elif kind in {"spot-bars", "perp-bars", "mark-bars"}:
        instrument_id = spot if kind == "spot-bars" else swap
        market_type = {"spot-bars": "spot", "perp-bars": "perpetual", "mark-bars": "mark"}[kind]
        rows = normalize_okx_klines(records, instrument_id=instrument_id, market_type=market_type, downloaded_ts_ns=downloaded, source=str(raw), mark_price=kind == "mark-bars")
    elif kind in {"spot-meta", "perp-meta"}:
        market_type = "spot" if kind == "spot-meta" else "perpetual"
        rows = [_okx_meta(record, market_type, downloaded) for record in records]
    else:
        raise ValueError(f"unsupported OKX import kind: {kind}")
    output = out / f"okx_{base}_{kind.replace('-', '_')}.parquet"
    written = _write_parquet(output, rows)
    if written is None:
        raise ValueError("raw file contained no importable records")
    return written


def run_forward(exchange: str, base: str, duration: float, out: Path) -> Path:
    if duration <= 0:
        raise ValueError("duration must be positive")
    from nautilus_trader.adapters.binance import (
        BinanceDataClientConfig,
        BinanceDataClientFactory,
        BinanceEnvironment,
        BinanceInstrumentProviderConfig,
        BinanceProductType,
        BinanceSpotMarketDataMode,
    )
    from nautilus_trader.adapters.okx import (
        OKXDataClientConfig,
        OKXDataClientFactory,
        OKXEnvironment,
        OKXInstrumentType,
        OKXRegion,
    )
    from nautilus_trader.common import DataActor, Environment, LoggerConfig
    from nautilus_trader.live import LiveNode, LiveNodeConfig
    from nautilus_trader.model import BookType, ClientId, InstrumentId, TraderId

    base = base.upper()
    run_id = f"{exchange}_{base}_{int(time.time())}"
    event_path = out / "forward" / run_id / "events.jsonl"
    oi_raw_path = out / "forward" / run_id / "open_interest_raw.jsonl"
    report_path = out / "forward" / run_id / "coverage.json"
    counts: dict[str, int] = {}

    if exchange == "binance":
        spot_client = ClientId("BINANCE_SPOT")
        perp_client = ClientId("BINANCE_USD_M")
        subscriptions = [
            (InstrumentId.from_str(f"{base}USDT.BINANCE"), spot_client, False),
            (InstrumentId.from_str(f"{base}USDT-PERP.BINANCE"), perp_client, True),
        ]
        configs = {
            str(spot_client): BinanceDataClientConfig(
                product_type=BinanceProductType.SPOT,
                environment=BinanceEnvironment.LIVE,
                spot_market_data_mode=BinanceSpotMarketDataMode.Json,
                instrument_provider=BinanceInstrumentProviderConfig(
                    load_all=False,
                    load_ids=[f"{base}USDT.BINANCE"],
                    log_warnings=False,
                ),
            ),
            str(perp_client): BinanceDataClientConfig(
                product_type=BinanceProductType.USD_M,
                environment=BinanceEnvironment.LIVE,
                instrument_provider=BinanceInstrumentProviderConfig(
                    load_all=False,
                    load_ids=[f"{base}USDT-PERP.BINANCE"],
                    log_warnings=False,
                ),
            ),
        }
        factories = {str(spot_client): BinanceDataClientFactory(), str(perp_client): BinanceDataClientFactory()}
    elif exchange == "okx":
        client = ClientId("OKX_PUBLIC")
        subscriptions = [
            (InstrumentId.from_str(f"{base}-USDT.OKX"), client, False),
            (InstrumentId.from_str(f"{base}-USDT-SWAP.OKX"), client, True),
        ]
        configs = {
            str(client): OKXDataClientConfig(
                instrument_types=[OKXInstrumentType.SPOT, OKXInstrumentType.SWAP],
                environment=OKXEnvironment.LIVE,
                region=OKXRegion.GLOBAL,
            )
        }
        factories = {str(client): OKXDataClientFactory()}
    else:
        raise ValueError("exchange must be binance or okx")

    class Recorder(DataActor):
        def _save(self, kind: str, event: Any, quality_flag: str = "ok") -> None:
            counts[kind] = counts.get(kind, 0) + 1
            payload = event.to_dict() if hasattr(event, "to_dict") else str(event)
            _append_json(event_path, {
                "type": kind,
                "receive_ts": time.time_ns(),
                "event_ts": getattr(event, "ts_event", None),
                "source_init_ts": getattr(event, "ts_init", None),
                "quality_flag": quality_flag,
                "payload": payload,
            })

        def on_start(self) -> None:
            for instrument_id, client_id, derivative in subscriptions:
                self.subscribe_socket_state(client_id=client_id)
                self.subscribe_quotes(instrument_id, client_id=client_id)
                self.subscribe_trades(instrument_id, client_id=client_id)
                self.subscribe_book_deltas(instrument_id, BookType.L2_MBP, depth=20, client_id=client_id, managed=True)
                if derivative:
                    self.subscribe_mark_prices(instrument_id, client_id=client_id)
                    self.subscribe_index_prices(instrument_id, client_id=client_id)
                    self.subscribe_funding_rates(instrument_id, client_id=client_id)

        def on_quote(self, event: Any) -> None:
            self._save("quote", event)

        def on_trade(self, event: Any) -> None:
            self._save("trade", event)

        def on_book_deltas(self, event: Any) -> None:
            self._save("book_deltas", event, "native_managed_book")

        def on_mark_price(self, event: Any) -> None:
            self._save("mark_price", event)

        def on_index_price(self, event: Any) -> None:
            self._save("index_price", event)

        def on_funding_rate(self, event: Any) -> None:
            self._save("funding_rate", event)

        def on_socket_state(self, event: Any) -> None:
            self._save("socket_state", event, "gap_or_recovery_state")

    started = time.time_ns()
    status = "completed"
    error = None
    node = None
    try:
        node = LiveNode.build(
            "forward-data",
            LiveNodeConfig(
                environment=Environment.LIVE,
                trader_id=TraderId("DATA-001"),
                logging=LoggerConfig(bypass_logging=True),
                data_clients=configs,
            ),
            data_factories=factories,
        )
        node.add_actor(Recorder())
        handle = node.handle()

        async def poll_open_interest(stop: asyncio.Event) -> None:
            while not stop.is_set():
                try:
                    if exchange == "binance":
                        url = f"{BINANCE_FUTURES}/fapi/v1/openInterest"
                        body, received = await asyncio.to_thread(
                            _request_json, url, {"symbol": f"{base}USDT"}, oi_raw_path
                        )
                        record = {
                            "type": "open_interest",
                            "exchange": exchange,
                            "instrument_id": f"{base}USDT-PERP.BINANCE",
                            "event_ts": timestamp_ns(body["time"], "ms"),
                            "receive_ts": received,
                            "available_ts": received,
                            "oi_base_qty": body["openInterest"],
                            "oi_contract_qty": body["openInterest"],
                            "oi_quote_notional": None,
                            "source": url,
                            "quality_flag": "ok",
                        }
                    else:
                        url = f"{OKX}/api/v5/public/open-interest"
                        body, received = await asyncio.to_thread(
                            _request_json,
                            url,
                            {"instType": "SWAP", "instId": f"{base}-USDT-SWAP"},
                            oi_raw_path,
                        )
                        raw = body["data"][0]
                        record = {
                            "type": "open_interest",
                            "exchange": exchange,
                            "instrument_id": f"{base}-USDT-SWAP.OKX",
                            "event_ts": timestamp_ns(raw["ts"], "ms"),
                            "receive_ts": received,
                            "available_ts": received,
                            "oi_base_qty": raw.get("oiCcy"),
                            "oi_contract_qty": raw.get("oi"),
                            "oi_quote_notional": None,
                            "source": url,
                            "quality_flag": _quality("missing_oi_base_qty" if not raw.get("oiCcy") else ""),
                        }
                    counts["open_interest"] = counts.get("open_interest", 0) + 1
                    _append_json(event_path, record)
                except (FetchError, KeyError, IndexError) as exc:
                    counts["open_interest_gap"] = counts.get("open_interest_gap", 0) + 1
                    _append_json(event_path, {
                        "type": "open_interest_gap",
                        "receive_ts": time.time_ns(),
                        "quality_flag": "unavailable",
                        "error": str(exc),
                    })
                try:
                    await asyncio.wait_for(stop.wait(), timeout=60)
                except TimeoutError:
                    pass

        async def collect_for_duration() -> None:
            stop = asyncio.Event()
            task = asyncio.create_task(node.run_async())
            oi_task = asyncio.create_task(poll_open_interest(stop))
            await asyncio.sleep(duration)
            stop.set()
            handle.stop()
            await task
            await oi_task

        asyncio.run(collect_for_duration())
    except Exception as exc:
        status = "blocked"
        error = f"{type(exc).__name__}: {exc}"
    finally:
        if node is not None:
            node.dispose()

    if status == "completed" and not any(
        counts.get(kind, 0)
        for kind in ("quote", "trade", "book_deltas", "mark_price", "index_price", "funding_rate")
    ):
        status = "completed_with_gaps"
        error = "no native market events received during the bounded run"

    expected_streams = ["quote", "trade", "book_deltas", "mark_price", "index_price", "funding_rate"]
    report = {
        "exchange": exchange,
        "base": base,
        "status": status,
        "error": error,
        "started_ts": started,
        "ended_ts": time.time_ns(),
        "requested_duration_seconds": duration,
        "events_path": event_path.as_posix(),
        "open_interest_raw_path": oi_raw_path.as_posix(),
        "counts": counts,
        "missing_streams": [kind for kind in expected_streams if not counts.get(kind)],
        "orderbook_maintenance": "NautilusTrader managed=True; socket state retained for gaps and recovery",
        "orderbook_sample_tradable": False if not counts.get("book_deltas") else None,
        "open_interest_collection": "public REST snapshot immediately and approximately every 60 seconds",
        "known_unavailable": {
            "usdt_external_quote": "no external fiat/stablecoin source configured",
            "liquidations": "not exposed by the selected standard DataActor subscriptions",
            "platform_rule_changes": "historical effective time unavailable; daily REST snapshots required",
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="USDT research data collection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    history = subparsers.add_parser("history")
    history.add_argument("--exchange", choices=["binance", "okx"], required=True)
    history.add_argument("--base", choices=["BTC", "ETH"], required=True)
    history.add_argument("--start", required=True, help="inclusive ISO-8601 time")
    history.add_argument("--end", required=True, help="exclusive ISO-8601 time")
    history.add_argument("--out", type=Path, default=Path("data"))

    offline = subparsers.add_parser("import-okx")
    offline.add_argument("--kind", choices=["funding", "spot-bars", "perp-bars", "mark-bars", "spot-meta", "perp-meta"], required=True)
    offline.add_argument("--base", choices=["BTC", "ETH"], required=True)
    offline.add_argument("--raw", type=Path, required=True)
    offline.add_argument("--out", type=Path, default=Path("data/imported"))

    forward = subparsers.add_parser("forward")
    forward.add_argument("--exchange", choices=["binance", "okx"], required=True)
    forward.add_argument("--base", choices=["BTC", "ETH"], required=True)
    forward.add_argument("--duration", type=float, required=True, help="seconds before clean stop")
    forward.add_argument("--out", type=Path, default=Path("data"))

    args = parser.parse_args(argv)
    if args.command == "history":
        path = collect_history(args.exchange, args.base, _parse_utc(args.start), _parse_utc(args.end), args.out)
    elif args.command == "import-okx":
        path = import_okx(args.kind, args.base, args.raw, args.out)
    else:
        path = run_forward(args.exchange, args.base, args.duration, args.out)
    print(path)


if __name__ == "__main__":
    main()

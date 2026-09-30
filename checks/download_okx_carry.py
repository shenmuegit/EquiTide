"""Download OKX BTC-USDT-SWAP history for the fixed cross-venue carry test."""

import csv
import hashlib
import io
import json
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/raw/okx/BTC/cross_exchange_carry_20260930"
OUT = ROOT / "data/normalized/okx/BTC/cross_exchange_carry_20260930"
HOST = "https://www.okx.com/api/v5/public/"
START, END = 1765843200000, 1789516800000  # 2025-12-16 to 2026-09-16 UTC
MINUTE = 60_000


def utc_ms(value):
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)


def get(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"}),
                         timeout=60) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def history(module, aggregation, begin, end):
    query = urlencode({"module": module, "instType": "SWAP", "instFamilyList": "BTC-USDT",
                       "dateAggrType": aggregation, "begin": begin, "end": end})
    body = json.loads(get(HOST + "market-data-history?" + query))
    if body["code"] != "0":
        raise RuntimeError(body)
    return [item for group in body["data"] for detail in group["details"]
            for item in detail["groupDetails"]]


def archive_files(module):
    # OKX archive boundaries are UTC+8; stay below its 10-month / 10-day limits.
    month_edges = [utc_ms(s) for s in ("2025-11-30T16:00:00Z", "2026-02-28T16:00:00Z",
                                   "2026-05-31T16:00:00Z", "2026-08-31T16:00:00Z")]
    entries = {}
    for begin, end in zip(month_edges, month_edges[1:]):
        for item in history(module, "monthly", begin, end):
            entries[item["filename"]] = item
    if module == 2:
        day_edges = [utc_ms(s) for s in ("2026-08-31T16:00:00Z", "2026-09-08T16:00:00Z",
                                       "2026-09-16T16:00:00Z")]
        for begin, end in zip(day_edges, day_edges[1:]):
            for item in history(module, "daily", begin, end):
                entries[item["filename"] + "_" + item["dateTs"]] = item
    return list(entries.values())


def load_archives(module):
    records, sources = {}, []
    for item in archive_files(module):
        name = item["filename"]
        path = BASE / (str(item["dateTs"]) + "_" + name)
        if not path.exists():
            path.write_bytes(get(item["url"]))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None or len(archive.namelist()) != 1:
                raise ValueError(f"bad archive: {path}")
            rows = csv.DictReader(io.TextIOWrapper(archive.open(archive.namelist()[0]), encoding="utf-8"))
            key = "open_time" if module == 2 else "funding_time"
            for row in rows:
                ts = int(row[key])
                if START <= ts < END:
                    if ts in records and records[ts] != row:
                        raise ValueError(f"conflicting {key} {ts}")
                    records[ts] = row
        sources.append({"url": item["url"].split("?", 1)[0], "path": str(path),
                        "sha256": digest})
    return records, sources


def recent_funding():
    records, pages, cursor = {}, [], END
    while cursor >= utc_ms("2026-08-31T16:00:00Z"):
        query = urlencode({"instId": "BTC-USDT-SWAP", "after": cursor, "limit": 100})
        body = json.loads(get(HOST + "funding-rate-history?" + query))
        if body["code"] != "0":
            raise RuntimeError(body)
        page = body["data"]
        if not page:
            break
        pages.append({"query": query, "data": page})
        for row in page:
            ts = int(row["fundingTime"])
            if START <= ts < END:
                records[ts] = {"instrument_name": row["instId"],
                               "funding_rate": row["realizedRate"], "funding_time": row["fundingTime"]}
        next_cursor = int(page[-1]["fundingTime"])
        if next_cursor >= cursor:
            raise ValueError("funding pagination did not retreat")
        cursor = next_cursor
        if len(page) < 100:
            break
    raw = BASE / "recent_funding.json"
    raw.write_text(json.dumps(pages, indent=2) + "\n", encoding="utf-8")
    return records, {"url": HOST + "funding-rate-history", "path": str(raw),
                     "sha256": hashlib.sha256(raw.read_bytes()).hexdigest()}


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    bars, bar_sources = load_archives(2)
    funding, funding_sources = load_archives(3)
    latest, latest_source = recent_funding()
    for ts, row in latest.items():
        if ts in funding and funding[ts] != row:
            raise ValueError(f"conflicting funding {ts}")
        funding[ts] = row
    expected = list(range(START, END, MINUTE))
    missing = sorted(set(expected) - bars.keys())
    if missing:
        raise ValueError(f"missing {len(missing)} minutes; first={missing[0]}")
    if any(row["instrument_name"] != "BTC-USDT-SWAP" or row["confirm"] != "1"
           for row in bars.values()):
        raise ValueError("unexpected instrument or unclosed bars")
    if not funding or min(funding) > START + 8 * 3600_000 or max(funding) < END - 8 * 3600_000:
        raise ValueError("funding does not cover requested range")
    times = sorted(funding)
    gaps = [(a, b) for a, b in zip(times, times[1:]) if b - a > 8 * 3600_000]
    if gaps:
        raise ValueError(f"funding gaps: {gaps[:3]}")
    bar_path, funding_path = OUT / "perp_bars.parquet", OUT / "funding_settlement.parquet"
    pl.DataFrame([{"open_ts": ts, "open": float(bars[ts]["open"]),
                   "close": float(bars[ts]["close"])} for ts in expected]).write_parquet(bar_path)
    pl.DataFrame([{"settlement_ts": ts, "realized_rate": float(funding[ts]["funding_rate"])}
                  for ts in times]).write_parquet(funding_path)
    manifest = {"version": "cross_exchange_carry_20260930", "start_utc": datetime.fromtimestamp(START/1000, timezone.utc).isoformat(),
                "end_exclusive_utc": datetime.fromtimestamp(END/1000, timezone.utc).isoformat(),
                "bar_rows": len(bars), "funding_rows": len(funding), "missing_bar_minutes": len(missing),
                "bars_sha256": hashlib.sha256(bar_path.read_bytes()).hexdigest(),
                "funding_sha256": hashlib.sha256(funding_path.read_bytes()).hexdigest(),
                "sources": {"bars": bar_sources, "funding": funding_sources + [latest_source]}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("bar_rows", "funding_rows", "missing_bar_minutes")}, indent=2))


if __name__ == "__main__":
    # A missing minute must fail closed rather than fill from a later bar.
    assert len(set(range(0, 180_000, MINUTE)) - {0, 60_000}) == 1
    main()

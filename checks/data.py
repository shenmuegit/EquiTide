from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import time
from unittest.mock import patch

import polars as pl

from usdt_quant.data import (
    _binance_open_interest_pages,
    _open_interest_window,
    _request_json,
    book_sample_tradable,
    import_okx,
    normalize_binance_klines,
    normalize_binance_open_interest,
    normalize_okx_funding,
    normalize_okx_open_interest,
    timestamp_ns,
    usable_at,
)


def main() -> None:
    hour_ms = 3_600_000
    t0 = 1_700_000_000_000
    t1 = t0 + 8 * hour_ms
    t2 = t1 + 8 * hour_ms
    rows = normalize_okx_funding(
        [
            [
                {"fundingTime": str(t2), "fundingRate": "0.0003"},
                {
                    "fundingTime": str(t1),
                    "fundingRate": "0.0001",
                    "realizedRate": "-0.0002",
                },
            ],
            [
                {
                    "fundingTime": str(t1),
                    "fundingRate": "0.0001",
                    "realizedRate": "-0.0002",
                },
                {
                    "fundingTime": str(t0),
                    "fundingRate": "0.0004",
                    "realizedRate": "0.0005",
                },
            ],
        ],
        "BTC-USDT-SWAP",
        downloaded_ts_ns=timestamp_ns(t2 + hour_ms, "ms"),
    )
    assert len(rows) == 3
    assert rows[1]["realized_rate"] == Decimal("-0.0002")
    assert rows[1]["indicative_rate"] == Decimal("0.0001")
    assert rows[2]["realized_rate"] is None  # Never fall back to fundingRate.
    assert rows[0]["actual_interval_hours"] is None
    assert rows[1]["actual_interval_hours"] == Decimal("8")
    assert rows[2]["actual_interval_hours"] == Decimal("8")

    assert timestamp_ns(1_700_000_000_123, "ms") == 1_700_000_000_123_000_000
    assert timestamp_ns(1_700_000_000_123_456, "us") == 1_700_000_000_123_456_000
    assert not usable_at({"available_ts": 200}, 199)
    assert usable_at({"available_ts": 200}, 200)

    bars = normalize_binance_klines(
        [
            [t0, "1", "2", "0.5", "1.5", "10", t0 + 59_999, "15", 3, "4", "6", "0"],
            [t0 + 60_000, "1.5", "2", "1", "1.8", "8", t0 + 119_999, "13", 2, "3", "5", "0"],
        ],
        exchange="binance",
        instrument_id="BTCUSDT",
        market_type="spot",
        downloaded_ts_ns=timestamp_ns(t0 + 90_000, "ms"),
    )
    assert len(bars) == 1
    assert bars[0]["is_closed"] is True
    assert bars[0]["available_ts"] == timestamp_ns(t0 + 60_000, "ms")
    assert bars[0]["taker_buy_base_volume"] == Decimal("4")
    assert bars[0]["taker_buy_quote_volume"] == Decimal("6")

    binance_oi = normalize_binance_open_interest(
        [
            [
                {
                    "symbol": "BTCUSDT",
                    "sumOpenInterest": "100.5",
                    "sumOpenInterestValue": "5000000.25",
                    "timestamp": t0 + hour_ms,
                },
                {
                    "symbol": "BTCUSDT",
                    "sumOpenInterest": "999",
                    "sumOpenInterestValue": "999",
                    "timestamp": t0 + 3 * hour_ms,
                },
            ]
        ],
        "BTCUSDT-PERP",
        interval="1h",
        downloaded_ts_ns=timestamp_ns(t0 + 2 * hour_ms, "ms"),
    )
    assert len(binance_oi) == 1, "unfinished OI bucket leaked into history"
    assert binance_oi[0]["interval"] == "1h"
    assert binance_oi[0]["oi_base_qty"] == Decimal("100.5")
    assert binance_oi[0]["oi_quote_notional"] == Decimal("5000000.25")
    assert binance_oi[0]["available_ts"] == timestamp_ns(t0 + hour_ms, "ms")
    assert binance_oi[0]["bucket_start_ts"] == timestamp_ns(t0, "ms")
    assert binance_oi[0]["bucket_end_ts"] == timestamp_ns(t0 + hour_ms, "ms")
    assert binance_oi[0]["event_ts"] == timestamp_ns(t0 + hour_ms, "ms")
    assert not usable_at(binance_oi[0], timestamp_ns(t0 + hour_ms, "ms") - 1)
    assert usable_at(binance_oi[0], timestamp_ns(t0 + hour_ms, "ms"))

    okx_oi = normalize_okx_open_interest(
        [
            [[str(t1), "200", "20.25", "1010000"]],
            [
                [str(t0), "100", "10.5", "500000"],
                [str(t1), "200", "20.25", "1010000"],
            ],
        ],
        "BTC-USDT-SWAP",
        interval="1H",
        downloaded_ts_ns=timestamp_ns(t2, "ms"),
    )
    assert [row["event_ts"] for row in okx_oi] == [
        timestamp_ns(t0, "ms"),
        timestamp_ns(t1, "ms"),
    ]
    assert okx_oi[1]["oi_contracts"] == Decimal("200")
    assert okx_oi[1]["oi_base_qty"] == Decimal("20.25")
    assert okx_oi[1]["oi_quote_notional"] == Decimal("1010000")

    with TemporaryDirectory() as directory:
        newest = [
            {"timestamp": t0 + 2 * hour_ms},
            {"timestamp": t0 + 3 * hour_ms},
        ]
        oldest = [
            {"timestamp": t0},
            {"timestamp": t0 + hour_ms},
        ]
        with patch(
            "usdt_quant.data._request_json",
            side_effect=[(newest, 10), (oldest, 20)],
        ) as request:
            pages, downloaded = _binance_open_interest_pages(
                Path(directory) / "oi.jsonl",
                "BTCUSDT",
                t0,
                t0 + 4 * hour_ms,
                limit=2,
            )
        timestamps = [row["timestamp"] for page in pages for row in page]
        assert sorted(timestamps) == [t0 + offset * hour_ms for offset in range(4)]
        assert len(timestamps) == len(set(timestamps))
        assert downloaded == 20
        assert request.call_args_list[0].args[1]["endTime"] == t0 + 4 * hour_ms - 1
        assert request.call_args_list[1].args[1]["endTime"] == t0 + 2 * hour_ms - 1

    partial_window = _open_interest_window(
        [
            {
                "bucket_start_ts": timestamp_ns(t0 + hour_ms, "ms"),
                "bucket_end_ts": timestamp_ns(t2, "ms"),
            }
        ],
        requested_start_ts=timestamp_ns(t0, "ms"),
        requested_end_ts=timestamp_ns(t2, "ms"),
        provider_start_ts=timestamp_ns(t0 + hour_ms, "ms"),
        provider_end_ts=timestamp_ns(t2, "ms"),
    )
    assert partial_window["status"] == "partial"
    assert partial_window["requested_start_ts"] == timestamp_ns(t0, "ms")
    assert partial_window["provider_start_ts"] == timestamp_ns(t0 + hour_ms, "ms")
    assert partial_window["collected_window_start_ts"] == timestamp_ns(t0 + hour_ms, "ms")
    assert not book_sample_tradable(connected=True, synchronized=False)
    assert not book_sample_tradable(connected=False, synchronized=True)
    assert book_sample_tradable(connected=True, synchronized=True)
    with TemporaryDirectory() as directory:
        raw = Path(directory) / "funding.json"
        raw.write_text(json.dumps({"data": [{"fundingTime": str(t1),
                        "fundingRate": "0.0001", "realizedRate": "-0.0002"}]}))
        imported = pl.read_parquet(import_okx("funding", "ETH", raw, Path(directory)))
        assert "realized_rate" in imported.columns, "offline import lost funding columns"
        assert imported["realized_rate"][0] == Decimal("-0.0002")
        assert imported["indicative_rate"][0] == Decimal("0.0001")

        read_finished = []
        class Response:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                time.sleep(0.01)
                read_finished.append(time.time_ns())
                return b'{}'
        with patch("usdt_quant.data.urlopen", return_value=Response()):
            _, received = _request_json("https://example.invalid", {}, Path(directory) / "request.jsonl")
        assert received >= read_finished[0], "response marked available before it was read"
    print("data checks passed")


if __name__ == "__main__":
    main()

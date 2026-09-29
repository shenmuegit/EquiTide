from pathlib import Path

import pandas as pd

from freqtrade.data.history.datahandlers.parquetdatahandler import ParquetDataHandler
from freqtrade.enums import CandleType


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "data/normalized/binance/BTC/20260718T000000Z_20260916T000000Z_1789548557/spot_bars.parquet"
)
OUTPUT = Path(__file__).resolve().parents[1] / "data/binance"

raw = pd.read_parquet(
    SOURCE,
    columns=[
        "open_ts", "open", "high", "low", "close", "base_volume", "is_closed", "quality_flag"
    ],
).sort_values("open_ts")
assert len(raw) == 86_400
assert raw["is_closed"].all() and raw["quality_flag"].eq("ok").all()
assert raw["open_ts"].is_unique
assert raw["open_ts"].diff().dropna().eq(60_000_000_000).all()

raw["date"] = pd.to_datetime(raw["open_ts"], unit="ns", utc=True)
raw = raw.rename(columns={"base_volume": "volume"})
for column in ("open", "high", "low", "close", "volume"):
    raw[column] = raw[column].astype(float)
assert (raw["high"] >= raw[["open", "close", "low"]].max(axis=1)).all()
assert (raw["low"] <= raw[["open", "close", "high"]].min(axis=1)).all()
assert (raw["volume"] >= 0).all()

bars = raw.set_index("date").resample("15min").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
)
assert len(bars) == 5_760 and len(raw) == len(bars) * 15
assert bars.notna().all().all()
bars = bars.reset_index()
ParquetDataHandler(OUTPUT).ohlcv_store("BTC/USDT", "15m", bars, CandleType.SPOT)
print(f"Stored {len(bars)} BTC/USDT 15m candles: {bars.date.iloc[0]} to {bars.date.iloc[-1]}")

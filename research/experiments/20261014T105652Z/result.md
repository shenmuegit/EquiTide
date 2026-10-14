# BTC/ETH 固定星期 UTC 交易窗口研究结果

- 轮次：`20261014T105652Z`。星期、持有期、时间范围、成本和淘汰标准在计算前冻结于 `plan.json`；SHA256 `a9c89c51b97dc2894d4a78782c6f91f95add9460f99d00f238331663707085a3`。
- 本轮为 Binance 归档现货历史回测，不是本轮实时报价模拟、真实订单或实盘收益。已反复使用的 2025–2026 历史不是未触碰的最终留出集。
- 初始16项历史证据此前已逐项审计，缺少实际回测结果的配置为0；本轮未重算这些旧策略。

## 候选规则与动机

部分既有研究报告过 BTC/加密货币星期效应，本轮据此做独立的可交易性反证测试，不复现论文结论：[The day of the week effect in the cryptocurrency market](https://www.sciencedirect.com/science/article/pii/S1544612318304240)；[Bitcoin time-of-day, day-of-week and month-of-year effects](https://www.sciencedirect.com/science/article/pii/S1544612319301710)。这些旧样本只作动机，不能证明本策略有效。

BTC 与 ETH 分别建立独立 2,000 USDT 现货账户。每个配置每个 UTC 周在预先指定的星期一至星期日之一，于 00:00 确定性时间信号可得后，按 00:01 的下一分钟开盘买入；持有24或72小时，于对应日 00:01 的一分钟开盘卖出。每周最多一笔、窗口互不重叠；卖单被交易所过滤器代理拒绝时，下分钟重试至 OOS 终点；买单若被拒则跳过当周。只做多、不加杠杆、不借币、不跨币转账、不计现金利息。所有周几和持有期都预注册，未用 OOS 选定“最佳星期”。


## 数据与时序

- 数据：Binance BTCUSDT、ETHUSDT 现货连续一分钟 OHLCV，聚合检查 UTC 时间戳、已闭合状态、连续性、正价格、成交量非负及每日 1,440 根分钟K线。输入范围 `2024-09-16` 至 `2026-09-16`；OOS `2025-09-19 00:01` 至 `2026-09-14 00:01 UTC`。输入文件 SHA256 见 `data_manifest.json`。
- Walk-forward：360日分成12个连续、不重叠的30日评估窗，账户跨窗连续持仓和结算；没有模型训练、信号拟合或折间重置。首折前包含365日暖机和3日隔离。每配置仅约51–52笔往返交易，统计把握有限。
- 成交价是回测历史下一分钟开盘引用，不是当前市场报价，也不代表 Binance 实际接单或成交保证。百分比价格限制以成交前5分钟VWAP作代理；没有历史盘口、历史费率层级或历史交易所过滤器，按本轮公开 `exchangeInfo` 当前过滤器快照近似。

## 成本与敏感性

- 每侧手续费10bp、估算半价差1bp、滑点2bp，加 `0.5 × 前20个完整UTC日日收益样本标准差 × sqrt(订单金额 / 前20日quote ADV)` 冲击；最大参与率0.1%。按 Binance PRICE_FILTER 向不利方向tick取整、LOT_SIZE向下取量，并检查NOTIONAL与PERCENT_PRICE_BY_SIDE。所有成本假设同倍数生成1×/2×/3×场景；审计中容量/余额拒绝数均为0。
- 二维敏感性网格为资产 × 星期7类 × 持有期{1,3}，共28组、84个成本场景。局部邻域固定为同币种、循环星期距离≤1、两个持有期共6格；报告全量局部邻域3×正收益比例及热图。没用最优网格角点代替稳健性。

## 结论

- 28组全部 `rejected`，通过0。1×、2×、3×净收益为正的配置数分别 `8`、`1`、`0`。3×局部邻域为正的全局比例为 `0.0%`；均未通过所有成本场景为正及≥60%局部邻域门槛。
- 1×最高配置 `weekday_window_ETH_dow5_hold3d`：1×/2×/3×收益 `29.018% / 12.737% / -1.469%`，1×正收益折 `8/12`，3×分钟收盘与成交后采样回撤 `39.42%`，3×局部邻域正收益比例 `0.0%`。它在更高成本下转负，且回撤/邻域门槛失败，故不保留。
- 同期买入持有基准只读复用 `20261014T084051Z/report.json`，BTC 1×/3×为 `-34.57% / -34.90%`，ETH为 `-46.18% / -46.47%`。基准只作市场参照，不改变候选失败判定。
- 本轮没有保留盈利候选。没有计算 DSR/PBO，也没有把重复使用的 OOS 称为最终测试集；仓库已有大量策略试验，星期选择存在多重比较风险。


## 全部预注册配置

|配置|币种|UTC星期|持有天数|1×净收益|2×|3×|1×正折/12|1×/3×采样回撤|1×往返|3×邻域正比例|判定|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
|weekday_window_ETH_dow5_hold3d|ETH|Saturday|3|+29.02%|+12.74%|-1.47%|8/12|33.4% / 39.4%|51|0%|rejected|
|weekday_window_ETH_dow0_hold1d|ETH|Monday|1|+13.49%|-0.82%|-13.31%|8/12|20.1% / 26.2%|51|0%|rejected|
|weekday_window_BTC_dow5_hold3d|BTC|Saturday|3|+7.11%|-6.31%|-18.03%|7/12|25.7% / 32.4%|51|0%|rejected|
|weekday_window_ETH_dow2_hold1d|ETH|Wednesday|1|+2.36%|-10.55%|-21.81%|4/12|24.6% / 36.5%|51|0%|rejected|
|weekday_window_BTC_dow0_hold1d|BTC|Monday|1|+1.41%|-11.29%|-22.39%|6/12|15.0% / 23.5%|51|0%|rejected|
|weekday_window_ETH_dow0_hold3d|ETH|Monday|3|+0.22%|-12.40%|-23.42%|5/12|37.7% / 44.0%|51|0%|rejected|
|weekday_window_ETH_dow6_hold3d|ETH|Sunday|3|+0.19%|-12.44%|-23.46%|7/12|33.3% / 39.4%|51|0%|rejected|
|weekday_window_ETH_dow6_hold1d|ETH|Sunday|1|+0.05%|-12.80%|-23.98%|5/12|30.6% / 40.4%|52|0%|rejected|
|weekday_window_BTC_dow6_hold1d|BTC|Sunday|1|-4.44%|-16.62%|-27.24%|5/12|18.9% / 32.8%|52|0%|rejected|
|weekday_window_BTC_dow2_hold1d|BTC|Wednesday|1|-8.71%|-20.14%|-30.13%|5/12|20.9% / 37.2%|51|0%|rejected|
|weekday_window_BTC_dow6_hold3d|BTC|Sunday|3|-10.60%|-21.79%|-31.57%|8/12|25.9% / 35.8%|51|0%|rejected|
|weekday_window_ETH_dow4_hold3d|ETH|Friday|3|-12.58%|-23.79%|-33.55%|5/12|42.1% / 50.6%|52|0%|rejected|
|weekday_window_BTC_dow4_hold3d|BTC|Friday|3|-14.25%|-25.17%|-34.70%|4/12|28.4% / 39.6%|52|0%|rejected|
|weekday_window_ETH_dow5_hold1d|ETH|Saturday|1|-15.06%|-25.96%|-35.45%|5/12|20.4% / 36.2%|52|0%|rejected|
|weekday_window_BTC_dow0_hold3d|BTC|Monday|3|-15.29%|-25.89%|-35.16%|6/12|32.1% / 41.5%|51|0%|rejected|
|weekday_window_BTC_dow5_hold1d|BTC|Saturday|1|-16.32%|-26.98%|-36.28%|4/12|18.8% / 36.3%|52|0%|rejected|
|weekday_window_BTC_dow4_hold1d|BTC|Friday|1|-18.38%|-28.78%|-37.84%|5/12|22.6% / 38.4%|52|0%|rejected|
|weekday_window_ETH_dow4_hold1d|ETH|Friday|1|-21.89%|-31.90%|-40.62%|6/12|30.1% / 43.3%|52|0%|rejected|
|weekday_window_BTC_dow1_hold1d|BTC|Tuesday|1|-29.98%|-38.73%|-46.39%|4/12|32.3% / 46.8%|51|0%|rejected|
|weekday_window_ETH_dow1_hold1d|ETH|Tuesday|1|-34.15%|-42.43%|-49.67%|4/12|37.6% / 50.4%|51|0%|rejected|
|weekday_window_BTC_dow3_hold1d|BTC|Thursday|1|-39.68%|-47.22%|-53.82%|2/12|45.9% / 57.2%|51|0%|rejected|
|weekday_window_BTC_dow2_hold3d|BTC|Wednesday|3|-40.34%|-47.79%|-54.31%|3/12|54.4% / 63.5%|51|0%|rejected|
|weekday_window_BTC_dow3_hold3d|BTC|Thursday|3|-45.20%|-52.04%|-58.03%|3/12|53.5% / 61.8%|51|0%|rejected|
|weekday_window_BTC_dow1_hold3d|BTC|Tuesday|3|-49.61%|-55.91%|-61.42%|4/12|59.9% / 67.3%|51|0%|rejected|
|weekday_window_ETH_dow2_hold3d|ETH|Wednesday|3|-55.79%|-61.34%|-66.19%|4/12|71.3% / 76.4%|51|0%|rejected|
|weekday_window_ETH_dow3_hold1d|ETH|Thursday|1|-59.01%|-64.16%|-68.66%|1/12|62.0% / 70.4%|51|0%|rejected|
|weekday_window_ETH_dow3_hold3d|ETH|Thursday|3|-63.31%|-67.91%|-71.94%|3/12|69.2% / 74.8%|51|0%|rejected|
|weekday_window_ETH_dow1_hold3d|ETH|Tuesday|3|-63.81%|-68.35%|-72.32%|4/12|73.8% / 78.7%|51|0%|rejected|


## 实施尝试记录

首次运行时成本辅助函数模块路径错误，首个配置尚未产出回测或交易文件即退出。修正为导入已审计的滞后成本函数后，完整重跑全部84个成本场景；这个短暂代码错误不是一个策略结果，失败原因和修复记在 `evaluation_attempts.jsonl` 与 `setup_failure.log`。

## 复现与审计

- 环境复现命令：`.venv/bin/python research/experiments/20261014T105652Z/reproduce.py`。
- 28个fingerprint均先成功 reserve，完整计算后逐项 finish。审计独立重放28×3成本结果、逐折收益、成交账本与连续净值哈希；详情见 `audit.log`。
- `report.json` 保存逐格净收益、逐折收益/回撤/Sharpe/Calmar、交易成本分项和净值哈希；`fold_results.csv`、`cost_scenarios.csv`、`daily_equity.csv.gz`、`trades.csv.gz` 及 `weekday_daily_returns.csv` 提供明细。
- 回撤是分钟收盘净值与成交后参考价采样，不含分钟内高低点或逐笔路径。

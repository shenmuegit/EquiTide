# USDT 市场中性量化技术栈选型

确认日期：2026-09-16  
依据：[策略、数据采集与因子挖掘研究](../../../usdt_quant_strategy_factor_research.md)

## 1. 已确认范围

首版覆盖数据采集、因子研究、回测和自动实盘交易，通过 FastAPI 提交任务和查询结果。

交易范围沿用研究文档：Binance、OKX，BTC、ETH，各平台独立建立现货多头与等基础币数量的 USDT 本位线性永续空头组合。

当前已实现历史数据导入、因子与模型研究、共享策略回测，以及按建仓时间提交历史分析的 API。数据版本、固定研究切分、资金和成本参数由程序选择，完整依据随结果保存。业务记录存入 PostgreSQL，批量数据与结果保存在文件中。`web/` 单页已接入真实 API，位于 `http://127.0.0.1:5178`；用户只选择历史买入日期和小时（北京时间），页面分别展示 M1 当时判断和 B0 随后 24 小时基于历史数据的模拟回放，支持真实分析记录、深浅模式和手机布局。两腿执行、自动交易和实盘管理尚未通过验收；原生能力缺口见第 4.3 节，具体进度统一维护在[项目构建计划](../plans/2026-09-16-usdt-project-build.md)。

## 2. 已确认技术选择

| 部分 | 选择 | 用途 |
| --- | --- | --- |
| 开发语言与依赖 | Python 3.12、uv | 研究、策略和后端开发，管理依赖与运行环境 |
| 因子计算 | Polars、NumPy | 时间对齐、滚动窗口和批量因子计算 |
| 模型 | scikit-learn | 岭回归、Logistic 回归及模型评估 |
| 历史数据 | Parquet | 保存行情、因子和回测明细 |
| 业务数据库 | PostgreSQL | 实验登记、策略配置、任务与运行记录 |
| 回测与实盘 | NautilusTrader 2.x | 使用 2.x 开展研发；正式发布并完成验证后接实盘，实盘具体版本届时确定 |
| 后端接口 | FastAPI | 按建仓时间提交分析、查询任务与结果，后续管理策略运行 |
| 前端 | React、TypeScript、Vite | 历史买入时间输入、判断与回放、真实分析记录 |
| 部署 | Linux、Docker Compose | 部署网页、API、计算程序和交易程序 |

完整构建顺序、文件职责和逐项验收统一见[项目构建计划](../plans/2026-09-16-usdt-project-build.md)，双腿现金流核对是其中的任务 1。

## 3. 最小实现约束

- 因子公式、数据可用时间、标签、资金费、基差、费用和总投入资金收益率遵循研究文档。
- 项目实现所需因子和双腿策略逻辑；回测与实盘优先复用交易框架原生的订单、持仓和账户处理。
- FastAPI 接收操作并返回结果。研究回测与实盘分别在独立进程运行，耗时回测不能占用实盘事件循环。
- Parquet 保存批量分析数据，PostgreSQL 保存业务记录。交易框架的原生持久化方式随引擎版本适配结果确定。
- 研发使用 NautilusTrader 2.x。实盘等待 2.x 正式发布并通过本项目验收；当前候选发布版仅用于研发和验证。

## 4. 交易引擎的已核查事实

2026-09-16 通过 GitHub 发布 API 与 PyPI 核查，默认发布版本均为 `1.231.0`，GitHub 发布标题为 `1.231.0 Beta`，发布说明将其列为计划中的最后一个 1.x 版本。PyPI 同时提供 `2.0.0rc5`，上传日期为 2026-09-15。在线安装文档已面向 2.x，并明确不建议候选发布版用于真实资金交易。

用户在两个版本的离线验证之后，已确认使用 2.x 开展研发，等待正式发布并完成验证后接实盘。实盘具体版本尚未确定。以下 1.x 结果保留为选型证据，不是当前研发路线。

来源：[1.231.0 发布说明](https://github.com/nautechsystems/nautilus_trader/releases/tag/v1.231.0)、[PyPI 发布信息](https://pypi.org/pypi/nautilus_trader/json)、[官方安装说明](https://nautilustrader.io/docs/latest/getting_started/installation/)。这些是本次核查结果；确定实施版本时需再次核实发布状态。

### 4.1 已完成的 1.231.0 离线验证

验证环境为本机 Windows、Python 3.12 和 uv 隔离依赖环境。以下回测结果仅针对 `nautilus_trader.backtest.engine.BacktestEngine` 的旧版 Python/Cython 核心，不代表同一软件包中的 Rust 核心或 2.x 行为。

| 检查 | 已验证结果 |
| --- | --- |
| 安装与导入 | 1.231.0 安装成功，回测引擎可创建；Binance、OKX 的行情与交易客户端工厂可导入 |
| 订单与持仓 | 合成行情下可建立 0.1 BTC 永续空头并扣除成交手续费 |
| 资金费数据 | 策略收到结算时刻的一次 `FundingRateUpdate` 回调 |
| 资金费入账 | 标记价 50,000 USDT、费率 0.0001 时，0.1 BTC 空头应收 0.5 USDT；与零费率对照相比，实际账户余额增量为 0 |
| 原生扩展接口 | 在 `SimulationModule` 中调用 `adjust_account`，账户余额确实增加 0.5 USDT；这只验证余额调整接口，不是资金费结算实现 |
| 保证金与清算 | 旧版核心提供 `MarginModel` 扩展；内置模型按合约固定比例计算，`add_venue` 无 `liquidation_enabled` 参数，不能将 Rust 核心的清算功能算作这条路径的已验证能力 |
| 交易状态持久化 | 该旧版 Python 核心的原生数据库配置只接受 Redis；已选 PostgreSQL 的用途仍是业务记录 |

资金费对照的两个最终余额均为 9,999.1 USDT；余额调整扩展试验为 9,999.6 USDT。样本使用合成数据，以上结果不构成交易所联调或实际策略收益结论。

可复现检查：[离线验证脚本](../../../checks/nautilus_v1.py)。从项目根目录运行：

```powershell
uv run --no-project --python 3.12 --with nautilus_trader==1.231.0 python checks/nautilus_v1.py
```

源码依据：[旧版回测引擎](https://github.com/nautechsystems/nautilus_trader/blob/v1.231.0/nautilus_trader/backtest/engine.pyx)、[模拟扩展接口](https://github.com/nautechsystems/nautilus_trader/blob/v1.231.0/nautilus_trader/backtest/modules.pyx)、[保证金模型](https://github.com/nautechsystems/nautilus_trader/blob/v1.231.0/nautilus_trader/accounting/margin_models.pyx)、[原生持久化配置](https://github.com/nautechsystems/nautilus_trader/blob/v1.231.0/nautilus_trader/system/kernel.py)。

### 4.2 已完成的 2.0.0rc5 离线验证

另行安装 `2.0.0rc5`，使用其原生 Python API 和同样的 0.1 BTC 空头、50,000 USDT 标记价，在实际结算时刻输入一条最终费率记录。未添加资金费结算扩展。

| 费率 | 最终账户余额（USDT） | 相对零费率的现金流（USDT） |
| --- | --- | --- |
| 0 | 9,999.1 | 0 |
| 0.0001 | 9,999.6 | +0.5 |
| -0.0001 | 9,998.6 | -0.5 |

三个离线用例均通过持仓数量、资金费回调和账户现金流断言。该版本还暴露 `liquidation_enabled` 配置，但本次未验证清算行为及其与两平台实际规则的一致性。原生资金费结算通过此样本，不能替代完整双腿回测、账户模式适配及实盘联调验收。

可复现检查：[2.x 离线验证脚本](../../../checks/nautilus_v2.py)。从项目根目录运行：

```powershell
uv run --no-project --python 3.12 --with nautilus_trader==2.0.0rc5 python checks/nautilus_v2.py
```

上述 `2.0.0rc5` 是已通过本次离线验证的研发起点，不是实盘依赖。官方仍不建议候选发布版用于真实资金交易。

### 4.3 2026-09-16 实施前复核

- 单腿检查及双腿检查已写入现有脚本，使用锁定依赖运行 `uv run --locked python checks/nautilus_v2.py` 通过。单腿正负资金费现金流仍为 +0.5 / -0.5 USDT；双腿零、正、负费率最终总余额分别为 19,993.1855、19,993.6855、19,992.6855 USDT。各用例完成四次成交、合计扣费 11.8145 USDT 并清空持仓；现货最终余额均为 9,999.99 USDT，永续分别为 9,993.1955、9,993.6955、9,992.6955 USDT。正费率净损益 -6.3145 USDT，总资金收益率 -0.0315725%。
- `2.0.0rc5` 的 OKX 历史解析函数读取 `raw.funding_rate`，而交易所文档把 `realizedRate` 定义为实际结算费率。因此该版本的原生历史结果不能直接作为本项目的 OKX 结算标签；数据导入须保留原始字段，并从 `realizedRate` 生成实际结算记录。来源：[版本源码](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc5/crates/adapters/okx/src/common/parse.rs#L591-L610)、[OKX 字段定义](https://app.okx.com/docs-v5/en/#public-data-rest-api-get-funding-rate-history)。
- 引擎按 `ts_init` 排序回放。双腿样本中只将资金费 `ts_init` 从结算时刻改为晚 3 秒，实际运行即报 `Late funding boundary`。离线账务应在结算时刻输入最终费率；策略特征另按研究文档的 `available_ts` 取数，不直接使用结算回放的费率回调或缓存作为当时已知特征。来源：[回放排序源码](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc5/crates/backtest/src/engine.rs#L409-L424)，本地临时回放复现。
- 原生执行检查在 Windows 和 Linux 上结果一致：同一 `BINANCE` 或 `OKX` Venue 注册两个 Sandbox 执行客户端时，引擎拒绝注册第二个。单个 MARGIN 账户虽接受现货与永续订单，但现货不形成现金库存：两腿各 0.1 BTC、成交价 50,000 USDT 时，20,000 USDT 仅扣除 5.9 USDT 手续费，没有 BTC 余额；CASH 账户则报 `Cash account cannot trade futures or perpetuals`。因此这些配置尚不能作为本项目现金现货加永续的前向模拟接入。复现：`uv run --locked python checks/execution.py`；[脚本](../../../checks/execution.py)、[Windows 结果](../../../data/execution/native_rc5.json)、[Linux 结果](../../../data/execution/linux_native_rc5.json)。
- 同一检查已复现原生部分成交、另一腿拒单及停止回调后仍保留持仓；这是事件能力验证，项目的对冲修复、保证金规则和停止处置尚未验收。前向采集取得公共 OI，但 [Binance 原生日志](../../../data/execution_probe.log)显示现货与永续 WebSocket 连接分别超时，节点未进入策略启动阶段；不能认定实时行情或断档恢复已通过。总计划任务 6/7 保持未通过。

## 5. 与目标对应的验收条件

以下保留当前目标的验收条件。历史买入分析页面及研究与回测 API 已实现；执行接入与实盘相关条件仍未通过，不能以离线检查通过代替整体验收。

- 页面只输入北京时间的历史日期和小时，即可提交分析并显示 M1 判断、B0 回放和分析记录；缺数据及失败有明确提示。
- API 能够提交研究与回测、查询任务和结果；后续实盘接口能够启动、停止和查询策略运行状态。
- 固定数据、参数和依赖版本后，可以复现因子、模型评估与回测结果；实验保留数据范围、参数和结果记录。
- 交易引擎的所选版本能够处理两平台所需现货与 USDT 线性永续交易；回测中的合约数量、资金费、手续费、基差损益及保证金口径与研究文档一致，能力缺口有明确验证结论。
- 回测能够按事件处理两腿成交、部分成交与资金费结算，并输出总资金净收益、回撤、未对冲敞口和保证金压力。
- 资金费验证必须核对账户现金流金额；仅收到资金费事件不算结算成功。
- 研究回测运行期间，实盘仍能独立接收行情、处理订单与持仓事件。
- 实盘所用 NautilusTrader 2.x 已正式发布，并通过上述账户、交易和回测验收。

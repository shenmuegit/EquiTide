# USDT 量化研究

Python 3.12、NautilusTrader 2.0.0rc5、PostgreSQL，以及 `web/` 下的 React、TypeScript、Vite 单页。当前提供历史买入分析页面、研究、回测与任务 API。自动交易和实盘管理尚未通过验收。

`Freqtrade/` 是上游 Freqtrade 的 Git 子模块；克隆本仓库时使用 `git clone --recurse-submodules`。`freqtrade_trial/` 保存 BTC/USDT 15 分钟线的指标策略、回测结果和未来数据偏差检查结果。

## 启动

Linux 安装 Docker Compose 后，在项目目录运行：

```sh
docker compose up -d --build
```

页面位于 <http://127.0.0.1:5178>，API 位于 <http://127.0.0.1:8000>，接口文档位于 <http://127.0.0.1:8000/docs>。计算在独立进程执行，记录保存在 PostgreSQL，行情和结果保存在 `data/`。数据库使用 Compose 的 `postgres` 卷；重启不会清空记录。页面与 API 端口分别可用 `USDT_QUANT_PORT`、`USDT_QUANT_API_PORT` 修改。

页面只需选择历史买入日期和小时（北京时间）。系统自动确定数据版本、资金、成本及研究参数，分别展示 M1 当时的判断和 B0 随后 24 小时基于历史数据的模拟回放；分析记录来自真实任务，支持深浅模式和手机布局。

本地 Python 开发：

```sh
uv sync --locked
uv run --locked python checks/nautilus_v2.py
uv run --locked python checks/data.py
uv run --locked python checks/backtest.py
uv run --locked python checks/research.py
uv run --locked python checks/execution.py
```

运行 API 前设置 `DATABASE_URL`（PostgreSQL 连接地址），以及可选的 `USDT_QUANT_DATA_ROOT`（默认项目 `data/`）。启动 `uv run --locked uvicorn usdt_quant.api:app --host 127.0.0.1 --port 8000`。`checks/runs.py` 使用 `DATABASE_URL` 检验真实 HTTP、数据库与计算进程。

## 数据和研究

```sh
uv run --locked python -m usdt_quant.data history --exchange binance --base BTC --start 2026-07-18T00:00:00Z --end 2026-09-16T00:00:00Z
uv run --locked python -m usdt_quant.data forward --exchange binance --base BTC --duration 60
```

平台可选 `binance`、`okx`，标的可选 `BTC`、`ETH`。原始响应在 `data/raw/`，规范数据在 `data/normalized/`，字段覆盖与缺口在 `data/coverage/`。OKX 手动导入入口为 `python -m usdt_quant.data import-okx --help`。

仓库只保存代码与轻量验证结果；`data/raw/`、`data/normalized/`、`data/research/` 和 `data/runs/` 中的历史数据及生成结果留在本地，可按本文命令重新获取或生成。

回测参数包含全部投入资金、数量、单腿费用、执行成本、决策间隔和持有期限，并随结果保存。单次研究使用预先登记的训练、验证、测试边界；跨边界或尚未成熟的标签被剔除，预处理只在训练段拟合。已有研究配置可从命令行复现：

```sh
uv run --locked python -m usdt_quant.research --data-dir <数据版本目录> --output-dir <结果目录> --config-json <配置文件>
```

## 已验证范围

前端已通过 `npm --prefix web run build` 和 `node --experimental-transform-types checks/frontend_api.mjs`；真实浏览器提交分析、读取结果及缺数据提示已验证。

双腿核算、数据导入、回测与研究的最小检查，以及 HTTP—数据库—计算进程链路均有可运行检查。Binance 已取得 BTC/ETH 基础样本和 BTC 60 天样本；OKX 两币旧成功样本可追溯到原始响应，但结算标记价缺失，不能给出精确资金费账目。

F01–F12 语义已实现。最新 BTC 60 天数据中 F08/F09/F10/F11 有样本，F05/F12 因真实历史输入缺失保持空值；模型当前仅纳入训练覆盖率 ≥98% 的 F01/F02/F03/F04/F06/F07/F10。示例 M1 预测净收益约 -2.3213 USDT，B0 强制 24 小时回放净损益为 -2.69014786 USDT。

原生执行能力检查在 Windows 和 Linux 上得到一致结果：同一 Venue 注册两个执行客户端会被拒绝；单个 MARGIN 账户将现货作为保证金持仓处理，不形成现金现货库存，CASH 账户则拒绝永续。原生部分成交、拒单和停止后仍有持仓的事件已复现，但项目的异常处置与前向双腿执行尚未通过。见[执行检查](checks/execution.py)、[Windows 结果](data/execution/native_rc5.json)和[Linux 结果](data/execution/linux_native_rc5.json)。

前向采集目前只验证到公共 OI；[原生日志](data/execution_probe.log)记录了 Binance 现货和永续 WebSocket 的连接超时，节点未进入策略启动阶段。实时盘口、成交与断档恢复仍未验收。总计划任务 6/7 尚未通过；独立美元锚、实际账户费用/保证金规则与真实交易仍未验证。

Linux 容器已通过上述检查和 `checks/runs.py`；重启 Compose 后任务和完整报告保持一致。Linux 60 秒前向采集仍未收到原生行情事件，见[实际覆盖](data/forward/binance_BTC_1789551258/coverage.json)。

实施进度只维护在 [总计划](docs/superpowers/plans/2026-09-16-usdt-project-build.md)。

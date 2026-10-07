# 首次规则查询失败，未启动账户

公开exchangeInfo请求的symbols JSON含空格，被接口以400/-1100拒绝。10个观察配置全部finish blocked，没有虚拟成交、没有真实订单，没有创建或重置资金账户。原始失败report及成功取得的time响应保留；只改变数组参数的紧凑编码后，用新报价与新的观察登记重新运行。复现诊断见../../validation/exchange_info_diagnosis.json。

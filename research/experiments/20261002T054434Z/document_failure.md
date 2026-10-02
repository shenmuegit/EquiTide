# 文档生成失败留痕

54历史配置及3累计观测已完成finish之后，document.py首次解析因第33行嵌套f-string中的多余引号转义报SyntaxError: unexpected character after line continuation character，未执行文档生成，也未重新执行策略。根因是构造字符串时保留了不应出现的反斜杠；将逐折格式字符串先存fold_text后再插入表格，源码compile与完整生成成功。回测报告/源码、spec、登记状态及SHA均未改变。全部策略计算/audit此前成功；这是文档阶段失败。

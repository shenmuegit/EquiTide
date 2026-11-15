"""Configure only current account windows, receipts and publication metadata before binding."""
import ast,json,re,sys
from datetime import datetime,timedelta
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import put,now
assert not any((R/n).exists() for n in ['plan.json','batch.json','code_binding_before_evaluation.json','report.json'])
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
p=R/'review/setup.py';s=p.read_text();s=re.sub(r'2026-11-15T(?:08:30|10:30|10:10|12:10):00Z',lambda m:(datetime.fromisoformat(m.group().replace('Z','+00:00'))+timedelta(hours=2)).isoformat().replace('+00:00','Z'),s)
s=s.replace('Original SMA/single08:30to10:30,L4/FEWM10:10to12:10','Original SMA/single10:30to12:30,L4/FEWM12:10to14:10').replace('sources only','sources only')
s=s.replace('receipts=[]',"receipts=json.loads((R/'initial_remote_sync_receipts.json').read_text())").replace("receipts[0]['stdout']==receipts[1]['stdout']","receipts[-2]['stdout']==receipts[-1]['stdout']");ast.parse(s);p.write_text(s)
edit('checks.py',[('actual08fundsplit0/6/0/0','actualcurrentfundsplit0/0/0/0')])
edit('review/diagnostics.py',[('actual BTC entry-volatility-cap trade changes','actual BTC entry-hurdle trade changes')])
edit('finalize.py',[("['2026-11-15T10:30:00Z','2026-11-15T12:30:00Z']","['2026-11-15T12:30:00Z','2026-11-15T14:30:00Z']"),("['2026-11-15T12:10:00Z','2026-11-15T14:10:00Z']","['2026-11-15T14:10:00Z','2026-11-15T16:10:00Z']"),("'wrong_context_path_read_fact':1,'metadata_writer_parse_error_fact':1","'wrong_context_path_read_fact':0,'metadata_writer_parse_error_fact':0"),("['bootstrap.py', 'prepare.py'","['bootstrap.py', 'configure.py', 'prepare.py'")])
edit('publish.py',[('research: validate BTC ROC memory neighborhood with frozen risk filters','research: validate BTC entry hurdle neighborhood after execution costs')])
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_freeze_and_account_stdout_labels_corrected_before_binding':True,'prior_round_raw_logs_and_notes_unchanged':True,'financial_or_account_reruns':0})
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[{'requested_url':'https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History','actual_url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','web_reference':'turn286view0','access_UTC_date':'2026-11-15','read_success':True,'redirected':True},{'requested_url':'https://github.com/binance/binance-public-data/blob/master/README.md','actual_url':'https://github.com/binance/binance-public-data/blob/master/README.md','web_reference':'turn286view1','access_UTC_date':'2026-11-15','read_success':True}],'tool_timeouts':0,'HTTP_capture_timestamp_not_claimed':True})
(R/'research_work_plan.md').write_text('''本轮预先固定：BTC严格入场阈值H2.5%/3%/3.5% × ETH预算R .00875/.01；L29/E .005/V10/cap .0275及BTC本金3750/名义1000固定，ETH原15000/4000银行只读。旧H3%中心与对照只读，新2原生+4被动父；raw权重[1,1]保留，事前代表H2.5%/R.01。391日复用历史、原成本和资格门槛保持。
执行：完整数据/源码核验→全部完整spec和plan→逐一定义reserve→一次全期真实计算→独立核算审计、逐折/逐变体/连续NAV与敏感性图→逐一finish→各原账户新窗口独立reserve/延续/审计/finish→登记片段/只读监控/检查→封存/提交push/远端核验/释放锁。失败和负收益同样保存，不事后扩批或换代表。
本轮SMA/single10:30→12:30，L4/FEWM12:10→14:10；先查实际结算，不假定名义八小时。下轮L4/FEWM14:10→16:10可能跨实际16时结算，必须新查真实fundingTime并按各自持仓计账；三账户原08结算不可重复。日决策仍Nov16_00:01，完整67日权威和旧66/65前缀保留，不采用新研究参数到原冻结账户。
验证重点：严格阈值相等、真实持仓滞回、未来后缀排除、已完成前缀/下一OPEN、净资金费与1/2/3成本、原资本真实数量及平方根冲击、全共同事件轴DD；旧参考与账户NAV前缀/资金费唯一键保持。引擎与资金核算原字节不变。
''')
print('PASS current windows,complete initial-sync receipts and native publication metadata configured;0financial/account calculations')

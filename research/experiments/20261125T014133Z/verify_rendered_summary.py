"""Correct saved prose counts and next-direction wording, without financial execution."""
import copy,gzip,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'rendered_summary_binding.json');assert sha(Path(__file__))==b['source_sha256'] and b['bound_before_summary_correction'] and b['bound_after_completed_financial_and_account_evaluations']
assert all(sha(ROOT/p)==h for p,h in b['financial_and_original_account_artifacts_sha256'].items())
eco=rd(R/'joint_economic_review.json');count=len(eco['comparison_rows']);assert count==6 and eco['old_weakly_dominated_rows']==count
text=(R/'result.md').read_text();nxt=rd(R/'next_research_state.json');before=copy.deepcopy(nxt);assert sha(R/'result.md')==b['result_before_sha256'] and sha(R/'next_research_state.json')==b['next_state_before_sha256']
backup=R/'first_rendered_summary_before_wording_fix.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(json.dumps({'result.md':text,'next_research_state.json':nxt},ensure_ascii=False,sort_keys=True).encode(),mtime=0))
assert text.count('12成本行中')==1 and text.count('均已将08及16实际事件')==1
text=text.replace('12成本行中',str(count)+'成本行中').replace('均已将08及16实际事件','均已将Nov23_08及Nov23_16实际事件')
m=next(z for z in eco['native_mechanism_rows'] if z['asset']=='BTC' and z['coordinate']==.0275 and z['cost']==3)
text+='\n保存数值复核：两个新组合共6条成本对照记录，全部被相同ETH预算窗口下BTC H.03旧组合弱支配。BTC H.0275相对H.03在3倍成本下多'+str(m['delta_executions'])+'次执行、'+str(m['delta_round_trips'])+'次完整交易，毛价格收益减少'+str(-m['delta_gross_reference_price_PnL_usdt'])+' USDT；两新组合净收益各低约0.54170138个百分点，整体回撤相同。历史绝对门槛passed保留，未提升为更优候选。原文的12成本行计数更正为6，首次生成文本和交接状态原样留档；未重跑回测或账户。\n'
text+='\n工程检查说明：units阶段沿用了上一轮退出缓冲坐标，实际在bind/reserve/金融及账户计算之前失败；原始日志和失败源码保存在engineering_fix_before_binding.json。修正坐标、14个ID/28事件和L4/FEWM各6条资金费边界后，独立units_retry通过，再执行首次reserve与计算。失败回执未覆盖。\n'
(R/'result.md').write_text(text)
nxt['next_direction_basis']='本轮仅补测BTC H.0275×ETH资金费预算波动估计窗8/10两个新图；H.0325角点此前已有真实结果，九格共七旧格只读。新图均未优于相同ETH窗口的H.03旧组合，其中VW10完整净值还与旧H.0275/VW9相同。下轮先读完整元数据和实际结论，检查尚未测试的具体风险/趋势参数组合；已有组件净值优先只读复用，避免重复已完成完整配置。'
put(R/'next_research_state.json',nxt);assert {k:v for k,v in nxt.items() if k!='next_direction_basis'}=={k:v for k,v in before.items() if k!='next_direction_basis'}
assert all(sha(ROOT/p)==h for p,h in b['financial_and_original_account_artifacts_sha256'].items())
put(R/'rendered_summary_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':b['source_sha256'],'first_rendered_copy':str(backup.relative_to(ROOT)),'first_rendered_copy_sha256':sha(backup),'result_before_sha256':b['result_before_sha256'],'result_after_sha256':sha(R/'result.md'),'next_state_before_sha256':b['next_state_before_sha256'],'next_state_after_sha256':sha(R/'next_research_state.json'),'actual_matched_cost_rows':count,'only_next_direction_prose_changed':True,'first_sources_counts_quantities_all_handoff_fields_unchanged':True,'all_financial_and_original_account_artifacts_unchanged':b['financial_and_original_account_artifacts_sha256'],'new_financial_account_order_cashflow_or_model_evaluations':0})
print(json.dumps({'passed':True,'actual_cost_rows':count,'only_saved_prose_changed':True,'financial_and_account_reports_unchanged':True,'new_evaluations':0}))

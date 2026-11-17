"""Pin this round's first actual 16UTC source before any reserve or account calculation."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;assert not(R/'plan.json').exists();f=R/'new_actual_settlement_preflight.json';d=json.loads(f.read_text());rows=d['public_fields_by_asset'];assert set(rows)=={'BTC','ETH'}
for a,xs in rows.items():
 assert len(xs)==1 and datetime.fromtimestamp(int(xs[0]['fundingTime'])/1000,timezone.utc).isoformat().startswith('2026-11-17T16:00:00') and xs[0]['symbol']==a+'USDT' and 'fundingRate' in xs[0] and 'markPrice' in xs[0]
dest=R/'funding16_nov17_preflight.json';assert not dest.exists();dest.write_bytes(f.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();binding=R/'original_accounts_binding.json';b=json.loads(binding.read_text());b['sources_sha256'][str(dest.relative_to(ROOT))]=sha(dest);binding.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n');(R/'new_settlement_source_binding.json').write_text(json.dumps({'passed':True,'source':str(dest.relative_to(ROOT)),'sha256':sha(dest),'first_capture_utc':d['recorded_utc'],'all_actual_public_fields':rows,'no_cashflow_calculation':True,'before_first_reservation':True},indent=2)+'\n');print(json.dumps({'passed':True,'source':str(dest.relative_to(ROOT)),'first_capture_utc':d['recorded_utc'],'actual_fields':rows,'no_account_calculation':True}),flush=True)

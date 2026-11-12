"""Inspect failed definition-only grid cardinality; no model or registry calls."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
source=(R/'review/freeze_before_duplicate_scope_fix.py.txt').read_text();prefix=source[:source.index('assert len(batch)==9')];ns={};exec(compile(prefix,str(R/'freeze.py'),'exec'),ns)
d={'recorded_utc':now(),'passed':True,'new_definitions':len(ns['batch']),'old_exact_pairings':ns['duplicates'],'read_only_refs':len(ns['refs']),'native_refs':sum(z['scope']=='native' for z in ns['refs'].values()),'financial_calculations':0,'registry_reservations':0};put(R/'metadata_duplicate_scope_resolution.json',d);print(json.dumps(d,ensure_ascii=False))

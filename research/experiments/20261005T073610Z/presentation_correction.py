"""Preserve original published figure identities and repair labels without reevaluating any strategy."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;R=T.parents[2];prior=R/'research/experiments/20261005T053510Z'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def render_exit_correction():
 r=json.loads((prior/'report.json').read_text());fig,axes=plt.subplots(2,3,figsize=(13,7));entries=r['plan']['grid']['entry_lookback_days'];exits=r['plan']['grid']['exit_lookback_days'];assert exits==[15,25,30]
 for i,y in enumerate(('2025','2026')):
  for j,a in enumerate(('BTC','ETH','combination')):
   cells={(c['exit_days'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[cells[x,e]['scenes']['3']['net_return_pct'] for e in entries] for x in exits]);ax=axes[i,j];ax.imshow(v,cmap='RdYlGn',vmin=-20,vmax=60)
   for ii,x in enumerate(exits):
    for jj,e in enumerate(entries):ax.text(jj,ii,f'{v[ii,jj]:.2f}%',ha='center',va='center')
   ax.set_xticks(range(3),entries);ax.set_yticks(range(3),exits);ax.set_xlabel('Entry days');ax.set_ylabel('Exit days');ax.set_title(f'{y} {a}, 3x costs')
 fig.tight_layout();out=T/'previous_053510_sensitivity_corrected.png';fig.savefig(out,dpi=130);plt.close(fig);return out
if __name__=='__main__':
 out=render_exit_correction();note=json.loads((T/'presentation_correction.json').read_text());assert sha(prior/'sensitivity.png')==note['prior_original_figure_sha256'];assert sha(T/'report.json')==note['unchanged_current_report_sha256'];assert sha(prior/'report.json')==note['unchanged_prior_report_sha256'];assert sha(R/'research/automation/registry.jsonl')==note['unchanged_registry_sha256'];note.update(current_corrected_figure_sha256=sha(T/'sensitivity.png'),prior_corrected_copy=str(out.relative_to(R)),prior_corrected_copy_sha256=sha(out));(T/'presentation_correction.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n');print('PASS: graph labels follow frozen axes; all numerical reports and registry unchanged')

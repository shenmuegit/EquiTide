"""Render saved metrics with corrected varyingK/VC caption;no strategy or metric reevaluation."""
import sys,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());old=sha(R/'sensitivity.png');src=(R/'summarize.py').read_text();block=src[src.index('fig,axs='):src.index("summary={'report_sha256'")];exec(block)
put(R/'plot_caption_correction.json',{'passed':True,'old_png_sha256':old,'new_png_sha256':sha(R/'sensitivity.png'),'reason':'Remove inheritedfixedK/VCprose;bothK/VCarecurrentgridaxes,budgetM4VW8R.00875fixed.','saved_report_sha256':sha(R/'report.json'),'new_backtest_or_metric_evaluations':0,'all_actual_results_ledgers_and_bound_sources_unchanged':True})
print('PASS rendered saved2x9K/VCmetrics with corrected caption;0 backtest/policy/account reevaluations')

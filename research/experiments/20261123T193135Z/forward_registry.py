"""Reserve the original daily cutoff and finish only actual audited partial results."""
import argparse,json
from common import R,call,put,rel
import forward
def reserve():forward.reserve()
def finish():
 assert json.loads((R/'forward_verification.json').read_text())['passed'];done=[]
 for row in json.loads((R/'forward_batch.json').read_text()):done.append(call('finish',row,'rejected',rel(R/'forward_report.json')));put(R/'forward_finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['reserve','finish']);globals()[p.parse_args().command]()

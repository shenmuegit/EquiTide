import runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.argv=[str(R/'review/test_tail_stats.py'),'core391_tail_safe.py'];runpy.run_path(sys.argv[0],run_name='__main__')

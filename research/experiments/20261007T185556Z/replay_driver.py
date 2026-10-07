"""Force fresh component recalculation during offline replay; no pending-result shortcut."""
import importlib.util,sys
from pathlib import Path
T=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('replay_allocation_driver',T/'evaluate.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
m.allocation.component=m.original_component
if '--reproduce' not in sys.argv:sys.argv.append('--reproduce')
m.allocation.main()

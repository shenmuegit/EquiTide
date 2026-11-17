"""Final read-only source AST after date-qualified handoff formatting."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
runpy.run_path(str(R/'review/validate_sources.py'),run_name='__main__')

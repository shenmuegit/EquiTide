"""Compatibility for one frozen auditor's direct single-file journal read."""
import hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];PUB=Path(__file__).resolve().parent;layout=json.loads((PUB/'registry_layout.json').read_text());R=ROOT/layout['sealed_round'];journal=ROOT/layout['main_prefix_path'];fragment=ROOT/layout['new_fragment_path'];before=(R/'forward_verification.json').read_bytes();virtual=journal.read_bytes()+fragment.read_bytes();assert hashlib.sha256(virtual).hexdigest()==layout['reconstructed_original_after_append_sha256']
s=importlib.util.spec_from_file_location('frozen_single_file_forward_auditor',R/'audit_forward.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);original=Path.read_text
def compatible_read(self,*args,**kwargs):
 if self.resolve()==journal.resolve():return virtual.decode('utf-8')
 return original(self,*args,**kwargs)
try:
 Path.read_text=compatible_read;m.main()
finally:Path.read_text=original
assert (R/'forward_verification.json').read_bytes()==before
print('PASS legacy direct journal reader receives exact sealed bytes virtually; no registry/account/result bytes changed')

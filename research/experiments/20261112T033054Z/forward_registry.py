"""Dispatch original SMA65 daily-crossing reservation and finish without changing rules."""
import argparse
from forward import reserve,finish
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['reserve','finish']);globals()[p.parse_args().command]()

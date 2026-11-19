"""Readonly post-unlock hash, actual ledger and original midnight handoff audit."""
import copy, gzip, hashlib, json, subprocess
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path.cwd()
assert str(ROOT) == '/home/desktop/Documents/Codex/EquiTide'
R = ROOT / 'research/experiments/20261119T143526Z'
P = ROOT / 'research/experiments/20261119T123454Z'
F = ROOT / '.git/automation_proofs'
pf = F / (R.name + '.json')
rd = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
x = rd(pf)
m = rd(R / 'data_manifest.json')
own = x['commit']
release = x['native_flock_release']
assert release['exit_code'] == 0 and release['broker_pid'] == m['branch_lock_broker_pid'] and 'LOCK_RELEASED' in release['output']
assert rd(ROOT / x['effective_successful_seal_receipt'])['exit_code'] == rd(F / (R.name + '_publish_receipt.json'))['exit_code'] == 0
assert x['complete_tree_and_evidence_verification']['passed']
pid = m['branch_lock_broker_pid']
assert not Path('/proc', str(pid)).exists()
assert not any('FLOCK' in l and str(pid) in l.split() for l in Path('/proc/locks').read_text().splitlines())
assert sha(R / 'data_manifest.json') == x['precommit_sha256'][str((R / 'data_manifest.json').relative_to(ROOT))]
published = lambda path: subprocess.check_output(['git', 'show', own + ':' + path], cwd=ROOT)
peer = []
for path, h in {**m['artifacts'], **m['protected_inputs_sha256'], **m['code_and_frozen_source_sha256']}.items():
    actual = sha(ROOT / path)
    if actual != h and path == 'research/paper10/state.json':
        assert hashlib.sha256(published(path)).hexdigest() == h
        peer.append({'path': path, 'published_sha256': h, 'later_sha256': actual})
    else:
        assert actual == h, path
for path, item in m['shared_files'].items():
    old = published(path)
    assert hashlib.sha256(old).hexdigest() == item['sha256'], path
    if sha(ROOT / path) != item['sha256']:
        assert path in {'research/automation/registry.jsonl', 'research/monitor/latest.json', 'research/monitor/configs.json.gz'}, path
        if path == 'research/automation/registry.jsonl':
            assert (ROOT / path).read_bytes().startswith(old)
        peer.append({'path': path, 'published_sha256': item['sha256'], 'later_sha256': sha(ROOT / path), 'later_work_preserved': True})
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert subprocess.run(['git', 'merge-base', '--is-ancestor', own, head], cwd=ROOT).returncode == 0
assert subprocess.check_output(['git', 'for-each-ref', '--format=%(refname)', 'refs/heads'], cwd=ROOT, text=True).strip() == 'refs/heads/main'
aw = rd(R / 'account_window_verification.json')
w = rd(R / 'account_windows.json')
h = rd(R / 'next_research_state.json')['UTC_midnight_handoff']
fresh = rd(R / 'window_funding_preflight.json')
assert aw['passed'] and aw['current_funding_records_by_account'] == {a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}
assert aw['current_daily_event_counts'] == {a:len(w[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}
books = {}
for stem in ['candidate', 'l4h02', 'fewm']:
    W = R / (stem + '_observation')
    before = rd(ROOT / rd(W / 'previous_pointer.json')['state'])
    after = rd(W / 'state.json')
    delta = json.loads(gzip.decompress((W / 'delta.json.gz').read_bytes()))
    v = rd(R / (stem + '_verification.json'))
    assert v['passed'] and v['cost_scenes'] == 9 and v['full_NAV_points_checked'] == 9 * v['NAV_points_per_scene']
    assert v['new_daily_events'] == aw['current_daily_event_counts'][stem] and v['new_fills'] == aw['current_fills_by_account'][stem]
    assert v['new_funding_settlements'] == aw['current_funding_records_by_account'][stem]
    ledger = copy.deepcopy(before['books'])
    for z in delta['journal']:
        asset, k = z['asset'], str(z['cost_multiplier'])
        b = ledger[asset][k]
        if z['kind'] == 'funding':
            row = next(q for q in fresh['public_fields_by_asset'][asset] if int(q['fundingTime']) * 1000000 == z['timestamp_ns'])
            q = D(b['signed_units'])
            base = -q * D(row['markPrice']) * D(row['fundingRate'])
            amount = base * int(k) if base < 0 else base
            assert D(z['signed_units']) == q and D(z['base_amount_usdt']) == base and D(z['amount_usdt']) == amount
            assert D(z['cash_before']) == D(b['cash']) and D(z['cash_after']) == D(b['cash']) + amount
            if amount:
                b['cash'] = str(D(b['cash']) + amount)
        elif z['kind'] == 'trade':
            assert z['status'] == 'filled' and all(D(z['state_before'][key]) == D(val) for key, val in b.items())
            cash, q, entry = [D(b[key]) for key in ['cash', 'signed_units', 'entry_price']]
            fee = D(z['quantity']) * D(z['execution']) * D('.0005') * int(k)
            assert D(z['cost_parts']['fee']) == fee
            wanted_cash = cash - fee if z['opening'] else cash + q * (D(z['execution']) - entry) - fee
            assert D(z['state_after']['cash']) == wanted_cash
            ledger[asset][k] = copy.deepcopy(z['state_after'])
        else:
            assert z['kind'] == 'decision'
    assert ledger == after['books']
    if v['new_fills'] == 0:
        for asset, scenarios in before['books'].items():
            for k, book in scenarios.items():
                assert all(after['books'][asset][k][key] == val for key, val in book.items() if key != 'cash')
    for asset, scenarios in before['books'].items():
        for k, book in scenarios.items():
            changes = [D(z['change_signed_units']) for z in delta['journal'] if z['kind']=='trade' and z['status']=='filled' and z['asset']==asset and str(z['cost_multiplier'])==k]
            expected_units = D(book['signed_units']) + sum(changes,D(0))
            assert D(after['books'][asset][k]['signed_units']) == expected_units
            assert h['current_original_signed_units_by_asset_cost'][stem][asset][k] == after['books'][asset][k]['signed_units']
    assert len(after['context']['BTC']['daily']) - len(before['context']['BTC']['daily']) == aw['current_daily_event_counts'][stem]
    books[stem] = {'own_books_reconciled': True, 'quantity_conservation_from_actual_filled_trade_changes': True, 'NAV_points': v['NAV_points_per_scene'], 'new_funding_rows': v['new_funding_settlements'], 'new_daily_events': v['new_daily_events'], 'new_fills': v['new_fills'], 'complete_prefix_audit_passed': True}
fv = rd(R / 'forward_verification.json')
assert fv['passed'] and fv['new_daily_decisions'] == 2 and fv['new_reference_points'] == 1 and fv['independent_frozen_signal_cost_balance_NAV_and_nextstate_verified']
assert rd(R / 'SMA_daily_binding.json')['passed']
assert h['next_SMA_single_window_utc']==['2026-11-19T00:30:00Z','2026-11-19T02:30:00Z'] and not h['next_SMA_single_expected_daily_events_utc']
assert h['SMA_current_full_daily_context']==71 and h['SMA_next_full_daily_context_required']==71 and not h['SMA_next_requires_original_daily_adapter']
assert sha(ROOT/h['SMA_full71_authority'])==h['SMA_full71_sha256']==rd(R/'SMA_daily_binding.json')['full71_sha256']
assert h['next_L4_FEWM_window_utc']==['2026-11-19T02:10:00Z','2026-11-19T04:10:00Z'] and not h['next_L4_FEWM_expected_daily_events_utc']
assert h['next_L4_FEWM_preparation_action']['already_booked_actualNov19_00_do_not_repeat'] and h['next_L4_FEWM_preparation_action']['preserve_original_first19_00_source_UTC_bytes']
assert h['next_SMA_single_preparation_action']['never_reuse_L4_FEWM_funding_amounts'] and h['next_SMA_single_preparation_action']['candidate_actualNov19_00_and_original_daily_already_booked_once']
assert h['L4_FEWM_actualNov19_00_booked_once'] and not h['single_actualNov19_00_not_yet_booked'] and h['all3_perp_actualNov19_00_booked_once'] and h['all4_originalNov19_daily_booked_once']
assert sha(R/'funding00_nov19_preflight.json')==h['actual_Nov19_00_source_sha256']==rd(R/'actual00_nov19_prebinding_source.json')['sha256'] and rd(R/'funding00_nov19_preflight.json')['recorded_utc']==h['original_Nov19_00_capture_utc']
assert rd(R/'funding00_nov19_reconciliation.json')['passed']
assert h['L4_FEWM_actualNov18_00_booked_once'] and not h['single_actualNov18_00_not_yet_booked'] and h['all3_perp_actualNov18_00_booked_once'] and h['all4_originalNov18_daily_booked_once']
assert sha(R / 'funding00_nov18_preflight.json') == sha(P / 'funding00_nov18_preflight.json') == h['actual_Nov18_00_source_sha256'] and rd(R / 'funding00_nov18_preflight.json')['recorded_utc'] == h['original_Nov18_00_capture_utc']
assert h['L4_FEWM_actualNov18_08_booked_once'] and not h['single_actualNov18_08_not_yet_booked'] and h['all3_perp_actualNov18_08_booked_once']
assert sha(R / 'funding08_nov18_preflight.json') == sha(P / 'funding08_nov18_preflight.json') == h['actual_Nov18_08_source_sha256'] and rd(R / 'funding08_nov18_preflight.json')['recorded_utc'] == h['original_Nov18_08_capture_utc']
assert rd(R / 'funding08_reconciliation.json')['passed'] and rd(R / 'funding08_reconciliation.json')['all3_perps_booked_once_no_duplicate_keys']
assert rd(R / 'funding16_reconciliation.json')['passed'] and h['L4_FEWM_actualNov18_16_booked_once'] and not h['single_actualNov18_16_not_yet_booked'] and h['all3_perp_actualNov18_16_booked_once']
assert sha(R / 'funding16_nov18_preflight.json') == h['actual_Nov18_16_source_sha256'] == rd(R / 'actual16_prebinding_source.json')['sha256'] and rd(R / 'funding16_nov18_preflight.json')['recorded_utc'] == h['original_Nov18_16_capture_utc']
for name in ['funding08_nov17_preflight.json', 'funding16_nov17_preflight.json']:
    assert sha(R / name) == sha(P / name)
assert rd(R / 'sizing_effect_decomposition.json')['passed'] and rd(R / 'verification.json')['passed']
assert sha(R / 'engine.py') == sha(P / 'engine.py') and sha(R / 'core391_tail_safe.py') == sha(P / 'core391_tail_safe.py')
assert rd(R / 'report.json')['configs'] and m['new_actual_results']['financial_evaluation_runs'] == 1
proof = {'passed': True, 'verified_utc': datetime.now(timezone.utc).isoformat(), 'own_commit': own, 'HEAD_at_readonly_check': head, 'sealed_artifacts_unchanged': len(m['artifacts']), 'protected_files_verified_in_published_commit': len(m['protected_inputs_sha256']), 'subsequent_authorized_peer_changes': peer, 'original_account_checks': books, 'SMA_NAV_points': fv['NAV_points_per_scene'], 'current_actual_funding_split': aw['current_funding_records_by_account'], 'current_daily_event_counts': aw['current_daily_event_counts'], 'current_fills_by_account': aw['current_fills_by_account'], 'SMA_actual_full71_exact70prefix_retained': True,'current_daily_split_verified':aw['current_daily_event_counts'],'current_L4_FEWM_midnight_processed_once':True,'SMA_candidate_midnight_and_full71_completed_once_next_markonly':True, 'next_L4_FEWM_actual_new_funding_lookup_required': True, 'own_native_lock_released': True, 'completed_model_or_window_reruns': 0}
x['post_release_final_verification'] = proof
x['status'] = 'completed_published_verified_unlocked_peer_work_preserved' if peer else 'completed_published_verified_unlocked'
x['final_main_commit'] = head
pf.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(proof, ensure_ascii=False), flush=True)

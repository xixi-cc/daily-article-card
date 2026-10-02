import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import card_workflow as w


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.checkpoint = self.root / 'checkpoint.json'
        self.checkpoint.write_text('{"test": "synthetic, no paper processed"}')
        self.state = self.root / 'runtime'
        rows = [dict(key=f'Daily:2609.0000{i}', already_started=True,
                     artifacts={'checkpoint': str(self.checkpoint)}) for i in range(3)]
        rows.append(dict(key='Collection:2608.00001', already_started=False))
        w.initialize(self.state, dict(rows=rows, authority={'scope': str(self.checkpoint)}))

    def transition(self, key, stage):
        return w.record(self.state, 'transition', dict(key=key, stage=stage, note='Synthetic test',
                         artifacts={'receipt': str(self.checkpoint)}))

    def measurement(self, identity='one', start='2026-10-02T00:00:00Z', end='2026-10-02T00:01:00Z', usage=None):
        return dict(key='Daily:2609.00000', measurement_id=identity, stage='reading',
                    started_at=start, ended_at=end, usage=usage or {},
                    artifacts={'runtime_receipt': str(self.checkpoint)})

    def test_scope_and_terminal_do_not_reopen(self):
        with self.assertRaisesRegex(ValueError, 'stopped by scope'):
            self.transition('Collection:2608.00001', 'claimed')
        self.transition('Daily:2609.00000', 'source_exception')
        with self.assertRaisesRegex(ValueError, 'terminal'):
            self.transition('Daily:2609.00000', 'claimed')
        with self.assertRaisesRegex(ValueError, 'unknown paper'):
            self.transition('Daily:2609.99999', 'claimed')

    def test_active_limit_and_append_only(self):
        before = (self.state/'events.jsonl').read_bytes()
        self.transition('Daily:2609.00000', 'claimed')
        self.transition('Daily:2609.00001', 'claimed')
        with self.assertRaisesRegex(ValueError, 'limit'):
            self.transition('Daily:2609.00002', 'claimed')
        self.assertTrue((self.state/'events.jsonl').read_bytes().startswith(before))
        self.transition('Daily:2609.00001', 'unable_to_finish')
        self.transition('Daily:2609.00002', 'claimed')
        self.assertEqual(w.report(self.state)['counts']['claimed'], 2)

    def test_skip_and_duplicate_transition_rejected(self):
        with self.assertRaisesRegex(ValueError, 'transition'):
            self.transition('Daily:2609.00000', 'published')
        self.transition('Daily:2609.00000', 'claimed')
        with self.assertRaisesRegex(ValueError, 'transition'):
            self.transition('Daily:2609.00000', 'claimed')

    def test_token_accounting_unknown_and_parallel_wall(self):
        w.record(self.state, 'measurement', self.measurement(usage=dict(input_tokens=100, cached_input_tokens=80, output_tokens=10)))
        second = self.measurement('two', '2026-10-02T00:00:30Z', '2026-10-02T00:01:30Z')
        second['key'] = 'Daily:2609.00001'
        w.record(self.state, 'measurement', second)
        summary = w.report(self.state)['stages']['reading']
        self.assertEqual(summary['elapsed_seconds_sum'], 120)
        self.assertEqual(summary['covered_wall_seconds'], 90)
        self.assertEqual(summary['uncached_input_plus_output_known_sum'], 30)
        self.assertEqual(summary['effective_usage_unknown_measurements'], 1)
        self.assertEqual(summary['usage']['input_tokens']['unknown_measurements'], 1)

    def test_duplicate_measurement_not_counted(self):
        data = self.measurement()
        w.record(self.state, 'measurement', data)
        before = (self.state/'events.jsonl').read_bytes()
        with self.assertRaisesRegex(ValueError, 'already recorded'):
            w.record(self.state, 'measurement', data)
        self.assertEqual(before, (self.state/'events.jsonl').read_bytes())

    def test_invalid_time_and_usage(self):
        for fields in [dict(ended_at='2026-10-01T00:00:00Z'), dict(started_at='2026-10-02T00:00:00'),
                       dict(usage={'input_tokens': 1, 'cached_input_tokens': 2}),
                       dict(usage={'input_tokens': -1}), dict(usage={'output_tokens': True})]:
            with self.assertRaises(ValueError):
                w.record(self.state, 'measurement', dict(self.measurement(), **fields))

    def test_corruption_and_truncated_write_fail_closed(self):
        path = self.state/'events.jsonl'
        original = path.read_text()
        for bad in [original.replace('registered', 'published', 1), original + '{', original.rstrip('\n')]:
            path.write_text(bad)
            with self.assertRaises(ValueError):
                w.report(self.state)
        path.write_text(original)
        self.assertEqual(w.report(self.state)['event_count'], 1)

    def test_concurrent_writer_fails(self):
        with w.locked(self.state):
            with self.assertRaises(BlockingIOError):
                self.transition('Daily:2609.00000', 'claimed')

    def test_authority_drift_blocks_mutation(self):
        self.checkpoint.write_text('changed scope')
        with self.assertRaisesRegex(ValueError, 'changed evidence'):
            self.transition('Daily:2609.00000', 'claimed')

    def test_integrity_audit_tracks_artifact_drift(self):
        self.assertTrue(w.audit(self.state)['artifacts_unchanged'])
        self.checkpoint.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'changed evidence'):
            w.audit(self.state)

    def test_per_paper_report(self):
        w.record(self.state, 'measurement', self.measurement())
        self.assertEqual(w.report(self.state, 'Daily:2609.00000')['stages']['reading']['measurements'], 1)
        self.assertEqual(w.report(self.state, 'Daily:2609.00001')['stages'], {})

    def test_cannot_reinitialize(self):
        with self.assertRaisesRegex(ValueError, 'already exists'):
            w.initialize(self.state, dict(rows=[dict(key='Daily:x', already_started=False)],
                                        authority={'scope': str(self.checkpoint)}))

    def test_batch_is_bounded_and_only_sealed(self):
        for stage in w.STAGES[1:-1]:
            self.transition('Daily:2609.00000', stage)
        self.assertEqual(w.batch(self.state)['keys'], ['Daily:2609.00000'])
        self.transition('Daily:2609.00000', 'published')
        self.assertEqual(w.batch(self.state)['keys'], [])


if __name__ == '__main__':
    unittest.main()

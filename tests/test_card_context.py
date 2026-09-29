from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from card_context import brief, packet, receipt, reference
from prepare_card_intakes import prepare
from reconcile_card_resume import digest


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root/'production'
        self.repo.mkdir()
        for name in ['AGENTS.md','docs/PAPER_CARD_STANDARD.md','docs/PAPER_CARD_STANDARD_INTEGRATION.md',
                     'docs/CODEX_DAILY_SCREENING_AND_PUBLICATION.md']:
            p = self.repo/name
            p.parent.mkdir(exist_ok=True)
            p.write_text('Fixture instructions')
        self.card = self.root/'frozen/card.json'
        self.card.parent.mkdir()
        self.card.write_text(json.dumps(dict(arxiv_id='2609.12594', source_version='v1',
                                            title_en='Fixture', sections=['DO_NOT_COPY_SCIENCE'*1000])))
        self.manifest = self.root/'manifest.json'
        self.data = dict(production=dict(cards=dict(path=str(self.repo),head='fixture')),
                         source_hashes={str(self.root/'frozen/scope-stop-20260929-corrected.json'):'fixture'},
                         rows=[dict(key='Daily:2609.12594', program='Daily', arxiv_id='2609.12594',
                                    cohort='accepted_staged_not_installed', next_action='delivery',
                                    staged_card=str(self.card), eligible_to_claim=False)])
        self.save_manifest()

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.data))

    def job(self):
        out = self.root/'job'
        packet(self.manifest, 'Daily:2609.12594', out, 'delivery_audit')
        return out

    def result(self, out):
        report = out/'work/report.md'
        report.write_text('Detailed fixture report stays outside parent context.')
        result = dict(schema_version=1,key='Daily:2609.12594',packet_sha256=digest(out/'packet.json'),
                      outcome='audit_complete',source_version='v1',summary='Mechanical audit only.',
                      risk_flags=[],next_action='Parent reviews receipt.',artifacts={},full_report=reference(report))
        return result

    def submit(self, job, result):
        p = job/'work/result.json'
        p.write_text(json.dumps(result))
        return receipt(job/'packet.json', p, self.root/'result.receipt.json')

    def test_bounded_brief_does_not_copy_entire_ledger(self):
        self.data['rows'] += [dict(key=f'Daily:other-{i}',program='Daily',cohort='stopped_unstarted',
                                  next_action='remain stopped', secret_detail='DO_NOT_COPY_SCIENCE') for i in range(1000)]
        self.save_manifest()
        r = brief(self.manifest,self.root/'brief',limit=5)
        body = (self.root/'brief/controller.json').read_text()
        self.assertEqual(len(json.loads(body)['preview']),5)
        self.assertNotIn('DO_NOT_COPY_SCIENCE',body)
        self.assertLess(r['controller_chars'],5000)

    def test_packet_contains_only_selected_paper_and_pointers(self):
        before = digest(self.manifest)
        job = self.job()
        data = json.loads((job/'packet.json').read_text())
        self.assertFalse(data['execution_authorized'])
        self.assertFalse(data['spawn_options']['fork_context'])
        self.assertNotIn('DO_NOT_COPY_SCIENCE',(job/'packet.json').read_text())
        self.assertEqual(digest(self.manifest),before)

    def test_receipt_does_not_accept_install_or_publish(self):
        job = self.job()
        self.submit(job,self.result(job))
        r = json.loads((self.root/'result.receipt.json').read_text())
        self.assertFalse(r['scientific_acceptance'])
        self.assertFalse(r['installed'])
        self.assertFalse(r['published'])
        self.assertFalse(r['original_queue_mutated'])

    def test_wrong_paper_rejected(self):
        job=self.job();result=self.result(job);result['key']='Daily:OTHER'
        with self.assertRaisesRegex(ValueError,'different paper'):
            self.submit(job,result)

    def test_unbounded_result_rejected_without_truncation(self):
        job=self.job();result=self.result(job);result['summary']='x'*401
        with self.assertRaisesRegex(ValueError,'1..400'):
            self.submit(job,result)

    def test_long_history_field_rejected(self):
        job=self.job();result=self.result(job);result['all_prior_papers']='irrelevant history'
        with self.assertRaisesRegex(ValueError,'unexpected fields'):
            self.submit(job,result)

    def test_changed_artifact_rejected(self):
        job=self.job();result=self.result(job);(job/'work/report.md').write_text('changed')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            self.submit(job,result)

    def test_changed_source_rejected(self):
        job=self.job();result=self.result(job);self.card.write_text('{}')
        with self.assertRaisesRegex(ValueError,'input changed'):
            self.submit(job,result)

    def test_other_paper_report_rejected(self):
        job=self.job();result=self.result(job);result['full_report']=reference(self.card)
        with self.assertRaisesRegex(ValueError,'outside this work unit'):
            self.submit(job,result)

    def test_changed_version_rejected(self):
        job=self.job();result=self.result(job);result['source_version']='v2'
        with self.assertRaisesRegex(ValueError,'version changed'):
            self.submit(job,result)

    def test_duplicate_worker_ownership_rejected(self):
        runtime=self.root/'runtime.json'
        runtime.write_text(json.dumps(dict(active_units=[dict(key='Daily:2609.12594',agent_id='1'),dict(key='Daily:2609.12594',agent_id='2')])))
        with self.assertRaisesRegex(ValueError,'Duplicate active'):
            brief(self.manifest,self.root/'brief',runtime_path=runtime)

    def test_frozen_output_rejected(self):
        with self.assertRaisesRegex(ValueError,'outside production'):
            packet(self.manifest,'Daily:2609.12594',self.root/'frozen/new','worker')

    def test_changed_authority_rejected(self):
        job=self.job();result=self.result(job);self.manifest.write_text(json.dumps(self.data,indent=2))
        with self.assertRaisesRegex(ValueError,'manifest changed'):
            self.submit(job,result)

    def test_card_staged_needs_evidence_and_card(self):
        job=self.job();result=self.result(job);result['outcome']='card_staged'
        with self.assertRaisesRegex(ValueError,'needs card and evidence'):
            self.submit(job,result)

    def test_reported_item_is_not_requeued_or_accepted(self):
        job=self.job();self.submit(job,self.result(job))
        out=self.root/'brief'
        brief(self.manifest,out,receipts_dir=self.root)
        state=json.loads((out/'controller.json').read_text())
        self.assertEqual(state['preview'],[])
        self.assertEqual(state['reported_not_accepted']['count'],1)
        self.assertFalse(state['dispatch_authorized'])

    def test_stale_reported_result_rejected(self):
        job=self.job();self.submit(job,self.result(job))
        (job/'work/result.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'Changed packet/result'):
            brief(self.manifest,self.root/'brief',receipts_dir=self.root)

    def test_one_paper_intake_is_bound_to_frozen_queue(self):
        queue = self.root/'frozen/audit/candidates.json'
        queue.parent.mkdir()
        queue.write_text(json.dumps({'candidates': [
            {'arxiv_id': '2609.12594', 'reviewed_abstract': 'First abstract'},
            {'arxiv_id': '2609.99999', 'reviewed_abstract': 'Other paper secret'}]}))
        self.data['source_hashes'][str(queue)] = digest(queue)
        self.data['rows'][0]['run_state'] = 'pending_fulltext'
        self.save_manifest()
        intake_dir = self.root/'intakes'
        prepare(self.manifest, queue, ['2609.12594'], intake_dir)
        intake = intake_dir/'2609.12594.json'
        packet(self.manifest, 'Daily:2609.12594', self.root/'intake-job', 'worker', intake)
        self.assertNotIn('Other paper secret', intake.read_text())
        self.assertIn('intake', json.loads((self.root/'intake-job/packet.json').read_text())['existing_artifacts'])
        with self.assertRaisesRegex(ValueError, 'outside frozen'):
            prepare(self.manifest, queue, ['2609.12594'], self.root/'frozen/illegal-intake')
        queue.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'verified frozen input'):
            prepare(self.manifest, queue, ['2609.12594'], self.root/'intakes-2')

    def test_collection_packet_includes_catalog_site_instructions(self):
        catalog = self.root/'catalog'
        catalog.mkdir()
        (catalog/'AGENTS.md').write_text('Catalog publishing instructions')
        self.data['production']['catalog'] = dict(path=str(catalog), head='fixture')
        self.data['rows'] = [dict(key='Collection:2204.00887', program='Collection',
                                  arxiv_id='2204.00887', cohort='outside_original_collection_queue',
                                  next_action='resolve_identity', catalog_records=[])]
        self.save_manifest()
        packet(self.manifest, 'Collection:2204.00887', self.root/'collection-job', 'worker')
        job = json.loads((self.root/'collection-job/packet.json').read_text())
        self.assertIn(str(catalog/'AGENTS.md'), [x['path'] for x in job['instruction_files']])


if __name__ == '__main__':
    unittest.main()

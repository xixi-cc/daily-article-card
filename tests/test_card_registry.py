import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import card_registry as r
import card_workflow as w
from reconcile_card_resume import digest


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.registry=self.root/'registry'
        self.evidence=self.root/'evidence.json';self.evidence.write_text('{"fixture":true}')
        self.ref={'path':str(self.evidence),'sha256':digest(self.evidence)}
        r.record_many(self.registry,[])

    def row(self, **changes):
        return dict(dict(paper_id='2609.99991',program='Daily',status='not_selected',title='A Test Paper',
                         source_version='v1',reason='Reviewed; not S',evidence={'receipt':self.ref}),**changes)

    def test_identity_versions_doi_and_legacy(self):
        self.assertEqual(r.identity('https://arxiv.org/pdf/2609.99991v2.pdf'),('2609.99991','v2'))
        self.assertEqual(r.identity('https://doi.org/10.1103/PhysRevLett.135.187402'),('doi:10.1103/physrevlett.135.187402',None))
        self.assertEqual(r.identity('cond-mat-0702169'),('cond-mat/0702169',None))

    def test_duplicate_idempotent_and_version_query(self):
        self.assertEqual(r.record_many(self.registry,[self.row()]),1)
        self.assertEqual(r.record_many(self.registry,[self.row()]),0)
        self.assertEqual(r.lookup(self.registry,'2609.99991v1','Daily')['action'],'skip_previous_disposition')
        self.assertEqual(r.lookup(self.registry,'2609.99991v2','Daily')['action'],'changed_version_review_required')
        with self.assertRaisesRegex(ValueError,'blocks'):
            r.guard_claim(self.registry,'Daily:2609.99991','v2')

    def test_daily_lower_grade_does_not_reject_collection(self):
        r.record_many(self.registry,[self.row()])
        self.assertEqual(r.guard_claim(self.registry,'Collection:2609.99991')['action'],'review_other_program_evidence')

    def test_cross_program_source_issue_requires_review(self):
        r.record_many(self.registry,[self.row(status='source_exception')])
        with self.assertRaisesRegex(ValueError,'unresolved'):
            r.guard_claim(self.registry,'Collection:2609.99991')

    def test_title_conflict_and_doi_alias(self):
        r.record_many(self.registry,[self.row(),self.row(paper_id='2609.99992')])
        self.assertEqual(r.lookup(self.registry,title='a test paper')['action'],'identity_conflict')
        r.record_many(self.registry,[self.row(paper_id='doi:10.1234/test',program='Collection',status='has_card',aliases=['record-deadbeef'])])
        self.assertEqual(r.lookup(self.registry,'record-deadbeef','Collection')['action'],'reuse_existing_card')

    def test_db_is_append_only_and_event_collision_rolls_back(self):
        r.record_many(self.registry,[self.row(event_id='one')])
        with self.assertRaisesRegex(ValueError,'reused'):
            r.record_many(self.registry,[self.row(paper_id='2609.99992'),self.row(event_id='one',reason='different')])
        self.assertEqual(len(r.current(self.registry)),1)
        with r.connect(self.registry,create=True) as db:
            with self.assertRaises(sqlite3.IntegrityError):db.execute('DELETE FROM events')
            with self.assertRaises(sqlite3.IntegrityError):db.execute("UPDATE events SET payload='{}'")

    def test_changed_evidence_cannot_record(self):
        self.evidence.write_text('changed')
        with self.assertRaisesRegex(ValueError,'changed'):
            r.record_many(self.registry,[self.row()])

    def test_missing_registry_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'missing'):
            r.guard_claim(self.root/'missing','Daily:2609.99991')

    def test_current_public_card_overrides_stale_rejection(self):
        r.record_many(self.registry,[self.row()])
        repo=self.root/'repo';cards=repo/'data/curated_cards';cards.mkdir(parents=True)
        (cards/'2609.99991.json').write_text('{}')
        self.assertEqual(r.lookup(self.registry,'2609.99991','Daily',repo=repo)['action'],'reuse_existing_card')

    def test_export_separates_stopped_from_negative(self):
        r.record_many(self.registry,[self.row(),self.row(paper_id='2609.99992',status='stopped_unstarted')])
        summary=r.export(self.registry)
        self.assertEqual(summary['counts'],{'not_selected':1,'stopped_unstarted':1})
        self.assertTrue((self.registry/'no-card-current.md').exists())

    def test_parent_decision_required(self):
        p=self.root/'decision.json';p.write_text(json.dumps({'scientific_acceptance':False}))
        with self.assertRaisesRegex(ValueError,'parent-accepted'):r.accept_decision(self.registry,p)
        r.record_many(self.registry,[self.row()])
        receipt=self.root/'accepted-receipt.json';receipt.write_text(json.dumps({'key':'Daily:2609.99991'}))
        receipt_ref={'path':str(receipt),'sha256':digest(receipt)}
        p.write_text(json.dumps({'scientific_acceptance':True,'key':'Daily:2609.99991',
                                'decision':'accepted_source_exception','receipt':receipt_ref,'boundary':'Unclosed source proof.'}))
        self.assertEqual(r.accept_decision(self.registry,p),1)
        self.assertEqual(r.accept_decision(self.registry,p),0)
        self.assertEqual(r.current(self.registry)[0]['status'],'source_exception')
        r.record_many(self.registry,[self.row(status='has_card')])
        self.assertEqual(r.accept_decision(self.registry,p),0)
        self.assertEqual(r.current(self.registry)[0]['status'],'has_card')

    def test_worker_packet_blocks_before_writing(self):
        from card_context import packet
        r.record_many(self.registry,[self.row()])
        manifest=self.root/'manifest.json'
        manifest.write_text(json.dumps({'production':{'cards':{'path':str(self.root/'repo')}},
            'rows':[{'key':'Daily:2609.99991','program':'Daily','arxiv_id':'2609.99991'}]}))
        out=self.root/'new-worker'
        with self.assertRaisesRegex(ValueError,'blocks'):
            packet(manifest,'Daily:2609.99991',out,'worker',registry_path=self.registry)
        self.assertFalse(out.exists())

    def test_workflow_terminal_auto_records_and_recovers_idempotently(self):
        journal=self.root/'journal'
        w.initialize(journal,{'authority':{'scope':str(self.evidence)},'registry':str(self.registry),
            'rows':[{'key':'Daily:2609.99991','already_started':True,'source_version':'v1',
                     'title':'A Test Paper','artifacts':{'checkpoint':str(self.evidence)}}]})
        w.record(journal,'transition',{'key':'Daily:2609.99991','stage':'claimed','note':'Existing unit only','artifacts':{'receipt':str(self.evidence)}})
        w.record(journal,'transition',{'key':'Daily:2609.99991','stage':'not_selected','note':'Reviewed; below S','artifacts':{'receipt':str(self.evidence)}})
        self.assertEqual(r.current(self.registry)[0]['status'],'not_selected')
        self.assertEqual(w.sync_registry(journal)['added'],0)
        second=self.root/'second'
        w.initialize(second,{'authority':{'scope':str(self.evidence)},'registry':str(self.registry),
            'rows':[{'key':'Daily:2609.99991','already_started':True,'artifacts':{'checkpoint':str(self.evidence)}}]})
        with self.assertRaisesRegex(ValueError,'blocks'):
            w.record(second,'transition',{'key':'Daily:2609.99991','stage':'claimed','note':'Duplicate','artifacts':{'receipt':str(self.evidence)}})

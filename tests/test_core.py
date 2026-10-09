import tempfile
import unittest
from pathlib import Path
from core import Store, reward


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.sqlite3'
        self.store = Store(self.path)
        self.payload = dict(experience_level='beginner', learning_preference='example', device_type='mobile', answers=[1, 0, 1])

    def tearDown(self):
        self.temp.cleanup()

    def test_rule_and_manual_override(self):
        session = self.store.start(self.payload)
        self.assertEqual(session['ui_variant'], 'example')
        self.assertEqual(session['context']['diagnostic_score'], 100)
        changed = self.store.change_variant(session['session_id'], 'concise')
        self.assertEqual(changed['selection_method'], 'manual_preview')

    def test_low_score_gets_hint(self):
        self.payload['answers'] = [3, 2, 3]
        self.assertEqual(self.store.start(self.payload)['ui_variant'], 'hint')

    def test_completion_is_idempotent_and_persisted(self):
        sid = self.store.start(self.payload)['session_id']
        once = self.store.complete(sid, [1, 1, 1])
        twice = self.store.complete(sid, [1, 1, 1])
        self.assertEqual(once, twice)
        self.assertEqual(once['result']['reward'], 1)
        self.assertEqual(Store(self.path).get(sid), once)
        self.assertEqual(len(list(self.store.export_rows())), 1)
        with self.assertRaises(ValueError):
            self.store.complete(sid, [0, 0, 0])
        with self.assertRaises(ValueError):
            self.store.change_variant(sid, 'hint')

    def test_invalid_input_and_reward_limits(self):
        self.payload['answers'] = [True, 0, 1]
        with self.assertRaises(ValueError):
            self.store.start(self.payload)
        self.assertEqual(reward(0, 3, 0), 0)
        self.assertEqual(reward(0), 0.2)
        with self.assertRaises(ValueError):
            reward(4)

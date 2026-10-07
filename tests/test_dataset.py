import unittest
from dataset.generate import generate
from dataset.validate import validate_rows


class DatasetTests(unittest.TestCase):
    def test_reproducible_and_seed_changes_output(self):
        self.assertEqual(generate(100, 16), generate(100, 16))
        self.assertNotEqual(generate(100, 16), generate(100, 17))

    def test_bounds_and_coverage(self):
        rows = generate(1000)
        self.assertEqual(validate_rows(rows), [])
        self.assertEqual({r['ui_variant'] for r in rows}, {'hint', 'example', 'concise', 'challenge'})

    def test_corruption_is_detected(self):
        rows = generate(2)
        rows[0]['reward'] = 9
        rows[1]['learner_id'] = rows[0]['learner_id']
        self.assertEqual(len(validate_rows(rows)), 2)

    def test_no_empty_generation(self):
        with self.assertRaises(ValueError):
            generate(0)

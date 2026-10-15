import unittest

from linucb import LinUCB, VARIANTS


class LinUCBTests(unittest.TestCase):

    def setUp(self):
        self.model = LinUCB(alpha=0.8)
        self.context = {
            "experience_level": "beginner",
            "learning_preference": "hint",
            "device_type": "desktop",
            "diagnostic_score": 33.33,
        }

    def test_selects_a_valid_variant(self):
        result = self.model.select(self.context)

        self.assertIn(result["variant"], VARIANTS)
        self.assertEqual(result["method"], "linucb")
        self.assertEqual(len(result["scores"]), len(VARIANTS))

    def test_selection_contains_explanation(self):
        result = self.model.select(self.context)

        self.assertIn("predicted_reward", result)
        self.assertIn("exploration_bonus", result)
        self.assertIn("score", result)
        self.assertIn("LinUCB", result["reason"])

    def test_update_records_observation(self):
        self.model.update("hint", self.context, 0.8)

        self.assertEqual(self.model.counts["hint"], 1)
        self.assertEqual(self.model.counts["example"], 0)

    def test_update_changes_model(self):
        import copy
        before = copy.deepcopy(self.model.state())

        self.model.update("hint", self.context, 1.0)

        after = self.model.state()
        self.assertNotEqual(before["A"], after["A"])
        self.assertNotEqual(before["b"], after["b"])

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            self.model.update("unknown", self.context, 0.5)

    def test_invalid_reward_is_rejected(self):
        with self.assertRaises(ValueError):
            self.model.update("hint", self.context, 1.5)

    def test_model_state_can_be_restored(self):
        self.model.update("example", self.context, 0.75)

        restored = LinUCB(alpha=0.8, state=self.model.state())

        self.assertEqual(restored.counts, self.model.counts)
        self.assertEqual(restored.A, self.model.A)
        self.assertEqual(restored.b, self.model.b)

    def test_negative_alpha_is_rejected(self):
        with self.assertRaises(ValueError):
            LinUCB(alpha=-1)


if __name__ == "__main__":
    unittest.main()
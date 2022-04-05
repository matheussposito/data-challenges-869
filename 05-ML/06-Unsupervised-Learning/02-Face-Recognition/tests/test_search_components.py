from nbresult import ChallengeResultTestCase

class TestSearchComponents(ChallengeResultTestCase):
    def test_best_pc_number(self):
        self.assertGreaterEqual(self.result.best_pc, 200)
        self.assertLessEqual(self.result.best_pc, 300)

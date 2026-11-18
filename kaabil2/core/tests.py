from django.test import TestCase
from .scoring import calculate_role_fit, skill_gaps

class CareerScoringTests(TestCase):
    def test_perfect_fit(self):
        self.assertEqual(calculate_role_fit({1: 80, 2: 60}, {1: 80, 2: 60}), 100)
    def test_missing_skill_reduces_fit(self):
        self.assertLess(calculate_role_fit({1: 80}, {1: 20}), 100)
    def test_gap_is_reported(self):
        self.assertEqual(skill_gaps({1: 80}, {1: 30})[0]["gap"], 50)

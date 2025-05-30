import unittest
from cal import *
class TestCal(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum(2, 3), 5)
        self.assertEqual(sum(-1, 1), 0)
        self.assertEqual(sum(0, 0), 0)

    def test_minus(self):
        self.assertEqual(minus(5, 3), 2)
        self.assertEqual(minus(10, -5), 15)

    def test_umnoj(self):
        self.assertEqual(umnoj(3, 4), 12)
        self.assertEqual(umnoj(-2, 5), -10)
        self.assertEqual(umnoj(0, 100), 0)

    def test_delen(self):
        self.assertEqual(delen(10, 2), 5)
        self.assertAlmostEqual(delen(1, 3), 0.333333, places=6)

if __name__ == "__main__":
    unittest.main()
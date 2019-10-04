"""
Unit test file for plot_gtex.py
"""
import unittest
import plot_gtex

class TestParArray(unittest.TestCase):

    def test_linear_search_constant(self):

        L = [1, 2, 3, 4, 5, 6]
        r = plot_gtex.linear_search(3, L)
        self.assertEqual(r, 2) # the index where 3 occurs in L

    def test_linear_search_not_found(self):

        L = [1, 2, 3, 4, 5, 6]
        r = plot_gtex.linear_search(10, L)
        self.assertEqual(r, -1)

    def test_binary_search_constant(self):

        L = [(1, 1), (2, 2), (3, 3)]
        r = plot_gtex.binary_search(3, L)
        self.assertEqual(r, 3) # the index where 3 occurs in L

    def test_binary_search_not_found(self):

        L = [(1, 1), (2, 2), (3, 3)]
        r = plot_gtex.binary_search(10, L)
        self.assertEqual(r, -1)

if __name__ == '__main__':
    unittest.main()

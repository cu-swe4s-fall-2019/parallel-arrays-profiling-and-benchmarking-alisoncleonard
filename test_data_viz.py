"""
Unit test file for data_viz.py
"""
import unittest
import data_viz as dv

class TestMathLib(unittest.TestCase):

    def test_boxplot_out_file_type(self):
        L = [4, 6, 5, 9, 10, 3, 9]
        with self.assertRaises(ValueError) as ex:
            dv.boxplot(L, 'test.jpeg')
        message = 'Can not support file extension. Try .png instead'
        self.assertEqual(str(ex.exception), message)

    def test_histogram_out_file_type(self):
        L = [4, 6, 5, 9, 10, 3, 9]
        with self.assertRaises(ValueError) as ex:
            dv.histogram(L, 'test.jpeg')
        message = 'Can not support file extension. Try .png instead'
        self.assertEqual(str(ex.exception), message)

    def test_combo_out_file_type(self):
        L = [4, 6, 5, 9, 10, 3, 9]
        with self.assertRaises(ValueError) as ex:
            dv.combo(L, 'test.jpeg')
        message = 'Can not support file extension. Try .png instead'
        self.assertEqual(str(ex.exception), message)

if __name__ == '__main__':
    unittest.main()

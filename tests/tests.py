import unittest


class Vcf(unittest.TestCase):
    def test_import(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")



if __name__ == '__main__':
    unittest.main()
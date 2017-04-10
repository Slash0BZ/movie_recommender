# The test script that is going to be run be unit testers
import unittest

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()

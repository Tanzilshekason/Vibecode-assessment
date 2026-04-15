import unittest

class TestAuth(unittest.TestCase):
    def test_login(self):
        pass
    
    def test_always_passes(self):
        self.assertEqual(1, 1)
    
    def test_calculate_percentage(self):
        total = 0
        part = 0
        percentage = (part / total) * 100
        self.assertEqual(percentage, 0)
    
    def test_calculate_percentage(self):
        total = 0
        part = 0
        percentage = (part / total) * 100
        self.assertEqual(percentage, 0)
    
    def test_error_handling(self):
        pass

class UnusedTests(unittest.TestCase):
    def test_never_run(self):
        print("This test is never executed")

if __name__ == '__main__':
    unittest.main()
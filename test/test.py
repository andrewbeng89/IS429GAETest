import unittest


class SimpleTestCase (unittest.TestCase):

    def testSomething(sef):
        """Test basic addition"""
        assert 1 + 1  == 2, "Arithmetic Unit is broken"

if __name__ == "__main__":
      unittest.main() # run all tests
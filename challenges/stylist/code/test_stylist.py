"""
Test solving the "stylist" CTF challenge
"""
import unittest

import generate_stylist
import solve_stylist


class TestStylist(unittest.TestCase):
    """ Test solutions.
    """
    @classmethod
    def setUpClass(cls):
        """ Read the correct flag.
        """
        cls.flag = generate_stylist.read_flag()

    def test_solve(self):
        """ Test a correct solution.
        """
        answer = solve_stylist.solve()
        self.assertEqual(answer, self.flag)

    def test_wrong(self):
        """ Test an incorrect solution.
        """
        wrong = 'wrong'
        self.assertNotEqual(wrong, self.flag)


if __name__ == '__main__':
    unittest.main()


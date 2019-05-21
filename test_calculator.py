import calculator
import unittest
import doctest


class TestCalculator(unittest.TestCase):
    """Unit tests to check accuracy of calculator"""

    def test_format_numbers(self):
        """Test format_numbers function."""

        self.assertEqual(calculator.format_numbers(1000000), '$1,000,000.00')


    def test_calc_property_taxes(self):
        """Test calc_property_taxes function."""

        # Note: Need to keep an eye out for tests that should return formatted numbers
        self.assertEqual(calculator.calc_property_taxes(1000000), '$1,000.00')


    def test_calc_ho_ins(self):
        """Test calc_ho_ins function."""

        self.assertEqual(calculator.calc_ho_ins(1000000), '$3,500.00')

    def test_calc_mortgage(self):
        """Test calc_mortgage function."""

        self.assertEqual(calculator.calc_mortgage(1000000, 200000), 4053.482478607086)


    def test_calc_mo_salary(self):
        """Test calc_mo_salary function."""

        self.assertEqual(calculator.calc_mo_salary(120000), 10000)


    def test_rule_36(self):
        """Test rule_36 function."""

        self.assertEqual(calculator.rule_36(5000, 500), 1300.0)


# def load_tests(loader, tests, ignore): 
#     """Also run our doctests and file-based doctests.

#     This function name, ``load_tests``, is required.
#     """

#     tests.addTests(doctest.DocTestSuite(arithmetic))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()

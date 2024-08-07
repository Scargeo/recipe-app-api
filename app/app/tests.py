"""
sample tests
"""

from django.test import SimpleTestCase
from . import calc


class CalcTests(SimpleTestCase):

    """Test the calculator module."""
    def text_add_numbers(self):
        """Test adding numbers together."""
        res = calc.add(5, 7)

        self.assertEqual(res, 12)

    def test_subtract_numbers(self):
        """Test subtracting numbers."""

        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)

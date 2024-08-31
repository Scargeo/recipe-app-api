"""
Test custom Django management commands.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# mocking the behaviour
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database """
        patched_check.return_value = True

        # execute the command in the wait_for_db
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

        @patch("time.sleep")
        def test_wait_for_db_delay(self, patched_sleep, patched_check):
            """Test waiting for database to get OperationalError"""
            """The side effect allows you to pass in exception  """
            patched_check.side_effect = [Psycopg2Error] * 3 + \
                [OperationalError] * 5 * [True]

            call_command("wait_for_db")

            self.assertEqual(patched_check.call_count, 5)
            patched_check.assert_called_once_with(databases=['default'])


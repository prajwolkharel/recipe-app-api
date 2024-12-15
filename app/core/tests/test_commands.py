from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready."""
        patched_check.return_value = True  # Mock the database as ready
        call_command('wait_for_db')  # Run the custom management command

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error."""
        # Mock the `check` method to simulate connection issues, then success
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # Run the custom management command
        call_command('wait_for_db')

        # Ensure the check method was called 6 times
        self.assertEqual(patched_check.call_count, 6)

        # Ensure the check method was called with the 'default' database
        patched_check.assert_called_with(databases=['default'])

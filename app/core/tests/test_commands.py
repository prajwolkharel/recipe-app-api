"""
Test custom Django management commands.
"""
from unittest.mock import patch
# Import `patch` from `unittest.mock` to mock specific parts of the code during testing.
# In this case, we are mocking the `check` method of the `wait_for_db` management command.

from psycopg2 import OperationalError as Psycopg2Error
# Import `OperationalError` from the `psycopg2` library, which is commonly raised by PostgreSQL
# when a connection to the database cannot be made (e.g., database is down or not responding).

from django.core.management import call_command
# Import `call_command` to invoke Django management commands programmatically within the tests.

from django.db.utils import OperationalError
# Import `OperationalError` from `django.db.utils` to simulate database operational errors during the test.

from django.test import SimpleTestCase
# Import `SimpleTestCase` from Django's test framework for testing code that doesn't require a database.
# `SimpleTestCase` is typically used for unit tests where the database is not required, and it's faster for tests that don't involve database interactions.

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready."""
        # This test case checks the behavior of the `wait_for_db` management command when the database is ready.

        # Mock the behavior of `check` method to return `True` immediately, indicating that the database is ready.
        patched_check.return_value = True

        # Call the custom management command `wait_for_db` to simulate the command being executed.
        call_command('wait_for_db')

        # Assert that the `check` method was called exactly once with the 'default' database.
        # The `check` method is responsible for checking the database connection and determining if the database is up.
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error."""
        # This test case ensures that the `wait_for_db` command correctly retries when the database is not yet available.

        # Mock the `check` method to raise `Psycopg2Error` and `OperationalError` multiple times,
        # simulating a scenario where the database is not initially available and we need to retry.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # The `side_effect` defines a sequence of exceptions to be raised by the `check` method during successive calls.
        # First, two `Psycopg2Error` exceptions are raised, followed by three `OperationalError` exceptions,
        # and finally, `True` is returned to indicate the database is ready.

        # Call the `wait_for_db` management command to simulate the wait operation.
        call_command('wait_for_db')

        # Assert that the `check` method was called exactly 6 times (2 times for `Psycopg2Error`, 3 for `OperationalError`, and 1 time for `True`).
        self.assertEqual(patched_check.call_count, 6)

        # Ensure that the `check` method was called with the 'default' database each time.
        patched_check.assert_called_with(databases=['default'])

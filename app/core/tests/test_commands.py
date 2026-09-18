"""
Test custom Django management commands.
"""
from unittest.mock import patch  # To Mock the behaviour of DB
# Its one of the possibilities of error we might get
from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command  # Helper function for testing
from django.db.utils import OperationalError  # Another error we might get
from django.test import SimpleTestCase  # Lib to test the unit Test


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_delay_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationlError"""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

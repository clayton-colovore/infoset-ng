#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
_test_directory = os.path.dirname(os.path.realpath(__file__))
_lib_directory = os.path.abspath(os.path.join(_test_directory, os.pardir))
_root_directory = os.path.abspath(os.path.join(_lib_directory, os.pardir))
if _test_directory.endswith('/infoset-ng/infoset/test') is True:
    sys.path.append(_root_directory)
else:
    print(
        'This script is not installed in the "infoset-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

from infoset.api import API
from infoset.test import unittest_setup


class APITestCase(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    def setUp(self):
        """Setup the environment prior to testing."""
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_index(self):
        """Testing method / function index."""
        # Initializing key variables
        expected = b'Infoset API v1.0 Operational.\n'
        response = self.API.get('/infoset/api/v1/status')

        # Verify reponses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()

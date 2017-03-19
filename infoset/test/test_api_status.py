#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
_TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_LIB_DIRECTORY = os.path.abspath(os.path.join(_TEST_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_LIB_DIRECTORY, os.pardir))
if _TEST_DIRECTORY.endswith('/infoset-ng/infoset/test') is True:
    sys.path.append(_ROOT_DIRECTORY)
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

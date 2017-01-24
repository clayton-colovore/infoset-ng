#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest

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

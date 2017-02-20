#!/usr/bin/env python3
"""Test the db_device library in the infoset.db module."""

import unittest
import json
from pprint import pprint

from infoset.api import API, CACHE
from infoset.db import db_device
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class APITestCase(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['values'] = database.values()
    expected['idx_device'] = database.idx_device()

    # Retrieve data
    test_object = db_device.GetIDXDevice(expected['idx_device'])

    def setUp(self):
        """Setup the environment prior to testing."""
        # Test mode
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_lastcontacts_1(self):
        """Testing method / function lastcontacts."""
        # Clear the memory cache
        CACHE.clear()

        # Initialize key variables
        precision = 5

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts?secondsago=3600'
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        print('\n')
        pprint(self.expected['values'])
        print('\n')
        pprint(result)
        print('\n')

        # Convert the list of expected values to an easy to compare dict
        check_dict = {}
        for item in self.expected['values']:
            check_dict[str(item['timestamp'])] = item['value']

        # Verify the expected data is there
        for timestamp, value in sorted(result.items()):
            if timestamp in check_dict:
                self.assertEqual(
                    round(result[timestamp], precision),
                    round(check_dict[timestamp], precision))
            else:
                self.assertEqual(value, 0)

    def test_lastcontacts_2(self):
        """Testing method / function lastcontacts."""
        # Clear the memory cache
        CACHE.clear()

        # Initializing key variables
        pass

    def test_id_agents(self):
        """Testing method / function id_agents."""
        # Clear the memory cache
        CACHE.clear()

        # Initializing key variables
        pass

    def test_deviceagents(self):
        """Testing method / function deviceagents."""
        # Clear the memory cache
        CACHE.clear()

        # Initializing key variables
        pass

    def test_devicename_agents(self):
        """Testing method / function devicename_agents."""
        # Clear the memory cache
        CACHE.clear()

        # Initializing key variables
        pass

    def test__start_timestamp(self):
        """Testing method / function _start_timestamp."""
        # Clear the memory cache
        CACHE.clear()

        # Initializing key variables
        pass


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()

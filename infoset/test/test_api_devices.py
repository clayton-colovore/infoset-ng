#!/usr/bin/env python3
"""Test the db_device library in the infoset.db module."""

import unittest
import json

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
    expected['idx_device'] = database.idx_device()
    expected['idx_agent'] = database.idx_agent()

    # Retrieve data
    test_object = db_device.GetIDXDevice(expected['idx_device'])

    def setUp(self):
        """Setup the environment prior to testing."""
        # Test mode
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_db_getidxdevice(self):
        """Testing method / function db_getidxdevice."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/devices/{}'.format(self.expected['idx_device'])
        )
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(result, dict), True)
        self.assertEqual(result['description'], self.test_object.description())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())
        self.assertEqual(result['idx_device'], self.test_object.idx_device())
        self.assertEqual(
            result['devicename'], self.test_object.devicename())

        # Test the number and names of keys
        keys = [
            'idx_device', 'devicename', 'description', 'enabled', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_db_deviceagent_indices(self):
        """Testing method / function db_deviceagent_agentindices."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/devices/{}/agents'
            ''.format(self.expected['idx_device'])
        )
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, [self.expected['idx_agent']])


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()

#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest
import json
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

from infoset.api import API, CACHE
from infoset.db import db_agent
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
    expected['idx_agent'] = database.idx_agent()
    expected['id_agent'] = database.id_agent()

    # Retrieve data
    test_object = db_agent.GetIDXAgent(expected['idx_agent'])

    def setUp(self):
        """Setup the environment prior to testing."""
        # Test mode
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_agents(self):
        """Testing method / function agents."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/agents/{}'.format(self.expected['idx_agent'])
        )
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(result, dict), True)
        self.assertEqual(result['id_agent'], self.test_object.id_agent())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())
        self.assertEqual(result['idx_agent'], self.test_object.idx_agent())
        self.assertEqual(
            result['idx_agentname'], self.test_object.idx_agentname())
        self.assertEqual(result['agent'], self.test_object.agent())

        # Test the number and names of keys
        keys = [
            'idx_agent', 'idx_agentname', 'id_agent',
            'enabled', 'agent', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_agents_query(self):
        """Testing method / function agents_query."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        response = self.API.get('/infoset/api/v1/agents')
        data = json.loads(response.get_data(as_text=True))
        result = data[0]

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(result['id_agent'], self.test_object.id_agent())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())
        self.assertEqual(result['idx_agent'], self.test_object.idx_agent())
        self.assertEqual(
            result['idx_agentname'], self.test_object.idx_agentname())
        self.assertEqual(result['agent'], self.test_object.agent())

        # Test the number and names of keys
        keys = [
            'idx_agent', 'idx_agentname', 'id_agent',
            'enabled', 'agent', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_agents_query_2(self):
        """Testing method / function agents_query."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/agents?id_agent={}'
            ''.format(self.expected['id_agent']))
        response = self.API.get(uri)
        data = json.loads(response.get_data(as_text=True))
        result = data[0]

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(result['id_agent'], self.test_object.id_agent())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())
        self.assertEqual(result['agent'], self.test_object.agent())

        # Test the number and names of keys
        keys = [
            'idx_agent', 'idx_agentname', 'id_agent',
            'enabled', 'agent', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()

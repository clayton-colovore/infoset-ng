#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest
import json

from infoset.api import API
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

    # Retrieve data
    good_agent = db_agent.GetIDXAgent(expected['idx_agent'])

    def setUp(self):
        """Setup the environment prior to testing."""
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_agents(self):
        """Testing method / function agents."""
        # Initializing key variables
        response = self.API.get(
            '/infoset/api/v1/agents/{}'.format(self.expected['idx_agent']))
        data = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, dict), True)
        self.assertEqual(data['id_agent'], self.good_agent.id_agent())
        self.assertEqual(data['exists'], self.good_agent.exists())
        self.assertEqual(data['enabled'], self.good_agent.enabled())
        self.assertEqual(data['idx_agent'], self.good_agent.idx_agent())
        self.assertEqual(
            data['idx_agentname'], self.good_agent.idx_agentname())
        self.assertEqual(data['name'], self.good_agent.name())

    def test_agents_query(self):
        """Testing method / function agents_query."""
        # Initializing key variables
        response = self.API.get('/infoset/api/v1/agents')
        data = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(data[0]['id_agent'], self.good_agent.id_agent())
        self.assertEqual(data[0]['exists'], self.good_agent.exists())
        self.assertEqual(data[0]['enabled'], self.good_agent.enabled())


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()

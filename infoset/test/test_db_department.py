#!/usr/bin/env python3
"""Test the db_department library in the infoset.db module."""

import unittest

from infoset.db import db_department
from infoset.test import unittest_db


class TestGetIDXDepartment(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database
    expected = unittest_db.setup_db_department()

    # Retrieve data
    good_agent = db_department.GetIDXDepartment(expected['idx_department'])

    def test_init_(self):
        """Testing method init."""
        # Test with non existent AgentIDX
        record = db_department.GetIDXDepartment(-1)
        self.assertEqual(record.exists(), False)

    def test_idx_department(self):
        """Testing method idx_department."""
        # Testing with known good value
        result = self.good_agent.idx_department()
        self.assertEqual(result, self.expected['idx_department'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_department()
        self.assertNotEqual(result, expected)

    def test_name(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_code(self):
        """Testing method code."""
        # Testing with known good value
        result = self.good_agent.code()
        self.assertEqual(result, self.expected['code'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.code()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_enabled(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)


class TestGetCodeDepartment(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database
    expected = unittest_db.setup_db_department()

    # Retrieve data
    good_agent = db_department.GetCodeDepartment(expected['code'])

    def test_init_getcode(self):
        """Testing method __init__."""
        # Test with non existent AgentID
        record = db_department.GetCodeDepartment('bogus')
        self.assertEqual(record.exists(), False)

    def test_idx_department(self):
        """Testing method idx_department."""
        # Testing with known good value
        result = self.good_agent.idx_department()
        self.assertEqual(result, self.expected['idx_department'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_department()
        self.assertNotEqual(result, expected)

    def test_name(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_code(self):
        """Testing method code."""
        # Testing with known good value
        result = self.good_agent.code()
        self.assertEqual(result, self.expected['code'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.code()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_enabled(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database
    expected = unittest_db.setup_db_department()

    def test_code_exists(self):
        """Testing function code_exists."""
        # Testing with known good value
        expected = True
        result = db_department.code_exists(self.expected['code'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_department.code_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_department_exists(self):
        """Testing function idx_department_exists."""
        # Testing with known good value
        expected = True
        result = db_department.idx_department_exists(
            self.expected['idx_department'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_department.idx_department_exists(None)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()

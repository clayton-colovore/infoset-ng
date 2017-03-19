#!/usr/bin/env python3
"""Class used to set test configuration used by unittests."""

# Standard imports
import sys
import os

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

# Infoset libraries
try:
    from infoset.test import unittest_setup
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)


def main():
    """Create test configurations."""
    # Check environment
    config = unittest_setup.TestConfig()
    config.create()


if __name__ == '__main__':
    # Do the unit test
    main()

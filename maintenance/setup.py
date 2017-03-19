#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import sys
import os

# PIP3 imports
try:
    import yaml
    from sqlalchemy import create_engine
except ImportError:
    import pip
    packages = ['PyYAML', 'sqlalchemy']
    for package in packages:
        pip.main(['install', '--user', package])
    print(
        'New Python packages installed. Please run this script again to '
        'complete the Infoset-NG installation.')
    sys.exit(0)

# Try to create a working PYTHONPATH
_maint_directory = os.path.dirname(os.path.realpath(__file__))
_root_directory = os.path.abspath(
    os.path.join(_maint_directory, os.pardir))
if _root_directory.endswith('/infoset-ng') is True:
    sys.path.append(_root_directory)
else:
    print(
        'Infoset-NG is not installed in a "infoset-ng/" directory. '
        'Please fix.')
    sys.exit(2)

# Infoset libraries
from maintenance import _setup

if __name__ == '__main__':
    # Run setup
    _setup.run()

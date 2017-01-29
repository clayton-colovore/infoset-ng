#! /usr/bin/env python3
"""infoset-ng api tester."""

# Standard imports
import sys
import os

# Try to create a working PYTHONPATH
script_directory = os.path.dirname(os.path.realpath(__file__))
bin_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
root_directory = os.path.abspath(os.path.join(bin_directory, os.pardir))
if script_directory.endswith('/infoset-ng/bin/tools') is True:
    sys.path.append(root_directory)
else:
    print(
        'This script is not installed in the "infoset-ng/bin/tools" '
        'directory. Please fix.')
    sys.exit(2)

# Infoset-ng imports
try:
    from infoset.utils import configuration
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.api import API


def main():
    """Get Flask server running.

    Args:
        None

    Returns:
        None

    """
    # Start
    config = configuration.Config()
    bind_port = config.bind_port()
    listen_address = config.listen_address()
    API.run(debug=True, host=listen_address, threaded=True, port=bind_port)


if __name__ == '__main__':
    main()

#! /usr/bin/env python3
"""infoset-ng api."""

# Standard imports
import sys

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

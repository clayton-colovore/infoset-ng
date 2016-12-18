#!/usr/bin/env python3

"""Infoset WSGI script.

Serves as a Gunicorn WSGI entry point for infoset.api.api.py

"""

# Standard libraries
import sys

# Infoset libraries
try:
    from infoset.api.api import API
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)


if __name__ == '__main__':
    # Start
    API.run()

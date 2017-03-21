#!/usr/bin/env python3
"""infoset  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import os

# Try to create a working PYTHONPATH
_MAINT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(
    os.path.join(_MAINT_DIRECTORY, os.pardir))
if _ROOT_DIRECTORY.endswith('/infoset-ng') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'Infoset-NG is not installed in a "infoset-ng/" directory. '
        'Please fix.')
    sys.exit(2)


def run():
    """Do the installation.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    scripts = ['prerequisites.py', 'setup.py', 'finalize.py']

    # Continue
    for script in scripts:
        executable = 'python3 {}/{}'.format(_MAINT_DIRECTORY, script)
        returncode = os.system(executable)
        if bool(returncode) is True:
            sys.exit(2)

    # End normally
    sys.exit(0)


if __name__ == '__main__':
    # Run main
    run()

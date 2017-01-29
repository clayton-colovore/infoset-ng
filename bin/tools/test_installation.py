#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import sys
import os
from random import randint
from collections import defaultdict

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

# Infoset libraries
try:
    from infoset.reference import reference
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import log


def data2post():
    """Generate data to post.

    Args:
        None

    Returns:
        None

    """
    # Generate fake data
    result = defaultdict(lambda: defaultdict(dict))
    labels = ['_infoset_test_1_', '_infoset_test_2_']
    sources = ['_source_1_', '_source_2_']
    for label in labels:
        for source in sources:
            result[label][source] = randint(5, 10)

    # Return
    return result


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    config = reference.ReferenceSampleConfig()
    api = reference.ReferenceSampleAPI(config)
    agent_name = config.agent_name()
    devicename = config.prefix
    id_agent = reference.get_id_agent(agent_name, test=True)

    # Instantiate an agent
    report = reference.ReferenceSampleAgent(config, devicename, test=True)

    # Populate data and post
    report.populate_dict(data2post())
    success = report.post()

    # Posting success
    if success is True:
        # Log success
        log_message = (
            'Successfully posted test data for agent ID %s'
            '') % (id_agent)
        log.log2see(1015, log_message)

        # Try to retrieve data
        uri = ('/agents?id_agent=%s') % (id_agent)
        results = api.get(uri)

        if bool(results) is True:
            if isinstance(results, dict) is True:
                # print results
                if results['exists'] is True:
                    log_message = (
                        'Successfully retrieved test data for agent ID %s'
                        '') % (id_agent)
                    log.log2see(1034, log_message)
                    print('\nOK\n')
                else:
                    log_message = (
                        'WARNING: Contacted this infoset server. '
                        'The data for the test agent ID %s is not present '
                        'in the database. Ingester has not added agent to '
                        'the database'
                        '') % (id_agent)
                    log.log2see(1035, log_message)
                    print("""\
OK, but Ingester has not updated the database yet. \
Run test in a minute and this message should change. \
If not, the Ingester may not be running.
""")
            else:
                log_message = (
                    'Failed to retrieve posted data to the local infoset '
                    'server. Review the installation steps '
                    'and verify whether the API is running.')
                log.log2die(1039, log_message)
                print('\nFail\n')

        else:
            log_message = (
                'Failed to retrieve posted data to the local infoset '
                'server. Review the installation steps '
                'and verify whether the API is running.')
            log.log2die(1039, log_message)
            print('\nFail\n')

    else:
        log_message = (
            'Failed to post data to the local infoset server. '
            'Review the installation steps '
            'and verify whether the API is running.')
        log.log2die(1039, log_message)
        print('\nFail\n')


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""Infoset ingest cache daemon.

Extracts agent data from cache directory files.

"""

# Standard libraries
import sys
from random import randint
from collections import defaultdict

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
        uri = ('db/agent/getidagent/%s') % (id_agent)
        results = api.get(uri)

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
            print('\nOK - Ingester not running\n')
    else:
        log_message = (
            'Failed to post data to the local infoset server. '
            'Review the installation steps '
            'and verify whether the API is running.')
        log.log2die(1039, log_message)
        print('\nFail\n')


if __name__ == "__main__":
    main()

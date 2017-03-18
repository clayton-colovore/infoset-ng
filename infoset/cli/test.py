#!/usr/bin/env python3
"""infoset CLI classes for 'test'.

Functions to test ingester

"""

# Main python libraries
import sys
from collections import defaultdict
from random import randint

# Infoset-NG imports
from infoset.utils import general
from infoset.utils import log
from infoset.reference import reference


def run(args):
    """Process 'test' command.

    Args:
        parser: Argparse parser
        args: Argparse arguments

    Returns:
        None

    """
    if args.action == 'test':
        # Get configuration
        config = reference.ReferenceSampleConfig()
        api = reference.ReferenceSampleAPI(config)
        agent_name = config.agent_name()
        devicename = config.prefix
        id_agent = reference.get_id_agent(agent_name, test=True)

        # Instantiate an agent
        report = reference.ReferenceSampleAgent(config, devicename, test=True)

        # Populate data and post
        report.populate_dict(_data2post())
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
                        log.log2see(1132, log_message)
                        print('\nOK\n')
                    else:
                        log_message = (
                            'WARNING: Contacted this infoset server. '
                            'The data for the test agent ID %s is not present '
                            'in the database. Ingester has not added agent to '
                            'the database'
                            '') % (id_agent)
                        log.log2see(1133, log_message)
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
                    log.log2die(1140, log_message)
                    print('\nFail\n')

            else:
                log_message = (
                    'Failed to retrieve posted data to the local infoset '
                    'server. Review the installation steps '
                    'and verify whether the API is running.')
                log.log2die(1141, log_message)
                print('\nFail\n')

        else:
            log_message = (
                'Failed to post data to the local infoset server. '
                'Review the installation steps '
                'and verify whether the API is running.')
            log.log2die(1142, log_message)
            print('\nFail\n')

            # Exit OK
            sys.exit(0)
    else:
        # Show help if there are no matches
        general.cli_help()


def _data2post():
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

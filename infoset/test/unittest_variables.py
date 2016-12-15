#!/usr/bin/env python3
"""Class used to set global variables used by unittests."""


class TestVariables(object):
    """Checks all functions and methods."""

    def __init__(self):
        """Method initializing the class."""
        # Initialize key variables
        self.data = {}

        # Data used for testing cache validation
        self.data['cache_data'] = {
            'agent': 'unittest',
            'timeseries': {
                'cpu_count': {'base_type': 1,
                              'data': [[0, 2, None]],
                              'description': 'CPU Count'},
                'packets_recv': {'base_type': 64,
                                 'data': [['lo', 304495689, 'lo'],
                                          ['p10p1', 84319802, 'p10p1']],
                                 'description': 'Packets (In)'},
                'packets_sent': {'base_type': 64,
                                 'data': [['lo', 304495689, 'lo'],
                                          ['p10p1',
                                           123705549, 'p10p1']],
                                 'description': 'Packets (Out)'},
                'swap_used': {'base_type': 1,
                              'data': [[None, 363606016, None]],
                              'description': 'Swap Used'}},
            'devicename': 'unittest_device',
            'id_agent': 'a0810e3e36c59ea3cbdab599dcdb8'
                        '24fb468314b7340543493271ad',
            'timefixed': {
                'distribution': {'base_type': None,
                                 'data': [[0, 'Ubuntu 16.04 xenial', None]],
                                 'description': 'Linux Distribution'},
                'version': {'base_type': None,
                            'data': [[0, '#62-Ubuntu SMP', None]],
                            'description': 'Kernel Type'}},
            'timestamp': 1481561700}

    def cache_data(self):
        """Drop database if exists."""
        # Initialize key variables
        result = self.data['cache_data']
        return result

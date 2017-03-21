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
    import pymysql
except ImportError:
    import pip
    _PACKAGES = ['PyYAML', 'sqlalchemy', 'pymysql']
    for _PACKAGE in _PACKAGES:
        pip.main(['install', '--user', _PACKAGE])
    print(
        'New Python packages installed. Please run this script again to '
        'complete the Infoset-NG installation.')
    # Must exit abnormally as the script didn't complete
    sys.exit(2)

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

# Infoset libraries
from infoset.utils import log
from infoset.utils import configuration
from infoset.utils import general
from infoset.db.db_orm import BASE, Agent, Department, Device, Billcode
from infoset.db.db_orm import Configuration, DeviceAgent, Datapoint, AgentName
from infoset.db import URL
from infoset.db import db_configuration
from infoset.db import db_billcode
from infoset.db import db_department
from infoset.db import db_device
from infoset.db import db_agent
from infoset.db import db_agentname
from infoset.db import db_deviceagent
from infoset.db import db_datapoint
from infoset.db import db
from maintenance import misc


class _DatabaseSetup(object):
    """Class to setup database."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.reserved = '_SYSTEM_RESERVED_'
        self.config = configuration.Config()

    def _insert_datapoint(self):
        """Insert first datapoint in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_datapoint.idx_datapoint_exists(1) is False:
            record = Datapoint(
                id_datapoint=general.encode(self.reserved),
                agent_label=general.encode(self.reserved),
                agent_source=general.encode(self.reserved)
            )
            database = db.Database()
            database.add(record, 1047)

    def _insert_department(self):
        """Insert first department in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_department.idx_department_exists(1) is False:
            record = Department(
                code=general.encode(self.reserved),
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1102)

    def _insert_billcode(self):
        """Insert first billcode in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_billcode.idx_billcode_exists(1) is False:
            record = Billcode(
                code=general.encode(self.reserved),
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1104)

    def _insert_agent_device(self):
        """Insert first agent and device in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agentname = 1
        idx_agent = 1
        idx_device = 1

        # Add agent name
        if db_agentname.idx_agentname_exists(idx_agentname) is False:
            # Generate a name add a record in the database
            record = AgentName(
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1019)

        # Add agent
        if db_agent.idx_agent_exists(idx_agent) is False:
            # Generate an Agent ID and add a record in the database
            record = Agent(id_agent=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1109)

        # Add device
        if db_device.idx_device_exists(idx_device) is False:
            record = Device(
                description=general.encode(self.reserved),
                devicename=general.encode(self.reserved)
            )
            database = db.Database()
            database.add(record, 1106)

        # Add to Agent / Device table
        if db_deviceagent.device_agent_exists(idx_device, idx_agent) is False:
            record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1107)

    def _insert_config(self):
        """Insert first config in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        key_values = [('version', '0.0.0.0')]

        # Cycle through all the key value pairs
        for item in key_values:
            key = item[0]
            value = item[1]

            # Check if value exists and insert if not
            if db_configuration.config_key_exists(key) is False:
                record = Configuration(
                    config_key=general.encode(key),
                    config_value=general.encode(value))
                database = db.Database()
                database.add(record, 1108)

    def run(self):
        """Setup database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        use_mysql = True
        pool_size = 25
        max_overflow = 25
        config = self.config

        # Create DB connection pool
        if use_mysql is True:
            # Add MySQL to the pool
            engine = create_engine(
                URL, echo=True,
                encoding='utf8',
                max_overflow=max_overflow,
                pool_size=pool_size, pool_recycle=3600)

            # Try to create the database
            misc.print_ok('Attempting to create database tables')
            try:
                sql_string = (
                    'ALTER DATABASE %s CHARACTER SET utf8mb4 '
                    'COLLATE utf8mb4_general_ci') % (config.db_name())
                engine.execute(sql_string)
            except:
                log_message = (
                    'Cannot connect to database %s. '
                    'Verify database server is started. '
                    'Verify database is created. '
                    'Verify that the configured database authentication '
                    'is correct.') % (config.db_name())
                log.log2die(1046, log_message)

            # Apply schemas
            misc.print_ok('Applying Schemas.')
            BASE.metadata.create_all(engine)

            # Insert database entries
            self._insert_agent_device()
            self._insert_billcode()
            self._insert_department()
            self._insert_datapoint()
            self._insert_config()


def run():
    """Setup infoset-ng.

    Args:
        None

    Returns:
        None

    """
    # Run server setup
    _DatabaseSetup().run()

    # All done
    misc.print_ok('Database installation successful.')

    # End normally
    sys.exit(0)

    
if __name__ == '__main__':
    # Run setup
    run()

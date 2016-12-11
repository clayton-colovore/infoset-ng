#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import sys
from pathlib import Path

# Pip3 libraries
from sqlalchemy import create_engine

# Infoset libraries
try:
    from infoset.utils import log
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)
from infoset.utils import configuration
from infoset.utils import general
import infoset.utils
from infoset.db.db_orm import BASE, Agent, Department, Device, Billcode
from infoset.db.db_orm import Configuration, DeviceAgent, Datapoint
from infoset.db import URL
from infoset.db import db_configuration
from infoset.db import db_billcode
from infoset.db import db_department
from infoset.db import db_device
from infoset.db import db_agent
from infoset.db import db_deviceagent
from infoset.db import db_datapoint
from infoset.db import db


def insert_datapoint():
    """Insert first datapoint in the database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    reserved = '_SYSTEM_RESERVED_'

    # Insert
    if db_datapoint.idx_datapoint_exists(1) is False:
        record = Datapoint(
            id_datapoint=general.encode(reserved),
            agent_label=general.encode(reserved),
            agent_source=general.encode(reserved)
        )
        database = db.Database()
        database.add(record, 1011)


def insert_department():
    """Insert first department in the database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    reserved = '_SYSTEM_RESERVED_'

    # Insert
    if db_department.idx_department_exists(1) is False:
        record = Department(
            code=general.encode(reserved),
            name=general.encode(reserved))
        database = db.Database()
        database.add(record, 1102)


def insert_billcode():
    """Insert first billcode in the database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    reserved = '_SYSTEM_RESERVED_'

    # Insert
    if db_billcode.idx_billcode_exists(1) is False:
        record = Billcode(
            code=general.encode(reserved),
            name=general.encode(reserved))
        database = db.Database()
        database.add(record, 1104)


def insert_agent_device():
    """Insert first agent and device in the database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    reserved = '_SYSTEM_RESERVED_'
    idx_agent = 1
    idx_device = 1

    # Add agent
    if db_agent.idx_agent_exists(idx_agent) is False:
        # Generate a UID and add a record in the database
        record = Agent(
            id_agent=general.encode(reserved),
            name=general.encode(reserved))
        database = db.Database()
        database.add(record, 1109)

    # Add device
    if db_device.idx_device_exists(idx_device) is False:
        record = Device(
            description=general.encode(reserved),
            devicename=general.encode(reserved)
        )
        database = db.Database()
        database.add(record, 1106)

    # Add to Agent / Device table
    if db_deviceagent.device_agent_exists(idx_device, idx_agent) is False:
        record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
        database = db.Database()
        database.add(record, 1107)


def insert_config():
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


def server_setup():
    """Setup server.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True
    pool_size = 25
    max_overflow = 25

    # Get configuration
    config = configuration.Config()

    # Create DB connection pool
    if use_mysql is True:
        # Add MySQL to the pool
        engine = create_engine(
            URL, echo=True,
            encoding='utf8',
            max_overflow=max_overflow,
            pool_size=pool_size, pool_recycle=3600)

        # Try to create the database
        print('Attempting to create database tables')
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
            log.log2die(1036, log_message)

        # Apply schemas
        print('Applying Schemas')
        BASE.metadata.create_all(engine)

        # Insert database entries
        insert_agent_device()
        insert_billcode()
        insert_department()
        insert_datapoint()
        insert_config()


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Run server setup
    server_setup()

    # Install required PIP packages
    print('Installing required pip3 packages')
    pip3 = infoset.utils.general.search_file('pip3')
    if pip3 is None:
        log_message = ('Cannot find python "pip3". Please install.')
        log.log2die(1052, log_message)

    utils_directory = infoset.utils.__path__[0]
    requirements_file = ('%s/requirements.txt') % (
        Path(utils_directory).parents[1])
    script_name = (
        'pip3 install --user --upgrade --requirement %s'
        '') % (requirements_file)
    infoset.utils.general.run_script(script_name)


if __name__ == '__main__':
    main()

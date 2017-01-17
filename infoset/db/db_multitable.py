"""Module of infoset database functions.

Handles queries that span multiple tables.

"""

# PIP libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.utils import general
from infoset.db.db_orm import Datapoint, Device, Agent, DeviceAgent


def datapoint_summary():
    """Get summary datapoint information.

    Args:
        None

    Returns:
        data: list of dicts

    """
    # Initialize key variables
    data_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()

    # Get result of query
    rows = session.query(
        Datapoint.idx_datapoint,
        Datapoint.agent_label,
        Datapoint.agent_source,
        DeviceAgent.idx_deviceagent,
        Agent.id_agent,
        Agent.name,
        Device.devicename).filter(
            and_(
                Datapoint.idx_deviceagent == DeviceAgent.idx_deviceagent,
                Agent.idx_agent == DeviceAgent.idx_agent,
                Device.idx_device == DeviceAgent.idx_device,
                Agent.idx_agent != 1)
            )

    # Process query results
    for row in rows:
        idx_datapoint = row.idx_datapoint
        data_dict = {}
        data_dict['agent_label'] = general.decode(row.agent_label)
        data_dict['agent_source'] = general.decode(row.agent_source)
        data_dict['name'] = general.decode(row.name)
        data_dict['idx_deviceagent'] = row.idx_deviceagent
        data_dict['id_agent'] = general.decode(row.id_agent)
        data_dict['devicename'] = general.decode(row.devicename)

        # Assign values to data structures dependent on 'aslist' value
        data_dict['idx_datapoint'] = idx_datapoint
        data_list.append(data_dict)

    # Return the session to the database pool after processing
    database.close()

    # Return
    return data_list

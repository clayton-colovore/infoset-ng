"""Module of infoset database functions. Data table."""

# Python standard libraries
from collections import defaultdict
from sqlalchemy import and_

# Infoset libraries
from infoset.utils import general
from infoset.db import db_datapoint
from infoset.db import db
from infoset.db.db_orm import Data, Datapoint


class GetIDXData(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, config, idx_datapoint, start=None, stop=None):
        """Function for intializing the class.

        Args:
            config: Config object
            idx_datapoint: idx_datapoint of datapoint
            start: Starting timestamp
            stop: Ending timestamp

        Returns:
            None

        """
        # Initialize important variables
        self.data = defaultdict(dict)
        self.config = config

        # Get the datapoint's base_type
        datapointer = db_datapoint.GetIDXDatapoint(idx_datapoint)
        self.base_type = datapointer.base_type()
        self.agent_label = datapointer.agent_label()

        # Redefine start times
        if start is None:
            self.ts_start = general.normalized_timestamp() - (3600 * 24)
        else:
            self.ts_start = general.normalized_timestamp(start)

        # Redefine stop times
        if stop is None:
            self.ts_stop = general.normalized_timestamp()
        else:
            self.ts_stop = general.normalized_timestamp(stop)

        # Fix edge cases
        if self.ts_start > self.ts_stop:
            self.ts_start = self.ts_stop

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Data.timestamp, Data.value).filter(and_(
            Data.timestamp >= self.ts_start,
            Data.timestamp <= self.ts_stop,
            Data.idx_datapoint == idx_datapoint))

        # Massage data
        for instance in result:
            self.data[instance.timestamp] = float(instance.value)

        # Return the session to the database pool after processing
        database.close()

    def everything(self):
        """Get all datapoints.

        Args:
            None

        Returns:
            value: Dictionary of data_points

        """
        # Return data
        value = self._counter()
        return value

    def _counter(self):
        """Convert counter data to gauge.

        Args:
            None

        Returns:
            values: Converted dict of data keyed by timestamp

        """
        # Initialize key variables
        count = 0
        interval = self.config.interval()

        # Populate values dictionary with zeros. This ensures that
        # all timestamp values are covered if we have lost contact
        # with the agent at some point along the time series.
        if self.base_type == 1:
            values = dict.fromkeys(
                range(self.ts_start, self.ts_stop + interval, interval), 0)
        else:
            values = dict.fromkeys(
                range(self.ts_start + interval,
                      self.ts_stop + interval,
                      interval), 0)

        # Start conversion
        for timestamp, value in sorted(self.data.items()):
            # Process counter values
            if self.base_type != 1:
                # Skip first value
                if count == 0:
                    old_timestamp = timestamp
                    count += 1
                    continue

                #############################################################
                # Treat missing data with caution
                #############################################################
                # These are usually due to outages and can cause spikes
                # in the data. This ignores the first value after a zero.
                #############################################################
                if timestamp - old_timestamp > interval:
                    old_timestamp = timestamp
                    continue
                #############################################################
                #############################################################
                #############################################################

                # Get new value
                new_value = value - self.data[old_timestamp]

                # Do conversion to values / second
                if new_value >= 0:
                    values[timestamp] = new_value / interval
                else:
                    if self.base_type == 32:
                        fixed_value = 4294967296 + abs(value) - 1
                    else:
                        fixed_value = (
                            4294967296 * 4294967296) + abs(value) - 1
                    values[timestamp] = fixed_value / interval
            else:
                # Process gauge values
                values[timestamp] = self.data[timestamp]

            # Save old timestamp
            old_timestamp = timestamp

        # Return
        return values


def last_contacts(ts_start):
    """Get the last time each timeseries datapoint was updated.

    Args:
        config: Configuration object
        ts_start: Timestamp to start from

    Returns:
        data: List of dicts of last contact information

    """
    # Initialize key variables
    data = []
    last_contact = defaultdict(lambda: defaultdict(dict))

    # Get start and stop times
    ts_stop = general.normalized_timestamp()
    if ts_start > ts_stop:
        ts_start = ts_stop
    else:
        ts_start = general.normalized_timestamp(ts_start)

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(
        Data.value, Data.idx_datapoint, Data.timestamp).filter(
            and_(Data.timestamp >= ts_start, Data.timestamp <= ts_stop)
        )

    # Add to the list of device idx values
    for instance in result:
        idx_datapoint = instance.idx_datapoint
        timestamp = instance.timestamp
        value = instance.value

        # Update dictionary
        if idx_datapoint in last_contact:
            if timestamp > last_contact[idx_datapoint]['timestamp']:
                last_contact[idx_datapoint]['timestamp'] = timestamp
                last_contact[idx_datapoint]['value'] = value
            else:
                continue
        else:
            last_contact[idx_datapoint]['timestamp'] = timestamp
            last_contact[idx_datapoint]['value'] = value

    # Return the session to the pool after processing
    database.close()

    # Convert dict to list of dicts
    for idx_datapoint in last_contact:
        data_dict = {}
        data_dict['idx_datapoint'] = idx_datapoint
        data_dict['timestamp'] = last_contact[idx_datapoint]['timestamp']
        data_dict['value'] = last_contact[idx_datapoint]['value']
        data.append(data_dict)

    # Return
    return data


def last_contacts_by_device(idx_deviceagent, ts_start):
    """Get the last time each timeseries datapoint was updated.

    Args:
        config: Configuration object
        ts_start: Timestamp to start from

    Returns:
        data: List of dicts of last contact information

    """
    # Initialize key variables
    data = []
    last_contact = defaultdict(lambda: defaultdict(dict))

    # Establish a database session
    # Get start and stop times
    ts_stop = general.normalized_timestamp()
    if ts_start > ts_stop:
        ts_start = ts_stop
    else:
        ts_start = general.normalized_timestamp(ts_start)

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(
        Data.value, Data.idx_datapoint, Data.timestamp).filter(
            and_(
                Datapoint.idx_deviceagent == idx_deviceagent,
                Datapoint.idx_datapoint == Data.idx_datapoint,
                Data.timestamp >= ts_start,
                Data.timestamp <= ts_stop)
        )

    # Add to the list of device idx values
    for instance in result:
        idx_datapoint = instance.idx_datapoint
        timestamp = instance.timestamp
        value = instance.value

        # Update dictionary
        if idx_datapoint in last_contact:
            if timestamp > last_contact[idx_datapoint]['timestamp']:
                last_contact[idx_datapoint]['timestamp'] = timestamp
                last_contact[idx_datapoint]['value'] = value
            else:
                continue
        else:
            last_contact[idx_datapoint]['timestamp'] = timestamp
            last_contact[idx_datapoint]['value'] = value

    # Return the session to the pool after processing
    database.close()

    # Convert dict to list of dicts
    for idx_datapoint in last_contact:
        data_dict = {}
        data_dict['idx_datapoint'] = idx_datapoint
        data_dict['timestamp'] = last_contact[idx_datapoint]['timestamp']
        data_dict['value'] = last_contact[idx_datapoint]['value']
        data.append(data_dict)

    # Return
    return data

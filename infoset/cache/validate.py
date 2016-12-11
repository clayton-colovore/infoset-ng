#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
import re
import json
import time

# Infoset libraries
from infoset.utils import log
from infoset.utils import general
from infoset.db import db_deviceagent
from infoset.db import db_agent
from infoset.db import db_device


class ValidateCache(object):
    """Infoset class that ingests agent data.

    Args:
        None

    Returns:
        None

    Methods:
        __init__:
        populate:
        post:
    """

    def __init__(self, filepath=None, data=None):
        """Method initializing the class.

        Args:
            filepath: Cache filename
            data: Data dict expected to be in a cache file (Agent or server)

        Returns:
            None

        """
        # Initialize key variables
        self._valid = True
        self.information = {}
        _data = {}
        self.filepath = filepath

        # Assign data to self.information for future validity checks
        if filepath is not None:
            # Read data from file
            check = _CheckFile(self.filepath)
            if check.valid() is True:
                self.information = check.contents()
            else:
                self._valid = False
        else:
            if isinstance(data, dict) is True:
                # Check main keys in data.
                # Data read from file has already gone through this process.
                contents = _CheckMainKeys(data)
                if contents.valid() is True:
                    self.information = check.contents()
                else:
                    self._valid = False

    def getinfo(self):
        """Provide validated information when valid.

        Args:
            None

        Returns:
            data: Data

        """
        # Initialize key variables
        data = False

        # Return
        if self.valid() is True:
            data = self.information
        return data

    def valid(self):
        """Master method that defines whether data is OK.

        Args:
            None

        Returns:
            all_ok:

        """
        # Initialize key variables
        valid_list = [self._valid]
        ts_start = time.time()

        # Check timeseries and timefixed data in the data
        if len(valid_list) == valid_list.count(True):
            check = _CheckData(self.information)
            valid_list.append(check.valid())

        # Check if data to be validated is already in the database
        if len(valid_list) == valid_list.count(True):
            check = _CheckDuplicates(self.information)
            valid_list.append(check.valid())

        # Do final check
        if len(valid_list) == valid_list.count(True):
            # Log success
            ts_stop = time.time()
            duration = ts_stop - ts_start
            log_message = (
                'Data validation of %s took %s seconds.'
                '') % (self.filepath, round(duration, 4))
            log.log2debug(1126, log_message)
            all_ok = True

        else:
            # Log failure
            log_message = ('Cache data in %s is invalid') % (self.filepath)
            log.log2warning(1059, log_message)
            all_ok = False

        # Return
        return all_ok


class _CheckDuplicates(object):
    """Checks whether data for this agent has already been entered.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, data):
        """Method initializing the class.

        Args:
            data: Ingested data to validate

        Returns:
            None

        """
        # Initialize key variables
        self._valid = True
        self.data = data

        # Check that we are evaluating a dict
        if isinstance(self.data, dict) is False:
            log_message = ('Ingest data is not a dictionary')
            log.log2warning(1116, log_message)
            self._valid = False

    def valid(self):
        """Check if data keys are OK.

        Args:
            None

        Returns:
            valid: True if valid

        """
        # Initialize key variables
        valid = True
        timestamp = int(self.data['timestamp'])
        id_agent = self.data['id_agent']
        devicename = self.data['devicename']

        # Check if there is a duplicate entry for this id_agent
        if db_agent.id_agent_exists(id_agent) is not False:
            idx_agent = db_agent.GetIDAgent(id_agent).idx_agent()

            # Check if device exists
            if db_device.devicename_exists(devicename) is True:
                idx_device = db_device.GetDevice(devicename).idx_device()

                # Check for device / agent entry existence
                if db_deviceagent.device_agent_exists(
                        idx_device, idx_agent) is True:
                    # Check if this device / agent has been updated before
                    last_timesamp = db_deviceagent.GetDeviceAgent(
                        idx_device, idx_agent).last_timestamp()

                    # Validate
                    if timestamp <= last_timesamp:
                        log_message = (
                            'Data for id_agent %s, devicename %s '
                            'at timestamp %s '
                            'is already found in database.'
                            '') % (id_agent, devicename, timestamp)
                        log.log2warning(1113, log_message)
                        valid = False

        # Return
        return valid


class _CheckData(object):
    """Validates timeseries data in ingested data.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, data):
        """Method initializing the class.

        Args:
            data: Ingested data to validate

        Returns:
            None

        """
        # Initialize key variables
        self._valid = True
        self.data = data

        # Check that we are evaluating a dict
        if isinstance(self.data, dict) is False:
            log_message = ('Ingest data is not a dictionary')
            log.log2warning(1121, log_message)
            self._valid = False

    def _data_keys_ok(self):
        """Check if data keys are OK.

        Args:
            None

        Returns:
            valid: True if valid

        """
        # Initialize key variables
        valid = False
        data_types = ['timeseries', 'timefixed']

        # Process data
        if self._valid is True:
            for data_type in data_types:
                # Skip if data type isn't in the data
                if data_type in self.data:
                    valid = True

        # Log error
        if valid is False:
            log_message = (
                'Ingest data does not contain data keys.')
            log.log2warning(1003, log_message)

        # Return
        return valid

    def _agent_label_keys_ok(self):
        """Check if agent label keys are OK.

        Args:
            None

        Returns:
            valid: True if valid

        """
        # Initialize key variables
        valid = True
        data_types = ['timeseries', 'timefixed']

        # Check major keys expected under each ageng label
        if self._data_keys_ok() is False:
            valid = False
            return valid

        # Check each data_type
        for data_type in data_types:
            # Skip if key is not present
            if data_type not in self.data:
                continue

            # Process next major key
            # The "_" in this case is the agent label in the dict
            for _, agent_items in sorted(
                    self.data[data_type].items()):
                # Process keys in data reported by agents
                for key in ['base_type', 'description', 'data']:
                    if key not in agent_items:
                        log_message = (
                            '"%s" data type does not contain a "%s" key.'
                            '') % (data_type, key)
                        log.log2warning(1115, log_message)
                        valid = False
                        return valid

                # Process data
                if 'data' in agent_items:
                    for datapoint in agent_items['data']:
                        if len(datapoint) != 3:
                            log_message = (
                                '"%s" data type does not contain valid '
                                'datapoints in it\'s "data" key.'
                                '') % (data_type)
                            log.log2warning(1114, log_message)
                            valid = False
                else:
                    # If there is no data, then it must be invalid
                    log_message = (
                        'Ingest data has no "data" label '
                        'values for database.')
                    log.log2warning(1004, log_message)
                    valid = False
                    return valid

        # Return
        return valid

    def _charable_data_ok(self):
        """Check if timeseries data is OK.

        Args:
            None

        Returns:
            valid: True if valid

        """
        # Initialize key variables
        valid = True
        data_type = 'timeseries'

        # Check major keys expected under each ageng label
        if self._agent_label_keys_ok() is False:
            valid = False
            return valid

        # Check for timeseries data
        if data_type in self.data:

            # Process the data type
            for _, reported_data in sorted(
                    self.data[data_type].items()):

                # Make sure the base types are numeric
                if 'base_type' in reported_data:
                    try:
                        float(reported_data['base_type'])
                    except:
                        log_message = (
                            'TimeSeries "base_type" key is non numeric.')
                        log.log2warning(1120, log_message)
                        valid = False
                        return valid
                else:
                    log_message = (
                        'TimeSeries data has no "base_type" key.')
                    log.log2warning(1117, log_message)
                    valid = False
                    return valid

                # Process data
                if 'data' in reported_data:
                    for datapoint in reported_data['data']:
                        # Check to make sure value is numeric
                        value = datapoint[1]
                        try:
                            float(value)
                        except:
                            log_message = (
                                'TimeSeries data has non numeric data values.')
                            log.log2warning(1119, log_message)
                            valid = False
                            return valid
                else:
                    log_message = (
                        'TimeSeries data has no "data" key.')
                    log.log2warning(1118, log_message)
                    valid = False
                    return valid

        # Return
        return valid

    def valid(self):
        """Validate Data.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False
        valid_list = [self._valid]

        # All other tests need to pass for _charable_data_ok to pass
        valid_list.append(self._charable_data_ok())

        # Return
        if len(valid_list) == valid_list.count(True):
            valid = True
        else:
            log_message = ('Failed validity testing. %s') % (valid_list)
            log.log2warning(1002, log_message)
        return valid


class _CheckMainKeys(object):
    """Validates main keys in ingested data.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, data):
        """Method initializing the class.

        Args:
            data: Ingested data to validate

        Returns:
            None

        """
        # Initialize key variables
        self.data = data
        self._valid = True

        # Check if data is a dict
        if isinstance(data, dict) is False:
            log_message = ('Ingest data is not a dictionary')
            log.log2warning(1093, log_message)
            self._valid = False

    def _timestamp(self):
        """Verify existence of timestamp key.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False

        # Check key
        if self._valid is True:
            if 'timestamp' in self.data:
                if isinstance(self.data['timestamp'], int) is True:
                    valid = True

        # Return
        return valid

    def _id_agent(self):
        """Verify existence of id_agent key.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False

        # Check key
        if self._valid is True:
            if 'id_agent' in self.data:
                if isinstance(self.data['id_agent'], str) is True:
                    valid = True

        # Return
        return valid

    def _agent(self):
        """Verify existence of agent key.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False

        # Check key
        if self._valid is True:
            if 'agent' in self.data:
                if isinstance(self.data['agent'], str) is True:
                    valid = True

        # Return
        return valid

    def _devicename(self):
        """Verify existence of devicename key.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False

        # Check key
        if self._valid is True:
            if 'devicename' in self.data:
                if isinstance(self.data['devicename'], str) is True:
                    valid = True

        # Return
        return valid

    def valid(self):
        """Validate main keys.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False
        valid_list = [self._valid]
        valid_list.append(self._timestamp())
        valid_list.append(self._agent())
        valid_list.append(self._id_agent())
        valid_list.append(self._devicename())

        # Define validity
        if len(valid_list) == valid_list.count(True):
            valid = True
        else:
            log_message = ('Ingest data does not have all main keys')
            log.log2warning(1000, log_message)

        # Return
        return valid


class _CheckFile(object):
    """Validate file.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, filepath):
        """Method initializing the class.

        Args:
            filepath: Cache filename

        Returns:
            None

        """
        # Initialize key variables
        self.filepath = filepath
        self.data = None
        self._valid = False
        name_ok = _valid_filename(filepath)

        # Read data from file
        if name_ok is True:
            self.data = _read_data_from_file(filepath)
        else:
            # Log status
            log_message = (
                'File %s does has incorrect filename format.'
                '') % (filepath)
            log.log2warning(1026, log_message)

        # Check main keys in data.
        contents = _CheckMainKeys(self.data)
        if contents.valid() is True:
            if name_ok is True:
                self._valid = True

    def _keys_in_filename(self):
        """Validate main keys contained in the file are in the filename.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = True

        # Get timestamp and id_agent from filename
        filename = os.path.basename(self.filepath)
        (name, _) = filename.split('.')
        (tstamp, id_agent, _) = name.split('_')
        timestamp = int(tstamp)

        # Double check that the id_agent and timestamp in the
        # filename matches that in the file.
        # Ignore invalid files as a safety measure.
        # Don't try to delete. They could be owned by some
        # one else and the daemon could crash
        if id_agent != self.data['id_agent']:
            log_message = (
                'id_agent %s in file %s does not match '
                'id_agent %s in filename.'
                '') % (
                    self.data['id_agent'],
                    id_agent, self.filepath)
            log.log2warning(1123, log_message)
            valid = False

        # Check timestamp
        if timestamp != self.data['timestamp']:
            log_message = (
                'Timestamp %s in file %s does not match timestamp '
                '%s in filename.'
                '') % (
                    self.data['timestamp'],
                    timestamp, self.filepath)
            log.log2warning(1111, log_message)
            valid = False

        # Check timestamp validity
        if general.validate_timestamp(timestamp) is False:
            log_message = (
                'Timestamp %s in file %s is not normalized'
                '') % (self.data['timestamp'], self.filepath)
            log.log2warning(1112, log_message)
            valid = False

        # Return
        return valid

    def valid(self):
        """Validate main keys in filename.

        Args:
            None

        Returns:
            valid: Valid if True

        """
        # Initialize key variables
        valid = False
        valid_list = [self._valid]

        # Check keys
        if len(valid_list) == valid_list.count(True):
            valid_list.append(self._keys_in_filename())

        # Return
        if len(valid_list) == valid_list.count(True):
            valid = True
        else:
            log_message = (
                'File %s failed validity testing.') % (self.filepath)
            log.log2warning(1001, log_message)
        return valid

    def contents(self):
        """Return contents of file.

        Args:
            None

        Returns:
            self.data: Data in file

        """
        # Return
        return self.data


def _valid_filename(filepath):
    """Check if the filename in the filepath is valid.

    Args:
        filepath: Filepath

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = False

    # Filenames must start with a numeric timestamp and #
    # end with a hex string. This will be tested later
    regex = re.compile(r'^\d+_[0-9a-f]+_[0-9a-f]+.json')

    # Try reading file if filename format is OK
    filename = os.path.basename(filepath)
    if bool(regex.match(filename)) is True:
        valid = True

    # Return
    return valid


def _read_data_from_file(filepath):
    """Provide validated information when valid.

    Args:
        filepath: Path to file

    Returns:
        data: Data

    """
    # Initialize key variables
    data = {}

    # Ingest data
    try:
        with open(filepath, 'r') as f_handle:
            data = json.load(f_handle)
    except:
        # Log status
        log_message = (
            'File %s does not contain JSON data, does not exist, '
            'or is unreadable.') % (filepath)
        log.log2warning(1006, log_message)

    # Return
    return data

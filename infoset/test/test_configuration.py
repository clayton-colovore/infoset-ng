#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import os
import os.path
import tempfile
import unittest
import yaml

from infoset.utils import configuration


class TestConfiguration(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    log_directory = tempfile.mkdtemp()
    cache_directory = tempfile.mkdtemp()
    good_config = ("""\
main:
    log_directory: %s
    log_level: debug
    ingest_cache_directory: %s
    ingest_pool_size: 20
    bind_port: 3000
    interval: 300
    sqlalchemy_pool_size: 10
    sqlalchemy_max_overflow: 10
    db_hostname: localhost
    db_username: test_infoset
    db_password: test_B3bFHgxQfsEy86TN
    db_name: test_infoset
""") % (log_directory, cache_directory)

    # Convert good_config to dictionary
    good_dict = yaml.load(bytes(good_config, 'utf-8'))

    # Set the environmental variable for the configuration directory
    directory = tempfile.mkdtemp()
    os.environ['INFOSET_CONFIGDIR'] = directory
    config_file = ('%s/test_config.yaml') % (directory)

    # Write good_config to file
    with open(config_file, 'w') as f_handle:
        yaml.dump(good_dict, f_handle, default_flow_style=True)

    # Create configuration object
    config = configuration.Config()

    @classmethod
    def tearDownClass(cls):
        """Post test cleanup."""
        os.rmdir(cls.log_directory)
        os.rmdir(cls.cache_directory)
        os.remove(cls.config_file)
        os.rmdir(cls.directory)

    def test_init(self):
        """Testing method init."""
        # Testing with non-existant directory
        directory = 'bogus'
        os.environ['INFOSET_CONFIGDIR'] = directory
        with self.assertRaises(SystemExit):
            configuration.Config()

        # Testing with an empty directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        with self.assertRaises(SystemExit):
            configuration.Config()

        # Write bad_config to file
        config_file = ('%s/test_config.yaml') % (directory)
        with open(config_file, 'w') as f_handle:
            f_handle.write('')

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_file()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_log_file(self):
        """Testing method log_file."""
        # Test the log_file with a good_dict
        # good key and key_value
        result = self.config.log_file()
        self.assertEqual(result, ('%s/infoset-ng.log') % (self.log_directory))

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing log_file with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_file()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_web_log_file(self):
        """Testing method web_log_file ."""
        # Testing web_log_file with a good dictionary.
        result = self.config.web_log_file()
        self.assertEqual(result, ('%s/api-web.log') % (self.log_directory))

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing web_log_file with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.web_log_file()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_log_level(self):
        """Testing method log_level."""
        # Tesing with a good_dictionary
        # good key and good key_value
        result = self.config.log_level()
        self.assertEqual(result, 'debug')
        self.assertEqual(result, self.good_dict['main']['log_level'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing log_level with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_level()

        # Testing log_level with good key and blank key_value
        key = 'log_level:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.log_level()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_ingest_cache_directory(self):
        """Testing method ingest_cache_directory"""
        # Testing ingest_cache_directory with temp directory
        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing ingest_cache_directory with blank key_value(filepath)
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.ingest_cache_directory()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_ingest_pool_size(self):
        """Testing method ingest_pool_size."""
        # Testing ingest_pool_size with good_dict
        # good key and key_value
        result = self.config.ingest_pool_size()
        self.assertEqual(result, 20)
        self.assertEqual(result, self.good_dict['main']['ingest_pool_size'])

    def test_bind_port(self):
        """Testing method bind_port."""
        # Testing bind_port with good_dictionary
        # good key and key_value
        result = self.config.bind_port()
        self.assertEqual(result, 3000)
        self.assertEqual(result, self.good_dict['main']['bind_port'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing bind_port with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.bind_port()

        # Testing bind_port with good key and blank key_value
        key = 'bind_port:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.bind_port()
        self.assertEqual(result, 6000)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_interval(self):
        """Testing method interval."""
        # Testing interval with good_dictionary
        # good key value and key_value
        result = self.config.interval()
        self.assertEqual(result, 300)
        self.assertEqual(result, self.good_dict['main']['interval'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing interval with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.interval()

        # Testing interval with blank key_value
        key = 'interval:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.interval()
        self.assertEqual(result, 300)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_sqlalchemy_pool_size(self):
        """Testing method sqlalchemy_pool_size."""
        # Testing sqlalchemy_pool_size with a good dictionary
        # good key and key_value
        result = self.config.sqlalchemy_pool_size()
        self.assertEqual(result, 10)
        self.assertEqual(
            result, self.good_dict['main']['sqlalchemy_pool_size'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing sqlalchemy_pool_size with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.sqlalchemy_pool_size()

        # Testing sqlalchemy_pool_size with good key and blank key_value
        key = 'sqlalchemy_pool_size:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.sqlalchemy_pool_size()
        self.assertEqual(result, 10)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_sqlalchemy_max_overflow(self):
        """Testing method sqlalchemy_max_overflow."""
        result = self.config.sqlalchemy_max_overflow()
        self.assertEqual(result, 10)
        self.assertEqual(
            result, self.good_dict['main']['sqlalchemy_max_overflow'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing sqlalchemy_max_overflow with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.sqlalchemy_max_overflow()

        # Testing sqlalchemy_max_overflow with good key and blank key_value
        key = 'sqlalchemy_max_overflow:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        result = config.sqlalchemy_max_overflow()
        self.assertEqual(result, 10)

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_db_hostname(self):
        """Testing method db_hostname."""
        result = self.config.db_hostname()
        self.assertEqual(result, 'localhost')
        self.assertEqual(result, self.good_dict['main']['db_hostname'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing db_hostname with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_hostname()

        # Testing db_hostname with good key and blank key_value
        key = 'db_hostname:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_hostname()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_db_username(self):
        """Testing method db_username."""
        result = self.config.db_username()
        self.assertEqual(result, 'test_infoset')
        self.assertEqual(result, self.good_dict['main']['db_username'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing db_username with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_username()

        # Testing db_username with good key and blank key_value
        key = 'db_username:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_username()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_db_password(self):
        """Testing method db_password."""
        result = self.config.db_password()
        self.assertEqual(result, 'test_B3bFHgxQfsEy86TN')
        self.assertEqual(result, self.good_dict['main']['db_password'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing db_password with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_password()

        # Testing db_password with good key and blank key_value
        key = 'db_password:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_password()

        # Cleanup files in temp directories
        _delete_files(directory)

    def test_db_name(self):
        """Testing method db_name."""
        result = self.config.db_name()
        self.assertEqual(result, 'test_infoset')
        self.assertEqual(result, self.good_dict['main']['db_name'])

        # Set the environmental variable for the configuration directory
        directory = tempfile.mkdtemp()
        os.environ['INFOSET_CONFIGDIR'] = directory
        config_file = ('%s/test_config.yaml') % (directory)

        # Testing db_name with blank key and blank key_value
        key = ''
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_name()

        # Testing db_name with good key and blank key_value
        key = 'db_name:'
        key_value = ''
        bad_config = ("""\
main:
    %s %s
""") % (key, key_value)
        bad_dict = yaml.load(bytes(bad_config, 'utf-8'))

        # Write bad_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(bad_dict, f_handle, default_flow_style=True)

        # Create configuration object
        config = configuration.Config()
        with self.assertRaises(SystemExit):
            config.db_name()

        # Cleanup files in temp directories
        _delete_files(directory)


def _delete_files(directory):
    """Delete all files in directory."""
    # Cleanup files in temp directories
    filenames = [filename for filename in os.listdir(
        directory) if os.path.isfile(
            os.path.join(directory, filename))]

    # Get the full filepath for the cache file and remove filepath
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)

    # Remove directory after files are deleted.
    os.rmdir(directory)


if __name__ == '__main__':
    # Do the unit test
    unittest.main()

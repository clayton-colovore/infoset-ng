#!/usr/bin/env python3
"""Test the jm_general module."""

import tempfile
import unittest
import random
import os
import string
import hashlib

# Import non standard library
import yaml
from infoset.utils import general
from infoset import infoset


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    def test_root_directory(self):
        """Test function root_directory."""
        # Determine root directory for infoset
        infoset_dir = infoset.__path__[0]
        components = infoset_dir.split(os.sep)
        # Determine root directory 2 levels above
        root_dir = os.sep.join(components[0:-2])
        result = general.root_directory()
        self.assertEqual(result, root_dir)

    def testvalidate_timestamp(self):
        """Validate timestamp to be a multiple of 300 seconds."""
        # Initialize key variables
        result = general.validate_timestamp(300)
        self.assertEqual(result, True)
        result = general.validate_timestamp(400)
        self.assertEqual(result, False)
        result = general.validate_timestamp(500)
        self.assertEqual(result, False)

    def test_normalized_timestamp(self):
        """Testing method / function normalized_timestamp."""
        # Initialize key variables
        result = general.normalized_timestamp(300)
        self.assertEqual(result, 300)
        result = general.normalized_timestamp(350)
        self.assertEqual(result, 300)
        result = general.normalized_timestamp(599)
        self.assertEqual(result, 300)

    def test_hashstring(self):
        """Create a UTF encoded SHA hash string."""
        # Initialize key variables
        test_string = 'banana'
        test_string_encoded = bytes(test_string.encode())
        hasher = hashlib.sha256()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string)
        self.assertEqual(result, expected)

        hasher = hashlib.sha512()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string, sha=512)
        self.assertEqual(result, expected)
        result = general.hashstring(test_string, sha=512, utf8=True)
        self.assertEqual(result, expected.encode())

        hasher = hashlib.sha256()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string, sha=256)
        self.assertEqual(result, expected)
        result = general.hashstring(test_string, sha=256, utf8=True)
        self.assertEqual(result, expected.encode())

        hasher = hashlib.sha224()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string, sha=224)
        self.assertEqual(result, expected)
        result = general.hashstring(test_string, sha=224, utf8=True)
        self.assertEqual(result, expected.encode())

        hasher = hashlib.sha384()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string, sha=384)
        self.assertEqual(result, expected)
        result = general.hashstring(test_string, sha=384, utf8=True)
        self.assertEqual(result, expected.encode())

        hasher = hashlib.sha1()
        hasher.update(test_string_encoded)
        expected = hasher.hexdigest()
        result = general.hashstring(test_string, sha=1)
        self.assertEqual(result, expected)
        result = general.hashstring(test_string, sha=1, utf8=True)
        self.assertEqual(result, expected.encode())

    def test_encode(self):
        """Test function test_encode."""
        # Initialize key variables
        expected = b'carrot'
        result = general.encode("carrot")
        self.assertEqual(result, expected)

    def test_decode(self):
        """Test function test_decode."""
        # Initialize key variables
        expected = 'carrot'
        result = general.decode(b"carrot")
        self.assertEqual(result, expected)

    def test_read_yaml_files(self):
        """Test function read_yaml_files."""
        # Initialize key variables
        dict_1 = {
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4,
        }

        dict_2 = {
            'key6': 6,
            'key7': 7,
        }
        dict_3 = {}

        # Populate a third dictionary with contents of other dictionaries.
        for key in dict_1.keys():
            dict_3[key] = dict_1[key]

        for key in dict_2.keys():
            dict_3[key] = dict_2[key]

        # Create temp file with known data
        directory = tempfile.mkdtemp()
        filenames = {
            ('%s/file_1.yaml') % (directory): dict_1,
            ('%s/file_2.yaml') % (directory): dict_2
        }
        for filename, data_dict in filenames.items():
            with open(filename, 'w') as filehandle:
                yaml.dump(data_dict, filehandle, default_flow_style=False)

        # Get Results
        result = general.read_yaml_files([directory])

        # Clean up
        for key in result.keys():
            self.assertEqual(dict_3[key], result[key])
        filelist = [
            next_file for next_file in os.listdir(
                directory) if next_file.endswith('.yaml')]
        for delete_file in filelist:
            delete_path = ('%s/%s') % (directory, delete_file)
            os.remove(delete_path)
        os.removedirs(directory)

    def test_search_file(self):
        """Test function search_file."""
        # Initialize key variables
        result = general.search_file('cat')
        self.assertEqual(result, '/bin/cat')

    def test_run_script(self):
        """Test function run_script."""
        # Initialize key variables
        pass

if __name__ == '__main__':

    # Do the unit test
    unittest.main()

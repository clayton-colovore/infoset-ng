#!/usr/bin/env python3
"""Code that interacts with memory cache."""

# Standard libraries
import memcache


class Cache(object):
    """Class for interaction with memory cache."""

    def __init__(self, config):
        """Method initializing the class.

        Args:
            config: Configuration object

        Returns:
            None

        """
        # Initialize key variables
        connection_string = (
            '{}:{}'
            ''.format(
                config.memcached_hostname(), config.memcached_port()))
        self.cache = memcache.Client([connection_string], debug=0)

    def set(self, key, value):
        """Set the key, value pair in cache.

        Args:
            None

        Returns:
            result: Result of the set

        """
        # Initialize key variables
        result = self.cache.set(key, value)

        # Return
        return result

    def get(self, key):
        """Get the key, value pair in cache.

        Args:
            key: Key to retrieve

        Returns:
            result: Result of the set

        """
        # Initialize key variables
        result = self.cache.get(key)

        # Return
        return result

    def delete(self, key):
        """Delete the key, value pair in cache.

        Args:
            key: Key to retrieve

        Returns:
            result: Result of the set

        """
        # Initialize key variables
        result = self.cache.delete(key)

        # Return
        return result

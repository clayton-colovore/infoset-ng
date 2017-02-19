#!/usr/bin/env python3
"""Code that interacts with memory cache."""

# PIP3 libraries
import memcache
from flask import request


def flask_cache_key(*args, **kwargs):
    """Create a key for use by Flask-Caching.

    Args:
        None

    Returns:
        result: Key to be used

    """
    # Use the request URI as part of the key
    path = request.path

    # This helps to differentiate between various instances of infoset
    # each running on different ports
    server_port = request.environ['SERVER_PORT']

    # Use a hash of the request arguments as part of the key
    args = str(hash(frozenset(request.args.items())))

    # Return
    result = (
        'infoset_flask_{}_{}_{}'.format(
            path, server_port, args)[:255].encode('utf-8'))
    return result


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

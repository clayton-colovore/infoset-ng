Troubleshooting
===============

There are a number of ways you can troubleshoot the ``ingester`` and ``API``. The most accessible ways are through the log files and the API test script.

Ingester Troubleshooting
------------------------

This section covers the various ways you can troubleshoot ``ingester`` operation.

Ingester Logging
~~~~~~~~~~~~~~~~

It is always good to verify the operation of the ``ingester`` by observing changes in its log file. It is a good source of troubleshooting information.

You can see these changes as they occur by using the ``tail -f`` command as seen below:

::

    $ tail -f /opt/infoset-ng/log/infoset-ng.log

The location of the log file is governed by the ``log_file`` parameter in the configuration.

Testing Ingester Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can test the operation of the API by using the ``curl`` command which is often used to test basic website functionality. The example below shows how. Replace ``SERVER_IP`` with the IP address or fully qualified DNS name.

::

    $ curl http://SERVER_IP:6000/infoset/api/v1.0
    infoset-ng API Operational.
    $

The ``curl`` response should be ``infoset-ng API Operational`` if
successful.

Invalid Agents
~~~~~~~~~~~~~~

There is the possibility that agents may be posting incorrectly formatted JSON data to the ``API``. You can view the contents of these invalidated files in the  ``failures/`` sub-directory of the ``API`` cache directory. The cache directory is defined in the ``ingest_cache_directory:`` option of the configuration file.

API Troubleshooting
-------------------

There are a number of ways you can troubleshoot the ``API``. The most accessible ways are through the log file.


API Logging
~~~~~~~~~~~

It is always good to verify the operation of the ``API`` by observing changes in its log file. It is a good source of troubleshooting information.

You can see these changes as they occur by using the ``tail -f`` command as seen below:

::

    $ tail -f /opt/infoset-ng/log/web.log

The location of the log file is governed by the ``web_log_file`` parameter in the configuration.


Poor or Blocked Network Connectivity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is possible that there could be firewalls or intermittent connectivity causing issues to your ``API`` you should familarize yourself with the ``tcpdump`` command to determine whether connections are coming through.

In this example we are testing to see whether we are receiving traffic from IP address 192.168.1.100 on TCP port 6000 which the ``API`` uses

::

    $ sudo tcpdump -ni tcp port 6000 and host 192.168.1.100

You can also use the basic ``telnet`` command to determine whether the remote device or network can communicate with the ``API``. In this example we are testing to see whether we can communicate with the ``API`` running on a server with IP address 192.168.1.200 on the default TCP port 6000. 

::

    $ telnet 192.168.1.200 6000
    Trying 192.168.1.200...
    Connected to 192.168.1.200.
    Escape character is '^]'.
    ^]
    telnet> quit
    Connection closed.

If you get no response, then you need. Try this approach on both the local and remote ends of the connection. In other words, use the same command on both the remote client and ``API`` server. If there is response on the server, but none on the client, then there is probably a connectivity issue.

You can also determine whether the ``API`` server is running at all. Use the ``netstat`` command on the ``API`` server itself to determine whether it is listening on port 6000. If there is no response, then the API isn't running.

::

    $ netstat -ant |grep 6000
    tcp        0      0 0.0.0.0:6000            0.0.0.0:*               LISTEN
    $

You should also try to use the ``curl`` examples in the ``API`` guide to assist further.


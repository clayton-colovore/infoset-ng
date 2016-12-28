Operation
=========

``infoset-ng`` has two major components. These are:

1. **The Ingester**: Periodically retrieves data from the cache files
   and places it in the database.
2. **The API**: Stores and retrieves data from the database via REST API
   calls. Received data is placed in the cache directory defined in the
   configuration.

Explanations of how to permanently run each component will be given shortly, but first we'll cover how to test your installation.

Testing Operation After Installation
------------------------------------

There are a number of steps to take to make sure you have installed ``infoset-ng`` correctly. This section explains how to do basic testing before putting ``infoset-ng`` into production.

Start the API Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the ``infoset-ng`` API interactively.

::

    $ bin/infoset-ng-api --start


Start the Ingester Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ingester will need to be running prior to testing.

::

    $ bin/infoset-ng-ingester --start


Test API Functionality
~~~~~~~~~~~~~~~~~~~~~~

Now that both the API and ingester are running, it's time to test functionality by running the ``bin/tools/test_installation.py`` script

Here is an example of a successful test:

::

    $ bin/tools/test_installation.py
    2016-12-03 18:12:56,640 - infoset_console - INFO - [peter] (1054S): Successfully posted test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749
    2016-12-03 18:12:56,656 - infoset_console - INFO - [peter] (1054S): Successfully retrieved test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

    OK

    $

Refer to the Troubleshooting section of this page to rectify any issues.

Stop After Successful Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you have tested the functionality successsfully it is time to stop the interactive API session until you decide the best method to run ``infoset-ng``, either interactively as you did during the testing or as system daemons. 

::

    $ bin/infoset-ng-api --stop
    $ bin/infoset-ng-ingester --stop


The procedures to operate ``infoset-ng`` using the various types of daemons will be covered next.


Ingester Operation
------------------

The ``ingester`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Daemon**: Interactively run by a user from the CLI. The ``ingester`` will not automatically restart after a reboot.


Usage of the ``ingester`` in each mode will be discussed next.


The Ingester as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the preferred mode of operation for production systems. This mode is automatically configured if you installed ``infoset-ng`` using the ``root`` user.

The ``ingester`` can be started like this:

::

    $ sudo systemctl start infoset-ng-ingester.service

The ``ingester`` can be stopped like this:

::

    $ sudo systemctl stop infoset-ng-ingester.service

You can get the status of the ``ingester`` like this:

::

    $ sudo systemctl status infoset-ng-ingester.service

You can get the ``ingester`` to automatically restart on boot like this:

::

    $ sudo systemctl enable infoset-ng-ingester.service
    
A sample system startup script can be found in the
``examples/linux/systemd/infoset-ng-ingester.service`` file. Follow the instructions in the file to make changes to the startup operation of the ``ingester`` daemon.

**Note:** There will be no visible output when the ``ingester`` is running. The ``ingester`` logs its status to the ``etc/infoset-ng.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/infoset-ng.log


The Ingester as a User Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This mode is available if you want to run the ``ingester`` in a standalone mode. The ``ingester`` can be started like this:

::

    $ bin/infoset-ng-ingester --start

The ingester can be stopped like this:

::

    $ bin/infoset-ng-ingester --stop

You can get the status of the ingester like this:

::

    $ bin/infoset-ng-ingester --status

You may want to make sure that the ingester is running correctly. This will be covered next.

**Note:** There will be no visible output when the ``ingester`` is running. The ``ingester`` logs its status to the ``etc/infoset-ng.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/infoset-ng.log

API Operation
-------------
The ``API`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Process**: Run by a user from the CLI. The ``API`` will not automatically restart after a reboot.

Usage of the ``API`` in each mode will be discussed next.


The API as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the preferred mode of operation for production systems. This mode is automatically configured if you installed ``infoset-ng`` using the ``root`` user.

The ``API`` can be started like this:

::

    $ sudo systemctl start infoset-ng-api.service

The ``API`` can be stopped like this:

::

    $ sudo systemctl stop infoset-ng-api.service

You can get the status of the ``API`` like this:

::

    $ sudo systemctl status infoset-ng-api.service

You can get the ``API`` to automatically restart on boot like this:

::

    $ sudo systemctl enable infoset-ng-api.service
    
A sample system startup script can be found in the
``examples/linux/systemd/infoset-ng-api.service`` file. Follow the instructions in the file to make changes to the startup operation of the ``API`` daemon.

**Note:** There will be no visible output when the ``API`` is running. The ``API`` logs its status to the ``etc/api-web.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/api-web.log


The API as a User Process
~~~~~~~~~~~~~~~~~~~~~~~~~

You can run the API in standalone mode using the  ``bin/infoset-ng-api`` script. The standalone ``API`` can be started like this:

::

    $ bin/infoset-ng-api --start

The API can be stopped like this:

::

    $ bin/infoset-ng-api --stop

You can get the status of the API like this:

::

    $ bin/infoset-ng-api --status

**Note:** There will be no visible output when the API is running. Web traffic to the API is logged to the ``etc/api-web.log`` file by default. You will be able to see this interaction dynamically by running the following command:

::

    $ tail -f etc/api-web.log


Command Line Interface (CLI)
============================

This page outlines how to use the ``infoset-ng`` command line interface (CLI)

Viewing ``infoset-ng`` status
-------------------------------

There are two important ``infoset-ng`` daemons.

1) **ingester:** Gets data from devices
2) **API:** Displays device data on web pages

You can get the status of  each daemon using the following CLI commands:

Ingester status
~~~~~~~~~~~~~~~

You can get the status of the ingester using this command:

::

    $ bin/infoset-ng-cli show ingester status


API status
~~~~~~~~~~

You can get the status of the API using this command:

::

    $ bin/infoset-ng-cli show api status


Managing the ``infoset-ng`` Daemons
-------------------------------------

You can manage the daemons using the CLI. Here's how:

Ingester Management
~~~~~~~~~~~~~~~~~~~

The ingester can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung.

::

    $ bin/infoset-ng-cli ingester start

    $ bin/infoset-ng-cli ingester stop
    $ bin/infoset-ng-cli ingester stop --force

    $ bin/infoset-ng-cli ingester restart
    $ bin/infoset-ng-cli ingester restart --force

**Note:** You will need to do a restart whenever you modify a configuration parameter.

API Management
~~~~~~~~~~~~~~

The API can be started, stopped and restarted using the following commands. Use the ``--force`` option only if the daemon may be hung.

::

    $ bin/infoset-ng-cli api start

    $ bin/infoset-ng-cli api stop
    $ bin/infoset-ng-cli api stop --force

    $ bin/infoset-ng-cli api restart
    $ bin/infoset-ng-cli api restart --force

**Note:** You will need to do a restart whenever you modify a configuration parameter.

Testing Infoset-NG
------------------

You will need to verify system operation. Here's how.

::

    $ bin/infoset-ng-cli test ingester


Viewing ``infoset-ng`` logs
-----------------------------

When troubleshooting it is a good practice to view the ``infoset-ng`` log files.

Ingester logs
~~~~~~~~~~~~~

You can view the ingester logs using this command:

::

    $ bin/infoset-ng-cli show ingester logs


API logs
~~~~~~~~

You can view the API logs using this command:

::

    $ bin/infoset-ng-cli show api logs

Viewing the ``infoset-ng`` Configuration
------------------------------------------

You can view the configuration using this command:

::

    $ bin/infoset-ng-cli show configuration

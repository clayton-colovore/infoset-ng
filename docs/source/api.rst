Using the API
=============

This section outlines how to use the API

Why Infoset-ng Expects UTC Timestamps
-------------------------------------

There is a good reason for this. According to the python datetime documentation page, `The rules for time adjustment across the world are more political than rational, change frequently, and there is no standard suitable for every application aside from UTC.`

We cannot guarantee the python timezone libraries will be always up to date, so we default to UTC as recommended.

Posting Data to the API
-----------------------

Posting data to the API is. Add the prefix ``http://SERVER_IP:6000`` to
all the examples below to update data in your instance of ``infoset-ng``

Route /infoset/api/v1/receive/``<id_agent>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSON data needs to be posted to the ``http://SERVER_IP:6000/infoset/api/v1/receive/<id_agent>`` URL where ``id_agent`` is a unique identifier of the software script that is posting the data. This ``id_agent`` must be unique and consistent for each **script** or **application** posting data to ``infoset-ng``. For example, if you have three data collection scripts running across two devices, then each script must report a unique ``id_agent``, three unique IDs in total. We suggest using a hash of a random string to generate your ``id_agent``. There is a 512 character limit on the size of the ``agent_id``.

The example below explains the expected JSON format:

::

    {'agent': 'agent_name',
    'timeseries': {'label_l': {'base_type': 1,
                                   'data': [[1, 224.0, 'source_1']],
                                   'description': 'description_1},
                  'label_2': {'base_type': 1,
                                    'data': [[1, 1383.2, 'source_2']],
                                    'description': 'description_2'}},
    'devicename': '192.168.3.100',
    'timestamp': 1474823400,
    'id_agent': '8a6887228e33e3b433bd0da985c203904a48e2e90804ae217334dde2b905c57e'}

Where feasible, we will use Linux and networking related examples to
make explanation easier.

===================================     ========
Field                                   Descripton
===================================     ========
``agent``                               Agent or application name. If your agent script is designed to collect server performance data, you could name it 'server_performance'. Each server performance agent would therefore report the same agent value.
``timeseries``                          TimeSeries data follows
``timeseries[label]``                   A short label defining what the data is about.
``timeseries[label][base_type]``        Defines the type of data. The values are basesd on the SNMP standard. Values include: `0` for relatively unchanging alphanumeric data, which could include things like the version of an operating system; `1` for non-incremental, point-in-time numeric data such as temperature, speed, process count; `32` for numeric data that increments using a 32 bit counter such as bytes through a network interface since the device booted; `64` for 64 bit counter numeric data.
``timeseries[label][description]``      Description of the data, such as 'temperature data'
``timeseries[label][data]``             Data related to the labels. It is a list of lists. Each list has three fields `[index, value, source]`. The `index` value is a unique, unchangeable identifier for the source of the data, this is preferrably numeric such as an interface index number, but could also be string information such as an interface name or disk partition mount point. The `value` is the value of the data recorded. The `source` is a description of the source of the data to make it more recognizable when the data is eventually presented to your users. This could be `interface eth0` versus a plain `eth0`
``devicename``                          Devicename of the **device** sending the data. For phone apps, this could be set to a phone number of SIM ID.
``timestamp``                           Epoch **UTC** time when data was generated. This must be an integer.
``agent_id``                            A unique, unchanging identifier for the **application** sending the data.
===================================     ========

How to Create Agents Using Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you installed ``infoset-ng`` you probably ran the ``bin/tools/test_installation.py`` test script. This script emulates an agent and uses the classess in the ``infoset/reference/reference.py`` file to create the required JSON. Refer to this code when creating your agents.


Retrieving Data from the API
----------------------------
This section covers how to retrieve data from the API. First we cover some of the basics.

Overview
~~~~~~~~
Retrieving data from infoset is easy. Add the prefix ``http://SERVER_IP:6000`` to all the examples below to get data from your instance of ``infoset-ng``

You can test each route using the command:

::

    $ curl http://SERVER_IP:6000/route



The json fields in the results received from the API are explained in the ``infoset/db/db_orm.py`` file.


Database Table Names
^^^^^^^^^^^^^^^^^^^^

It is important to understand the purpose of each database table as they
are used in the routes. The structure of each table can be seen by
reviewing the ``db_orm.py`` file in the ``infoset.db`` module.

======================  ==============
Table                   Descripton
======================  ==============
``iset_agent``          Data on the agents that have posted information to the API
``iset_deviceagent``    The same agent could be installed on multiple devices. This table tracks which unique device and agent combination have posted information to the API
``iset_device``         Tracks all the devices that have posted information to the API
``iset_datapoint``      Stores metadata on the various datapoints that agents report on. A datapoint ID is unique throughout the system
``iset_data``           Stores the actual data for each datapoint
``iset_billcode``       Stores data on the billing code for datapoints. Useful for financial accounting.
``iset_department``     Stores data on the departments to which the billing code should be applied. Useful for financial accounting.
======================  ==============

Routes
~~~~~~

Data is retrieved by making HTTP requests to well known URIs or ``routes``. These are covered next.

Route /infoset/api/v1/agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive data on all agents that have ever posted data
to the API. It is returned in the form of a list of lists.

=========================   ======
Field                       Description
=========================   ======
``exists``                  True if the agent exists, False if not
``enabled``                 True if enabled, False if disabled
``id_agent``                The Agent ID
``idx_agent``               The unique index value of the agent in the database
``name``                    The agent name
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/agents

    [
      {
        "enabled": true,
        "exists": true,
        "id_agent": "ece739a93cca2c8e5444507990158b05b7d890d5798dc273578382d171bf6500",
        "idx_agent": 2,
        "last_timestamp": 1480570200,
        "name": "linux_in"
      },
      {
        "enabled": true,
        "exists": true,
        "id_agent": "1b3c081ba928d8a1ebb16084f23e55b972b0cda1737b0449853b591f4c84ad42",
        "idx_agent": 3,
        "last_timestamp": 1480570200,
        "name": "_garnet"
      },
    ]


Route /infoset/api/v1/agents/``<idx_agent>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific agent index value.

=========================   ======
Field                       Description
=========================   ======
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_agent``                The unique Agent ID
``idx_agent``               The unique index of the agent in the database
``devicename``              Unique devicename in the `infoset-ng` database
``name``                    The agent name
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/agents/3

    {
      "enabled": true,
      "exists": true,
      "id_agent": "70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557",
      "idx_agent": 3,
      "last_timestamp": 1480611300,
      "name": "linux_in"
    }
    $


Route /infoset/api/v1/agents?id_agent=<id_agent>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific ``id_agent`` value as a list.

=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``base_type``               Base type of the data
``billable``                True if billable, False if not.
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_agent``               The unique index of the agent that reported on this datapoint
``idx_billcode``            The index of the billing code to be applied to the datapoint
``idx_department``          The index value of the department to which the billing code should be applied
``idx_device``              The unique index of the device in the database
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
=========================   ======

Example:

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/agents?id_agent=70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557"

    [{
      "enabled": true,
      "exists": true,
      "id_agent": "70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557",
      "idx_agent": 3,
      "last_timestamp": 1480611600,
      "name": "linux_in"
    }]
    $


Route /infoset/api/v1/deviceagents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same agent could be installed on multiple devices. This route
returns data that tracks each unique device and agent combination have
posted information to the API. It is returned as a list of dicts.

=========================   ======
Field                       Description
=========================   ======
idx_agent                   The index value of the agent
idx_device                  The index value of the device
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/deviceagents

    [
      {
        "idx_agent": 1,
        "idx_device": 1
      },
      {
        "idx_agent": 2,
        "idx_device": 2
      },
      {
        "idx_agent": 3,
        "idx_device": 2
      },
      {
        "idx_agent": 4,
        "idx_device": 2
      }
    ]
    $


Route /infoset/api/v1/deviceagents/``idx_deviceagent``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same agent could be installed on multiple devices. This route
returns data that tracks each unique device and agent combination have
posted information to the API, filtered by ``idx_deviceagent``. It is returned as a list of dicts.

=========================   ======
Field                       Description
=========================   ======
idx_agent                   The index value of the agent
idx_device                  The index value of the device
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/deviceagents

    [
      {
        "idx_agent": 1,
        "idx_device": 1
      },
      {
        "idx_agent": 2,
        "idx_device": 2
      },
      {
        "idx_agent": 3,
        "idx_device": 2
      },
      {
        "idx_agent": 4,
        "idx_device": 2
      }
    ]
    $


Route /infoset/api/v1/devices/``<idx_device>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific device index value.

=========================   ======
Field                       Description
=========================   ======
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``devicename``              Unique devicename in the``infoset-ng`` database
``idx_device``              The unique index of the device in the database
=========================   ======


Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/devices/2

    {
      "description": null,
      "enabled": true,
      "exists": true,
      "devicename": "afimidis",
      "idx_device": 2x
    }
    $


Route /infoset/api/v1/datapoints/``<idx_datapoint>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific datapoint index value
value.

Please read section on the API's ``/infoset/api/v1/receive`` route for
further clarification of the field description in the table below.


=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``base_type``               Base type of the data
``billable``                True if billable, false if not.
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_agent``               The unique index of the agent that reported on this datapoint
``idx_billcode``            The index of the billing code to be applied to the datapoint
``idx_department``          The index value of the department to which the billing code should be applied
``idx_device``              The unique index of the device in the database
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
``timefixed_value``         Some datapoints may track unchanging numbers such as the version of an operating system. This value is placed here if the base_type is `0```
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/datapoints/2

    {
      "agent_label": "cpu_count",
      "agent_source": null,
      "base_type": 1,
      "billable": false,
      "enabled": true,
      "exists": true,
      "id_datapoint": "fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f",
      "idx_agent": 2,
      "idx_billcode": 1,
      "idx_datapoint": 2,
      "idx_department": 1,
      "idx_device": 2,
      "last_timestamp": 1480611600,
      "timefixed_value": null
    }
    $


Route /infoset/api/v1/datapoints?id_datapoint=<id_datapoint>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific id_datapoint value
value.

Please read section on the API's ``/infoset/api/v1/receive`` route for
further clarification of the field description in the table below.


=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``base_type``               Base type of the data
``billable``                True if billable, false if not.
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_agent``               The unique index of the agent that reported on this datapoint
``idx_billcode``            The index of the billing code to be applied to the datapoint
``idx_department``          The index value of the department to which the billing code should be applied
``idx_device``              The unique index of the device in the database
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
``timefixed_value``         Some datapoints may track unchanging numbers such as the version of an operating system. This value is placed here if the base_type is `0```
=========================   ======

Example:

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/datapoints?id_datapoint=fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f"

    {
      "agent_label": "cpu_count",
      "agent_source": null,
      "base_type": 1,
      "billable": false,
      "enabled": true,
      "exists": true,
      "id_datapoint": "fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f",
      "idx_agent": 2,
      "idx_billcode": 1,
      "idx_datapoint": 2,
      "idx_department": 1,
      "idx_device": 2,
      "last_timestamp": 1480611600,
      "timefixed_value": null
    }
    $


Route /infoset/api/v1/datapoints?idx_deviceagent=<idx_deviceagent>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific idx_deviceagent value
value.

Please read section on the API's ``/infoset/api/v1/receive`` route for
further clarification of the field description in the table below.


=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``base_type``               Base type of the data
``billable``                True if billable, false if not.
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_deviceagent``         The unique index of the device agent that reported on this datapoint
``idx_billcode``            The index of the billing code to be applied to the datapoint
``idx_department``          The index value of the department to which the billing code should be applied
``idx_device``              The unique index of the device in the database
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
``timefixed_value``         Some datapoints may track unchanging numbers such as the version of an operating system. This value is placed here if the base_type is `0```
=========================   ======

Example:

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/datapoints?idx_deviceagent=2"

    {
      "agent_label": "cpu_count",
      "agent_source": null,
      "base_type": 1,
      "billable": false,
      "enabled": true,
      "exists": true,
      "id_datapoint": "fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f",
      "idx_deviceagent": 2,
      "idx_billcode": 1,
      "idx_datapoint": 2,
      "idx_department": 1,
      "idx_device": 2,
      "last_timestamp": 1480611600,
      "timefixed_value": null
    }
    $


Route /infoset/api/v1/datapoints/all/summary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves dummary information about all datapoints.

Please read section on the API's ``/infoset/api/v1/receive`` route for
further clarification of the field description in the table below.


=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``devicename``              Unique devicename in the `infoset-ng` database
``id_agent``                The unique Agent ID
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_deviceagent``         The unique index of the deviceagent in the database
``name``                    The agent name
=========================   ======

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/datapoints/all/summary
    [
      {
        "agent_label": "system",
        "agent_source": null,
        "devicename": "palisadoes",
        "id_agent": "f32eda632703ac9d94d80b43d5dd54d0198cd0dabf541dae97b94e5b75b851d5",
        "idx_datapoint": 417,
        "idx_deviceagent": 4,
        "name": "remote_linux_passive"
      },
      {
        "agent_label": "version",
        "agent_source": null,
        "devicename": "palisadoes",
        "id_agent": "f32eda632703ac9d94d80b43d5dd54d0198cd0dabf541dae97b94e5b75b851d5",
        "idx_datapoint": 418,
        "idx_deviceagent": 4,
        "name": "remote_linux_passive"
      }
    ]
    $


Route /infoset/api/v1/datapoints&id_datapoint=``<id_datapoint>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route retrieves information for a specific datapoint ID value
value.

Please read section on the API's ``/infoset/api/v1/receive`` route for
further clarification of the field description in the table below.

=========================   ======
Field                       Description
=========================   ======
``agent_label``             Label that the agent assigned to the datapoint
``agent_source``            The source of the data
``base_type``               Base type of the data
``billable``                True if billable, false if not.
``enabled``                 True if enabled, False if not
``exists``                  True if the requested index value exists in the database
``id_datapoint``            The unique datapoint ID
``idx_datapoint``           The unique datapoint index
``idx_agent``               The unique index of the agent that reported on this datapoint
``idx_billcode``            The index of the billing code to be applied to the datapoint
``idx_department``          The index value of the department to which the billing code should be applied
``idx_device``              The unique index of the device in the database
``last_timestamp``          The **UTC** timestamp of the the most recent data posted by the agent to the API
``timefixed_value``         Some datapoints may track unchanging numbers such as the version of an operating system. This value is placed here if the base_type is `0```
=========================   ======

Example:

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/datapoints?id_datapoint=fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f"

    {
      "agent_label": "cpu_count",
      "agent_source": null,
      "base_type": 1,
      "billable": false,
      "enabled": true,
      "exists": true,
      "id_datapoint": "fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f",
      "idx_agent": 2,
      "idx_billcode": 1,
      "idx_datapoint": 2,
      "idx_department": 1,
      "idx_device": 2,
      "last_timestamp": 1480612500,
      "timefixed_value": null
    }
    $


Route /infoset/api/v1/devices/``<idx_device>``/agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive data on all the agents that have reported data
from a specific device. The agent data returned are their index values,
and the query is done based on the index of the device.

Example:

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/devices/2/agents

    [
      2,
      3,
      4
    ]
    $


Route /infoset/api/v1/lastcontacts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

Data is queried starting from 10X the interval value in your configuration file seconds ago until the present.


=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/lastcontacts

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 60370900.0
      },

    ...
    ...
    ...
    ...
    ...
    ...

      {
        "idx_datapoint": 417,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 418,
        "timestamp": 1483629900,
        "value": 60370900.0
      }
    ]


Route /infoset/api/v1/lastcontacts?secondsago=<seconds>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

The query starts looking for contacts as of ``secondsago`` seconds ago.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts?secondsago=3600"

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 60370900.0
      },

    ...
    ...
    ...
    ...
    ...
    ...

      {
        "idx_datapoint": 417,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 418,
        "timestamp": 1483629900,
        "value": 60370900.0
      }
    ]


Route /infoset/api/v1/lastcontacts?ts_start=``timestamp``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

A starting **UTC** timestamp needs to be provided. Searches for contacts are made from starting at this time until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts?ts_start=0"

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 60370900.0
      },

    ...
    ...
    ...
    ...
    ...
    ...

      {
        "idx_datapoint": 417,
        "timestamp": 1483629900,
        "value": 60370900.0
      },
      {
        "idx_datapoint": 418,
        "timestamp": 1483629900,
        "value": 60370900.0
      }
    ]


Route /infoset/api/v1/lastcontacts/id_agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

Data is queried starting from 10X the interval value in your configuration file seconds ago until the present.


=========================   ======
Field                       Description
=========================   ======
``devicename``              The name of the device generating the data
``name``                    The name of the agent generating the data
``id_agent``                The ID of the agent generating the data
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/lastcontacts/id_agents

    [
      {
        "devicename": "name_1",
        "id_agent": "bec9ba91e14804001e037fa4f52c94fb1ef027d04e1b86f6a74ab36e3b073609",
        "name": "Agent_Name",
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500,
            "value": 1.8191
          },
          "agent_label_2": {
            "timestamp": 1487377500,
            "value": 1.8694
          }
        }
      },
      {
        "devicename": "name_2", 
        "id_agent": "e33ce6311cf95c6264c6777323e9c717220b19ccad7b6da1877384e7fb3364e7", 
        "name": "Agent_Name", 
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500, 
            "value": 1.61078
          }, 
          "agent_label_2": {
            "timestamp": 1487377500, 
            "value": 1.54421
          }
        }
      }
    ]


Route /infoset/api/v1/lastcontacts/id_agents?secondsago=<seconds>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

The query starts looking for contacts as of ``secondsago`` seconds ago.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts/id_agents``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``devicename``              The name of the device generating the data
``name``                    The name of the agent generating the data
``id_agent``                The ID of the agent generating the data
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/id_agents?secondsago=3600"

    [
      {
        "devicename": "name_1",
        "id_agent": "bec9ba91e14804001e037fa4f52c94fb1ef027d04e1b86f6a74ab36e3b073609",
        "name": "Agent_Name",
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500,
            "value": 1.8191
          },
          "agent_label_2": {
            "timestamp": 1487377500,
            "value": 1.8694
          }
        }
      },
      {
        "devicename": "name_2", 
        "id_agent": "e33ce6311cf95c6264c6777323e9c717220b19ccad7b6da1877384e7fb3364e7", 
        "name": "Agent_Name", 
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500, 
            "value": 1.61078
          }, 
          "agent_label_2": {
            "timestamp": 1487377500, 
            "value": 1.54421
          }
        }
      }
    ]
    

Route /infoset/api/v1/lastcontacts/id_agents?ts_start=``timestamp``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive **all** the most recently posted data values.

A starting **UTC** timestamp needs to be provided. Searches for contacts are made from starting at this time until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts/id_agents``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``devicename``              The name of the device generating the data
``name``                    The name of the agent generating the data
``id_agent``                The ID of the agent generating the data
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/id_agents?ts_start=0"

    [
      {
        "devicename": "name_1",
        "id_agent": "bec9ba91e14804001e037fa4f52c94fb1ef027d04e1b86f6a74ab36e3b073609",
        "name": "Agent_Name",
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500,
            "value": 1.8191
          },
          "agent_label_2": {
            "timestamp": 1487377500,
            "value": 1.8694
          }
        }
      },
      {
        "devicename": "name_2", 
        "id_agent": "e33ce6311cf95c6264c6777323e9c717220b19ccad7b6da1877384e7fb3364e7", 
        "name": "Agent_Name", 
        "timeseries": {
          "agent_label_1": {
            "timestamp": 1487377500, 
            "value": 1.61078
          }, 
          "agent_label_2": {
            "timestamp": 1487377500, 
            "value": 1.54421
          }
        }
      }
    ]


Route /infoset/api/v1/lastcontacts/``<idx_deviceagent>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Searches for contacts are made starting from an hour ago to the present. from a specific Device Agent combination. The query is done based on the device's deviceagent index.

Data is queried starting from 10X the interval value in your configuration file seconds ago until the present.


=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC**  timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/lastcontacts/2

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]


Route /infoset/api/v1/lastcontacts/``<idx_deviceagent>``?secondsago=``seconds``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive the most recently posted data values from a specific Device Agent combination. The query is done based on the device's deviceagent index.

Data is queried starting from 10X the interval value in your configuration file seconds ago until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/2?secondsago=3600"

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]
    $


Route /infoset/api/v1/lastcontacts/``<idx_deviceagent>``?ts_start=``timestamp``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive the most recently posted data values from a specific Device Agent combination. The query is done based on the device's deviceagent index.

A starting **UTC** timestamp needs to be provided. Searches for contacts are made from starting at this time until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/2?ts_start=0"

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]
    $


Route /infoset/api/v1/lastcontacts/devicenames/``<devicename>``/id_agents/``<id_agent>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Searches for contacts are made starting from an hour ago to the present. from a specific ``devicename`` and ``id_agent`` combination.

Data is queried starting from 10X the interval value in your configuration file seconds ago until the present.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC** timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl http://SERVER_IP:6000/infoset/api/v1/devicenames/_INFOSET_TEST_/id_agents/558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]


Route /infoset/api/v1/lastcontacts/devicenames/``<devicename>``/id_agents/``<id_agent>``
?ts_start=``timestamp`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive the most recently posted data values from a specific ``devicename`` and ``id_agent`` combination.

A starting **UTC** timestamp needs to be provided. Searches for contacts are made from starting at this time until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts/devicenames/<devicename>/id_agents/<id_agent>``, which is the preferred method of getting this data.

=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC**  timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/devicenames/_INFOSET_TEST_/id_agent/558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749/?ts_start=0"
    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]
    $


Route /infoset/api/v1/lastcontacts/devicenames/``<devicename>``/id_agents/``<id_agent>``
?secondsago=``seconds``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This route will retreive the most recently posted data values from a specific ``devicename`` and ``id_agent`` combination.

A starting **UTC** timestamp needs to be provided. Searches for contacts are made from starting at this time until the present.

This route does not use the cache as efficiently as ``/infoset/api/v1/lastcontacts/devicenames/<devicename>/id_agents/<id_agent>``, which is the preferred method of getting this data.


=========================   ======
Field                       Description
=========================   ======
``idx_datapoint``           The datapoint index value
``timestamp``               **UTC**  timestamp of the most recent contact
``value``                   Value of the datapoint reading at the timestamp's point in time
=========================   ======

::

    $ curl "http://SERVER_IP:6000/infoset/api/v1/lastcontacts/devicenames/_INFOSET_TEST_/id_agent/558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749/?secondsago=3600"

    [
      {
        "idx_datapoint": 2,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 3,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 4,
        "timestamp": 1483629900,
        "value": 9.0
      },
      {
        "idx_datapoint": 5,
        "timestamp": 1483629900,
        "value": 9.0
      }
    ]
    $

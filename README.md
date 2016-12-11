# infoset-ng
`infoset-ng` is a lightweight Python 3 based REST API that stores and/or retrieves timestamped data. It runs on Linux.

We strongly recommend that you read everything on this page before installing `infoset-ng`
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

  - [Features](#features)
  - [Inspiration / History](#inspiration--history)
  - [Oversight](#oversight)
  - [Dependencies](#dependencies)
    - [Ubuntu / Debian / Mint](#ubuntu--debian--mint)
    - [Fedora](#fedora)
  - [Installation](#installation)
    - [Testing Installation](#testing-installation)
  - [Configuration](#configuration)
    - [Logrotate Configuration](#logrotate-configuration)
  - [Operation](#operation)
    - [Ingester Operation](#ingester-operation)
      - [Testing Ingester Operation](#testing-ingester-operation)
      - [Ingester Protection Using agentsd.py](#ingester-protection-using-agentsdpy)
    - [API Operation](#api-operation)
  - [Using the API](#using-the-api)
    - [Posting Data to the API](#posting-data-to-the-api)
      - [Route /infoset/api/v1.0/receive/`<id_agent>`](#route-infosetapiv10receiveid_agent)
    - [Retrieving Data from the API](#retrieving-data-from-the-api)
      - [Route /infoset/api/v1.0/db/agent/getallagents](#route-infosetapiv10dbagentgetallagents)
      - [Route /infoset/api/v1.0/db/deviceagent/alldeviceindices](#route-infosetapiv10dbdeviceagentalldeviceindices)
      - [Route /infoset/api/v1.0/db/deviceagent/getalldeviceagents](#route-infosetapiv10dbdeviceagentgetalldeviceagents)
      - [Route /infoset/api/v1.0/db/device/getidxdevice/`<idx_device>`](#route-infosetapiv10dbdevicegetidxdeviceidx_device)
      - [Route /infoset/api/v1.0/db/device/getidxagent/`<idx_agent>`](#route-infosetapiv10dbdevicegetidxagentidx_agent)
      - [Route /infoset/api/v1.0/db/agent/getidagent/`<id_agent>`](#route-infosetapiv10dbagentgetidagentid_agent)
      - [Route /infoset/api/v1.0/db/datapoint/getidxdatapoint/`<idx_datapoint>`](#route-infosetapiv10dbdatapointgetidxdatapointidx_datapoint)
      - [Route /infoset/api/v1.0/db/datapoint/getiddatapoint/`<idx_datapoint>`](#route-infosetapiv10dbdatapointgetiddatapointidx_datapoint)
      - [Route /infoset/api/v1.0/db/deviceagent/agentindices/`<idx_device>`](#route-infosetapiv10dbdeviceagentagentindicesidx_device)
      - [Route /infoset/api/v1.0/db/datapoint/charted/`<idx_device>`/`<idx_agent>`](#route-infosetapiv10dbdatapointchartedidx_deviceidx_agent)
      - [Route /infoset/api/v1.0/db/datapoint/timefixed/`<idx_device>`/`<idx_agent>`](#route-infosetapiv10dbdatapointtimefixedidx_deviceidx_agent)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
  - [Contribute](#contribute)
  - [Mailing list](#mailing-list)
  - [New Features](#new-features)
  - [Design Overview](#design-overview)
  - [Sample Output](#sample-output)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Features
`infoset-ng` has the following features:

1. Open source.
2. Written in python, a modern language.
3. Easy configuration.
4. Usee the well known Flask webserver for accepting data and responding to requests.
7. `infoset-ng` has a number of fault tolerant features aimed at making it resilient in unstable computing environemnts.
 1. MariaDB / MySQL database backend
 2. Database connection pooling to reduce database load.
 2. Ingestion of data supports parallel multiprocessing for maximum speed.
 3. The infoset-ng-ng API server can tolerate the loss of communication with its database by caching the data locally until the database returns online.
 3. The `infoset-ng` configuration is entirely stored in files. This allows it to collect data in the absense of a database, such as during maintenance or an outage.
 4. Backups are simple. Just save the entire contents of the `infoset-ng` directory tree including hidden files, and save a copy of the database for your performance data.

We are always looking for more contributors!

## Inspiration / History
The `infoset-ng` project originally took inspiration from the SourceForge based `switchmap` project. `switchmap` was written in PERL and designed to create tabular representations of network topologies. Early versions of `infoset` eventually had expanded features which included the polling of network devices for real time performance data. This data was presented via a web interface. The code became cumbersome and the original `infoset` was split into three componet parts.

1. `infoset-ng`: An API for storing and retrieving real time data.
2. `garnet`: A network / server performance charting web application that uses various types of agents for collecting real time data. `garnet` uses `infoset-ng` to store its data.
3. `switchmap-ng` A python 3 based feature equivalent version of `switchmap`.

Each of these projects resides on the University of the West Indies Computing Society's GitHub account.

## Oversight
`infoset-ng` is a student collaboration between:

1. The University of the West Indies Computing Society. (Kingston, Jamaica)
2. The University of Techology, IEEE Student Branch. (Kingston, Jamaica)
3. The Palisadoes Foundation http://www.palisadoes.org

And many others.

## Dependencies
The dependencies required for successful `infoset-ng` installation are `python3` and python's `pip3`.

### Ubuntu / Debian / Mint

The commands for installing the dependencies are:
```
# sudo apt-get install python3 python3-pip python3-dev python3-yaml
# pip3 install --user sqlalchemy
```

### Fedora
The commands for installing the dependencies are:
```
# sudo dnf install python3 python3-pip python3-dev python3-yaml
# pip3 install --user sqlalchemy
```
## Installation
Installation is simple. The first thing to do is verify that your system is running python 3.5 or higher. If not, you will need to upgrade. Use this command to check:
```
$ python3 --version
```

Next create the MySQL or MariaDB database.
```
$ mysql -u root -p
password:
mysql> create database infoset-ng;
mysql> grant all privileges on infoset-ng.* to infoset-ng@"localhost" identified by 'PASSWORD';
mysql> flush privileges;
mysql> exit;
```
Now clone the repository and copy the sample configuration file to its final location.
```
$ git clone https://github.com/PalisadoesFoundation/infoset-ng
$ cd infoset-ng
$ export PYTHONPATH=`pwd`
$ cp examples/etc/* etc/
```
Edit the database credential information in the server section of the `etc/config.yaml` file. Update the configured database password.
```
$ vim etc/config.yaml
```
Create the directories that `infoset-ng` will use for its working files.
```
$ sudo mkdir -p /opt/infoset-ng
$ sudo chown -R $USER /opt/infoset-ng
$ mkdir -p /opt/infoset-ng/log
$ mkdir -p /opt/infoset-ng/cache
```
Run the install scripts.
```
$ pip3 install --user sqlalchemy
$ python3 setup.py
$ source ~/.bashrc
$ sudo make
$ source venv/bin/activate
$ sudo make install
```

Start the `infoset-ng` API.

```
$ ./server.py
```

### Testing Installation
It is important to have a valid configuration file in the `etc/` directory before starting data collection. See the `Configuration` section of this document.

You can test whether your configuration works by:

1. Starting the API (Important, see the `Operation` section of this document)
2. Running the `bin/tools/test_installation.py` script

Here is an example of a successful test:
```
$ bin/tools/test_installation.py
2016-12-03 18:12:56,640 - infoset_console - INFO - [peter] (1054S): Successfully posted test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749
2016-12-03 18:12:56,656 - infoset_console - INFO - [peter] (1054S): Successfully retrieved test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

OK

$
```

## Configuration
It is important to have a valid configuration file in the `etc/` directory before starting data collection.

The `examples/etc` directory includes a sample file that can be copied to the `/etc` directory and edited.

The `README.md` file in the `examples/etc` directory explains what each parameter does. You can easily view this `README.md` file on the web by visiting the  `examples/etc` directory on GitHub.

### Logrotate Configuration
The `examples/linux/logrotate/infoset-ng` file is a working logrotate configuration to rotate the log files that infoset-ng generates. The log file data can be extensive and adding the logrotate file to your system is highly recommended.

```
$ sudo cp examples/linux/logrotate/infoset-ng /etc/logrotate.d
```
Instructions on how to operate `infoset-ng` follow.

## Operation
`infoset-ng` has two major components. These are:

1. **The API**: Stores and retrieves data from the database via REST API calls. Received data is placed in the cache directory defined in the configuration.
1. **The Ingester**: Periodically retrieves data from the cache files and places it in the database.

Explanations of how run each component will be given next.

**NOTE!** You must have a valid configuration file placed in the `etc/` directory before activating data collection.

### Ingester Operation

The steps for running the ingester are as follows.

1. Make sure you have a valid configuration file in the `etc/` directory
3. Start the `bin/ingestd.py` script

The ingester can be started like this:
```
$ bin/ingestd.py --start
```
The ingester can be stopped like this:
```
$ bin/ingestd.py --stop
```
You can get the status of the ingester like this:
```
$ bin/ingestd.py --status
```
You may want to run the `bin/agentsd.py` script too. This will be covered next.

#### Testing Ingester Operation
You can test the operation of the API by using the `curl` command which is often used to test basic website functionality. The example below shows how. Replace `SERVER_IP` with the IP address or fully qualified DNS name.

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0
infoset-ng API Operational.
$
```
The `curl` response should be`infoset-ng API Operational` if successful.

#### Ingester Protection Using agentsd.py
The `bin/agentsd.py` script automatically starts the ingester and restarts it whenever ingester failure is detected. `bin/agentsd.py` will only attempt to do so if the ingester agent is  `enabled` in the configuration file. `bin/agentsd.py` will immediately stop the ingester agent if it is `disabled` in the configuration file.

The script can be started like this:
```
$ bin/agentsd.py --start
```
The script can be stopped like this:
```
$ bin/agentsd.py --stop
```
You can get the status of the script like this:
```
$ bin/agentsd.py --status
```
### API Operation
The `server.py` script controls the API. The script can be started like this:
```
$ ./server.py
```
Make sure you have a valid configuration file in the `etc/` directory

## Using the API
This section outlines how to use the API
### Posting Data to the API
Posting data to the API is. Add the prefix `http://SERVER_IP:6000` to all the examples below to update data in your instance of `infoset-ng`

#### Route /infoset/api/v1.0/receive/`<id_agent>`

JSON data needs to be posted to the `http://SERVER_IP:6000/infoset/api/v1.0/receive/<id_agent>` URL where `id_agent` is a unique identifier of the software script that is posting the data. This `id_agent` must be unique and consistent for each **script** or **application** posting data to `infoset-ng`. For example, if you have three data collection scripts running across two devices, then each script must report a unique `id_agent`, three unique IDs in total. We suggest using a hash of a random string to generate your `id_agent`.  There is a 512 character limit on the size of the `agent_id`.

The example below explains the expected JSON format:

```
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
```

Where feasible, we will use Linux and networking related examples to make explantion easier.

| Field | Descripton |
|--------|--------|
|agent|Agent or application name. If your agent script is designed to collect server performance data, you could name it 'server_performance'. Each server performance agent would therefore report the same agent value.|
|timeseries|TimeSeries data follows|
|timeseries[label]| A short label defining what the data is about.|
|timeseries[label][base_type]| Defines the type of data. The values are basesd on the SNMP standard. Values include: `0` for relatively unchanging alphanumeric data, which could include things like the version of an operating system; `1` for non-incremental, point-in-time numeric data such as temperature, speed, process count; `32` for numeric data that increments using a 32 bit counter such as bytes through a network interface since the device booted; `64` for 64 bit counter numeric data.|
|timeseries[label][description]|Description of the data, such as 'temperature data'|
|timeseries[label][data]|Data related to the labels. It is a list of lists. Each list has three fields `[index, value, source]`. The `index` value is a unique, unchangeable identifier for the source of the data, this is preferrably numeric such as an interface index number, but could also be string information such as an interface name or disk partition mount point. The `value` is the value of the data recorded. The `source` is a description of the source of the data to make it more recognizable when the data is eventually presented to your users. This could be `interface eth0` versus a plain `eth0` |
|devicename|Devicename of the **device** sending the data. For phone apps, this could be set to a phone number of SIM ID.
|timestamp| Epoch time when data was generated. This must be an integer.|
|agent_id| A unique, unchanging identifier for the **application** sending the data.|

### Retrieving Data from the API
Retrieving data from infoset is easy. Add the prefix `http://SERVER_IP:6000` to all the examples below to get data from your instance of `infoset-ng`

You can test each route using the command:
```
$ curl http://SERVER_IP:6000/route
```
####API Route Naming Scheme
The API routes for retrieving database data have a simple naming scheme.
```
/db/<table_name>/<function or class>/<other arguments>
```
Here's some insight into this scheme.

| Field | Descripton |
|--------|--------|
|table name| Name of the table in the MySQL database|
|funtion or class| The `infoset.db` python module contains files related to each database table. The naming convention is `db_<table_name>`. Each file has funtions or classes in them. These are the names used in the API routes. You can review the files in the module for more details.|
|other arguments|Required module Class or function arguments|

####Database Table Names
It is important to understand the purpose of each database table as they are used in the routes. The structure of each table can be seen by reviewing the `db_orm.py` file in the `infoset.db` module.

| Table | Descripton |
|--------|--------|
|iset_agent| Data on the agents that have posted information to the API|
|iset_deviceagent| The same agent could be installed on multiple devices. This table tracks which unique device and agent combination have posted information to the API|
|iset_device|Tracks all the devices that have posted information to the API|
|iset_datapoint|Stores metadata on the various datapoints that agents report on. A datapoint ID is unique throughout the system|
|iset_data| Stores the actual data for each datapoint|
|iset_billcode| Stores data on the billing code for datapoints. Useful for financial accounting.|
|iset_department| Stores data on the departments to which the billing code should be applied. Useful for financial accounting.|


#### Route /infoset/api/v1.0/db/agent/getallagents
This route will retreive data on all agents that have ever posted data to the API. It is returned in the form of a list of lists.

| Field | Descripton |
|--------|--------|
|exists| True if the agent exists, False if not|
|enabled| True if enabled, False if disabled|
|id_agent| The Agent ID|
|idx_agent| The unique index value of the agent in the database|
|name| The agent name|
|last_timestamp| The timestamp of the the most recent data posted by the agent to the API|

Example:
```
curl http://SERVER_IP:6000/infoset/api/v1.0/db/agent/getallagents
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

```
#### Route /infoset/api/v1.0/db/deviceagent/alldeviceindices
This route will retreive data on all devices that have posted data to the API. It is returned as a list of index values.

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/deviceagent/alldeviceindices
[
  1,
  2
]
$
```
#### Route /infoset/api/v1.0/db/deviceagent/getalldeviceagents
The same agent could be installed on multiple devices. This route returns data that tracks each  unique device and agent combination have posted information to the API. It is returned as a list of dicts.

| Field | Descripton |
|--------|--------|
|idx_agent| The index value of the agent|
|idx_device| The index value of the device|

Example:
```
curl http://SERVER_IP:6000/infoset/api/v1.0/db/deviceagent/getalldeviceagents
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
```
#### Route /infoset/api/v1.0/db/device/getidxdevice/`<idx_device>`
This route retrieves information for a specific device index value.

| Field | Descripton |
|--------|--------|
|description| Description of the device|
|enabled| True if enabled, False if not|
|exists| True if the requested index value exists in the database|
|devicename| Unique devicename in the `infoset-ng` database|
|idx_device| The unique index of the device in the database|
|ip_address| The IP address of the device|

Example:
```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/device/getidxdevice/2
{
  "description": null,
  "enabled": true,
  "exists": true,
  "devicename": "afimidis",
  "idx_device": 2,
  "ip_address": null
}
$
```
#### Route /infoset/api/v1.0/db/device/getidxagent/`<idx_agent>`
This route retrieves information for a specific agent index value.

| Field | Descripton |
|--------|--------|
|enabled| True if enabled, False if not|
|exists| True if the requested index value exists in the database|
|id_agent| The unique Agent ID|
|idx_agent| The unique index of the agent in the database|
|devicename| Unique devicename in the `infoset-ng` database|
|last_timestamp| The timestamp of the the most recent data posted by the agent to the API|

Example:
```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/agent/getidxagent/3
{
  "enabled": true,
  "exists": true,
  "id_agent": "70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557",
  "idx_agent": 3,
  "last_timestamp": 1480611300,
  "name": "linux_in"
}
$
```

#### Route /infoset/api/v1.0/db/agent/getidagent/`<id_agent>`
This route retrieves information for a specific id_agent value.

| Field | Descripton |
|--------|--------|
|enabled| True if enabled, False if not|
|exists| True if the requested index value exists in the database|
|id_agent| The unique Agent ID|
|idx_agent| The unique index of the agent in the database|
|devicename| Unique devicename in the `infoset-ng` database|
|last_timestamp| The timestamp of the the most recent data posted by the agent to the API|

Example:
```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/agent/getidagent/70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557
{
  "enabled": true,
  "exists": true,
  "id_agent": "70f2d9061f3ccc96915e19c13817c8207e2005d05f23959ac4c225b6a5bfe557",
  "idx_agent": 3,
  "last_timestamp": 1480611600,
  "name": "linux_in"
}
$
```
#### Route /infoset/api/v1.0/db/datapoint/getidxdatapoint/`<idx_datapoint>`
This route retrieves information for a specific datapoint index value value.

Please read section on the API's `/infoset/api/v1.0/receive` route for further clarification of the field description in the table below.

| Field | Descripton |
|--------|--------|
|agent_label| Label that the agent assigned to the datapoint|
|agent_source| The source of the data|
|base_type| Base type of the data|
|billable| True if billable, false if not.|
|enabled| True if enabled, False if not|
|exists| True if the requested index value exists in the database|
|id_datapoint| The unique datapoint ID|
|idx_datapoint| The unique datapoint index|
|idx_agent| The unique index of the agent that reported on this datapoint|
|idx_billcode| The index of the billing code to be applied to the datapoint|
|idx_department| The index value of the department to which the billing code should be applied|
|idx_device| The unique index of the device in the database|
|last_timestamp| The timestamp of the the most recent data posted by the agent to the API|

Example:

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/datapoint/getidxdatapoint/2
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
```
#### Route /infoset/api/v1.0/db/datapoint/getiddatapoint/`<idx_datapoint>`
This route retrieves information for a specific datapoint ID value value.

Please read section on the API's `/infoset/api/v1.0/receive` route for further clarification of the field description in the table below.

| Field | Descripton |
|--------|--------|
|agent_label| Label that the agent assigned to the datapoint|
|agent_source| The source of the data|
|base_type| Base type of the data|
|billable| True if billable, false if not.|
|enabled| True if enabled, False if not|
|exists| True if the requested index value exists in the database|
|id_datapoint| The unique datapoint ID|
|idx_datapoint| The unique datapoint index|
|idx_agent| The unique index of the agent that reported on this datapoint|
|idx_billcode| The index of the billing code to be applied to the datapoint|
|idx_department| The index value of the department to which the billing code should be applied|
|idx_device| The unique index of the device in the database|
|last_timestamp| The timestamp of the the most recent data posted by the agent to the API|
|timefixed_value| Some datapoints may track unchanging numbers such as the version of an operating system. This value is placed here if the base_type is `0`|

Example:

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/datapoint/getiddatapoint/fef5fb0c60f6ecdd010c99f14d120598d322151b9d942962e6877945f1f14b5f
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
```
#### Route /infoset/api/v1.0/db/deviceagent/agentindices/`<idx_device>`
This route will retreive data on all the agents that have reported data from a specific device. The agent data returned are their index values, and the query is done based on the index of the device.

Example:
```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/deviceagent/agentindices/2
[
  2,
  3,
  4
]
$
```
#### Route /infoset/api/v1.0/db/datapoint/charted/`<idx_device>`/`<idx_agent>`
This route will retreive **charted** datapoint data for a specific agent running on a specific device. The query is done based on the index of the device and the index of the agent.

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/datapoint/charted/2/2
[
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
    "last_timestamp": 1480612800,
    "timefixed_value": null
  },
  {
    "agent_label": "cpu_stats_ctx_switches",
    "agent_source": null,
    "base_type": 64,
    "billable": false,
    "enabled": true,
    "exists": true,
    "id_datapoint": "2339ea7eec2a5ea6f794c3790690c848c8e4a1828887b7570793d0ccc4c520fa",
    "idx_agent": 2,
    "idx_billcode": 1,
    "idx_datapoint": 3,
    "idx_department": 1,
    "idx_device": 2,
    "last_timestamp": 1480612800,
    "timefixed_value": null
  }, ]
  $
```
#### Route /infoset/api/v1.0/db/datapoint/timefixed/`<idx_device>`/`<idx_agent>`
This route will retreive **timefixed** datapoint data for a specific agent running on a specific device. The query is done based on the index of the device and the index of the agent.

```
$ curl http://SERVER_IP:6000/infoset/api/v1.0/db/datapoint/timefixed/2/2
[
  {
    "agent_label": "distribution",
    "agent_source": null,
    "base_type": 0,
    "billable": false,
    "enabled": true,
    "exists": true,
    "id_datapoint": "830b1b1430ded05383ece39e8bcd29efc2a9d696f46fe990526fec414b2ed90c",
    "idx_agent": 2,
    "idx_billcode": 1,
    "idx_datapoint": 125,
    "idx_department": 1,
    "idx_device": 2,
    "last_timestamp": 1480613100,
    "timefixed_value": "Ubuntu 16.04 xenial"
  },
  {
    "agent_label": "release",
    "agent_source": null,
    "base_type": 0,
    "billable": false,
    "enabled": true,
    "exists": true,
    "id_datapoint": "5b68e2718d14c6b705ed773e2cfd534a203330e1e739be437dfa026e9732255c",
    "idx_agent": 2,
    "idx_billcode": 1,
    "idx_datapoint": 126,
    "idx_department": 1,
    "idx_device": 2,
    "last_timestamp": 1480613100,
    "timefixed_value": "4.4.0-42-generic"
  },
  {
    "agent_label": "version",
    "agent_source": null,
    "base_type": 0,
    "billable": false,
    "enabled": true,
    "exists": true,
    "id_datapoint": "4b2bc6fe126d32ca0ea2489106f4d82d92f324606915f4021ed3c49d0c6555b1",
    "idx_agent": 2,
    "idx_billcode": 1,
    "idx_datapoint": 128,
    "idx_department": 1,
    "idx_device": 2,
    "last_timestamp": 1480613100,
    "timefixed_value": "#62-Ubuntu SMP Fri Oct 7 23:11:45 UTC 2016"
  }
]
$
```
# Troubleshooting
`infoset-ng` also includes a web interface. To start the server run `python3 server.py` then navigate to <http://localhost:5000>

# Next Steps
There are many dragons to slay and kingdoms to conquer!
## Contribute
Here are a few things to know.

1. Contributions are always welcome. Contact our team for more.
2. View our contributor guidelines here: https://github.com/PalisadoesFoundation/infoset-ng/blob/master/CONTRIBUTING.md
3. View our guidelines for committing code here: https://github.com/PalisadoesFoundation/infoset-ng/blob/master/COMMITTERS.md

## Mailing list
Our current mailing list is: https://groups.google.com/forum/#!forum/gdg-jamaica
## New Features
Visit our GitHub issues for a full list of features and bug fixes. https://github.com/PalisadoesFoundation/infoset-ng/issues
## Design Overview
Visit our wiki's `infoset-ng` document for the rationale of the design. http://wiki.palisadoes.org/index.php/infoset-ng
## Sample Output
Visit http://calico.palisadoes.org/infoset-ng to view `infoset-ng`'s latest stable web output.

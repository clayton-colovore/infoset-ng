# infoset Configuration Details

This page has detailed information on how to configure `infoset-ng`.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [infoset Configuration Samples](#infoset-configuration-samples)
- [Main Configuration](#main-configuration)
- [Agent Configuration](#agent-configuration)
  - [Sample Agent Configuration](#sample-agent-configuration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## infoset Configuration Samples

This `examples/etc` directory includes a sample file that can be edited. `infoset-ng` assumes all files in this directory only contains `infoset-ng` configuration files.

You must place your configuration file in the `etc/` directory as your permanent configuration file location.
## Main Configuration
This section of the configuration file governs the general operation of `infoset-ng`.
```
main:
    log_file: /opt/infoset/log/infoset.log
    web_log_file: /opt/infoset/log/web.log
    log_level: debug
    ingest_cache_directory: /opt/infoset/cache
    ingest_pool_size: 20
    interval: 300
    listen_address: 0.0.0.0
    bind_port: 6000
    sqlalchemy_pool_size: 10
    sqlalchemy_max_overflow: 10
    db_hostname: localhost
    db_username: infoset
    db_password: PASSWORD
    db_name: infoset
```
|Parameter|Description|
| --- | --- |
| main: | YAML key describing the server configuration.|
| `log_file:` | The name of the log file `infoset-ng` uses for logging backend activities|
| `web_log_file:` | The name of the log file `infoset-ng` uses for logging API activities|
| log_level: | Defines the logging level. `debug` level is the most verbose, followed by `info`, `warning` and `critical`|
| `ingest_cache_directory:` | Location where the agent data ingester will store its data in the event it cannot communicate with either the database or the server's API|
| `ingest_pool_size:` | The maximum number of threads used to ingest data into the database|
| `interval:` | The expected interval in seconds between updates to the database from systems posting to the infoset API. Data retieved from the API will be spaced `interval` seconds apart.|
| `listen_address:` | IP address the API will be using. The default is `0.0.0.0` or all available IP addresses|
| `bind_port:` | The TCP port the API will be listening on|
| `sqlalchemy_pool_size:`|The SQLAlchemy pool size. This is the largest number of connections that `infoset-ng` will be keep persistently with the MySQL database|
| `sqlalchemy_max_overflow:`|The SQLAlchemy maximum overflow size. When the number of connections reaches the size set in `sqlalchemy_pool_size`, additional connections will be returned up to this limit. This is the floating number of additional database connections to be made available. |
| `db_hostname:` | The devicename or IP address of the database server.|
| `db_username:` | The database username|
| `db_password:` | The database password|
| `db_name:` | The name of the database|

## Agent Configuration
An `infoset-ng` agent processes data in the background. Here is a list of configurable agents and their purpose.

|Agent|Description|
| --- | --- |
| `ingestd:` | Processes information received by the API. This data is placed in the database.|


### Sample Agent Configuration
In this example the `infoset-ng` ingester agent named `ingestd` is configured:
```
agents:
	...
    ...
    ...
    - agent_name: ingestd
      agent_enabled: True
      agent_filename: bin/ingestd.py
      monitor_agent_pid: True
```
|Parameter|Description|
| --- | --- |
| agents: | YAML key describing configured agents. All agents are listed under this key.|
| agent_name: | Name of the agent (Don't change)|
| agent_enabled: | True if enabled|
| agent_filename: | Name of the agent's filename (Don't change)|
| monitor_agent_pid: | Set to True if the agent monitor needs to monitor the PID file to determine whether the ingester has hung|

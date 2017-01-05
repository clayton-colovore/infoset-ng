Best Practices
==============

There are a number of best practices to consider when implementing ``infoset-ng``.

Use a Web Proxy Server
----------------------

``infoset-ng`` uses ``Gunicorn`` as lightweight webserver. The ``Gunicorn`` development team strongly recommends operating ``Gunicorn`` behind a proxy server.

Nginx Configuration
~~~~~~~~~~~~~~~~~~~

Although there are many HTTP proxies available, the ``Gunicorn`` team strongly advises that you use ``Nginx``.

According to their website: `If you choose another proxy server you need to make sure that it buffers slow clients when you use default Gunicorn workers. Without this buffering Gunicorn will be easily susceptible to denial-of-service.`

A sample configuration can be found in the ``examples/linux/nginx`` directory

We also advise that you harden your ``nginx`` installation to reduce security risks.

Apache Configuration
~~~~~~~~~~~~~~~~~~~~

This is the less preferred option. Use ``Nginx`` whenever possible.

A sample configuration can be found in the ``examples/linux/apache`` directory

We also advise that you harden your ``nginx`` installation to reduce security risks.

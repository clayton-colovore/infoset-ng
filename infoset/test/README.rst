About Unittests
===============

This is the UnitTest section of the project. All modifications to code
must have an associated functional unittest to reduce the risk of bugs.


Conventions
-----------

There are some conventions to be followed.

1. All files here start with the prefix ``test_`` that match the name of
   the file in a module whose classes, methods and functions need to be
   tested.
2. All unittest methods must start with the string ``test_`` to be
   recognized by the unittest class.
3. All unittest scripts must be able to successfully run independently
   of all others.
4. Database tests must:
5. Only be able to run on a database whose name begins with the string
   ``test_``. This is because database tests may be desctructive.
6. Create the required initial database state for tests to run
   correctly.

Running Tests
-------------

There are some important things to know beforehand.

1. You can run all tests by running ``_do_all_tests.py`` from the
   ``infoset/test`` directory
2. The database tests are destructive. You will need to create a
   separate ``infoset-ng`` database to run the tests. The database name
   must start with the string ``test_``
3. You can ensure that the unittests use a config.yaml file external to
   the default ``etc/`` directory by specifying a new configuration
   directory using the ``INFOSET_CONFIGDIR`` environment variable. This
   will allow you to run tests with a reduced risk of disrupting running
   ``infoset-ng`` instances.

Mocks
-----

Many of these unittests use Python Mocks. A detailed tutorial on Mocks
can be found here:
http://www.drdobbs.com/testing/using-mocks-in-python/240168251

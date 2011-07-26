2. ``net`` module
==============================================

This module provides classes used to actually connect to dAmn using
Twisted. The `ConnectionFactory` starts connections and handles
disconnects. The `ChatProtocol` handles basic IO operations on the
connection, but delegates most of the processing to an instance of the
:py:class:`Client <dAmnViper.base.Client>` class.

2.1 ``ConnectionFactory`` - Connection management
-------------------------------------------------
.. _connectionfactory:

.. autoclass:: dAmnViper.net.ConnectionFactory
    :members:

2.2. ``ChatProtocol`` - Input and Output piping for chat servers
----------------------------------------------------------------
.. _chatprotocol:

.. autoclass:: dAmnViper.net.ChatProtocol
    :members:


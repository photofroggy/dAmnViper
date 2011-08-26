1. ``base`` module
==============================================
This module provides the dAmnClient class, which acts as an API for
connecting to and interacting with deviantART.com's chatrooms. This is
achieved using Twisted.

``dAmnClient`` is built on top of the ``Client`` class, which provides the
basic functionality required to connect to a dAmn server. The ``dAmnClient``
class handles the server handshake and sets the right information for the
connection, so should be used instead of the ``Client`` class in most cases.

1.1. ``IChatClient`` - Basic client interface
---------------------------------------------
.. _clientinterface:

.. autoclass:: dAmnViper.base.IChatClient
    :members:


1.2. ``ChatClient`` - The base chat client API
----------------------------------------------
.. _baseclient:

.. autoclass:: dAmnViper.base.ChatClient
    :members: __doc__
    :member-order: bysource

1.2.1. Main methods
+++++++++++++++++++

These methods should be a point of interest in understanding how
the class starts up and handles the connection.

.. automethod:: dAmnViper.base.ChatClient.init

.. automethod:: dAmnViper.base.ChatClient.populate_objects

.. automethod:: dAmnViper.base.ChatClient.nullflags

.. automethod:: dAmnViper.base.ChatClient.set_protocol

.. automethod:: dAmnViper.base.ChatClient.start

.. automethod:: dAmnViper.base.ChatClient.makeConnection

.. automethod:: dAmnViper.base.ChatClient.connectionLost

.. automethod:: dAmnViper.base.ChatClient.connectionFailed

.. automethod:: dAmnViper.base.ChatClient.connectionMade

.. automethod:: dAmnViper.base.ChatClient.persist

.. automethod:: dAmnViper.base.ChatClient.teardown

.. automethod:: dAmnViper.base.ChatClient.mainloop

.. automethod:: dAmnViper.base.ChatClient.on_loop

.. automethod:: dAmnViper.base.ChatClient.timedout

.. automethod:: dAmnViper.base.ChatClient.close

1.2.2. Connection events
++++++++++++++++++++++++
As well as the above methods, there are dummy methods which are called for
different events to do with the connection. These methods can be overwritten
if your client needs to do anything specific on those events. Those methods are
as follows:
    
    * ``on_connection_start`` - Parameters: connector
    * ``on_connection_lost`` - Parameters: connector, reason
    * ``on_connection_failed`` - Parameters: connector, reason
    * ``on_connection_made`` - No input.

1.1.3. Sending data
+++++++++++++++++++
These methods are used to send data to the server. You should use these
methods if you want to interact with dAmn.

.. automethod:: dAmnViper.base.ChatClient.send

.. automethod:: dAmnViper.base.ChatClient.raw

.. automethod:: dAmnViper.base.ChatClient.pong

.. automethod:: dAmnViper.base.ChatClient.handshake

.. automethod:: dAmnViper.base.ChatClient.login

.. automethod:: dAmnViper.base.ChatClient.join

.. automethod:: dAmnViper.base.ChatClient.part

.. automethod:: dAmnViper.base.ChatClient.say

.. automethod:: dAmnViper.base.ChatClient.npmsg

.. automethod:: dAmnViper.base.ChatClient.action

.. automethod:: dAmnViper.base.ChatClient.me

.. automethod:: dAmnViper.base.ChatClient.promote

.. automethod:: dAmnViper.base.ChatClient.demote

.. automethod:: dAmnViper.base.ChatClient.kick

.. automethod:: dAmnViper.base.ChatClient.ban

.. automethod:: dAmnViper.base.ChatClient.unban

.. automethod:: dAmnViper.base.ChatClient.get

.. automethod:: dAmnViper.base.ChatClient.set

.. automethod:: dAmnViper.base.ChatClient.admin

.. automethod:: dAmnViper.base.ChatClient.disconnect

.. automethod:: dAmnViper.base.ChatClient.kill

1.2.4. Receiving data
+++++++++++++++++++++
These methods are used to handle incoming data.

.. automethod:: dAmnViper.base.ChatClient.handle_pkt

.. automethod:: dAmnViper.base.ChatClient.pkt_generic

.. automethod:: dAmnViper.base.ChatClient.pkt_unknown

.. automethod:: dAmnViper.base.ChatClient.pkt_login

.. automethod:: dAmnViper.base.ChatClient.pkt_join

.. automethod:: dAmnViper.base.ChatClient.pkt_part

.. automethod:: dAmnViper.base.ChatClient.pkt_property

.. automethod:: dAmnViper.base.ChatClient.pkt_recv_join

.. automethod:: dAmnViper.base.ChatClient.pkt_recv_part

.. automethod:: dAmnViper.base.ChatClient.pkt_recv_kicked

.. automethod:: dAmnViper.base.ChatClient.pkt_recv_privchg

.. automethod:: dAmnViper.base.ChatClient.pkt_kicked

.. automethod:: dAmnViper.base.ChatClient.pkt_disconnect

1.2.5. Utility methods
++++++++++++++++++++++
These methods are general purpose methods which can be used in your
application.

.. automethod:: dAmnViper.base.ChatClient.format_ns

.. automethod:: dAmnViper.base.ChatClient.deform_ns

.. automethod:: dAmnViper.base.ChatClient.logger

.. automethod:: dAmnViper.base.ChatClient.new_logger

.. automethod:: dAmnViper.base.ChatClient.get_write_pair

1.3. ``dAmnClient`` - Basic dAmn client class
---------------------------------------------
.. _damnclient:

.. autoclass:: dAmnViper.base.dAmnClient
    :members:


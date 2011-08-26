4. ``parse`` module
==============================================
This module provides objects for parsing data going to and from the dAmn
server. Tablumps and packets are handled by classes here, and a class is
provided to generate output messages for stdout based on packets
received from dAmn.

4.1 ``Packet`` - Basic packet parsing
-------------------------------------
.. _packetobj:

.. autoclass:: dAmnViper.parse.Packet
    :members:

4.2 ``PacketEvent`` - Packet event object
-----------------------------------------
.. _packetevtobj:

.. autoclass:: dAmnViper.parse.PacketEvent
    :members:

4.3. ``ProtocolParser`` - dAmn protocol mapping
-----------------------------------------------
.. _protocolparser:

.. autoclass:: dAmnViper.parse.ProtocolParser
    :members:

4.4. ``Tablumps`` - dAmn tablump parsing
----------------------------------------
.. _tablumps:

.. autoclass:: dAmnViper.parse.Tablumps
    :members:

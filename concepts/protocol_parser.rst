2. Protocol parsing
===================
As mentioned in the :doc:`dAmn packets page <dAmn_packets>`, the protocol used
by the dAmn server is text based. Messages, or packets, sent to and from
clients, follow a specific format. Different packets mean different things.
Most of the packets in the protocol are documented `on this wiki
<http://www.botdom.com/documentation/DAmn>`_.

dAmn Viper provides enough functionality to parse the protocol into usable
objects and messages which can be displayed on the screen. This is done by the
``ProtocolParser`` class.

2.1. Packet naming
-------------------
For dAmn packets to be used in a program, the data they represent needs to be
translated into an object which can be used by programs to determine a
response.

The ``ProtocolParser`` class has a ``mapper`` method whichreturns a dictionary
with the following values::

    {
        'event': packet_name,
        'args': mapped_args,
        'rules': key_value_rules
    }

The ``packet_name`` is usually the packet's ``cmd``, or the command name of the
packet. In general, packet names can have the following formats::
        
            {pkt.cmd}
            {pkt.cmd}_{pkt.sub.cmd}
            {pkt.cmd}_{pkt.sub.cmd}_{pkt.sub.param}

Where ``pkt`` is a ``Packet`` object and ``pkt.sub`` is the object
``Packet(pkt.body)``.

By default, all packet names follow the first format. Packets may use other
formats if their ``cmd`` values have an entry in the ``names`` attribute of
the ``ProtocolParser`` class.

Entries in the ``names`` attribute are always iterables. The iterable can have
at most two items, and these items can be a ``pkt.cmd`` and a ``pkt.sub.cmd``,
in that order.

If a packet's command is found in the ``names`` attribute, then the second
format for the packet name is used. If a sub-packet's command is found, then
the third format is used.
        
2.2. Packet mapping
-------------------
Packet data is mapped into a dictionary according to the objects in the
``maps`` attribute of the `ProtocolParser` class. The ``mapper`` method uses
the object which is stored under the packet name's corresponding key. Each
object is a list, containing the names that each value will be stored under.
The data is mapped as so::

    maps[packet_name] = [pkt.param, pkt.args, pkt.body]
    
As an example, this is the map for the ``login`` packet::

    maps['login'] = ['username', ['e'], 'data']

Which results in the following dictionary being returned by the ``mapper``
method::

    {
        'event': 'login',
        'args': {
            'username': pkt.param,
            'e': pkt.args['e'],
            'data': pkt.body
        },
        'rules': [
            ('username', pkt.param),
            ('e', pkt.args['e']),
            ('data', pkt.body)
        ]
    }

**Note:** *Examples beyond this point will only show the ``args`` portion of
the returned object.*

If a ``generic_{pkt.cmd}`` method is defined, the behaviour of the mapper can
be changed for all packets with the same ``cmd`` value.

The `ProtocolParser` class defines a ``generic_recv`` packet, which creates the
mapped data using the attributes of ``pkt.sub`` instead of ``pkt``.

2.3. Packet arguments mapping
-----------------------------
In the previous example, you may have noticed that the object defining the
mapping for the ``login`` packet used a list to define how the packet's
``args`` data was mapped. This is because the packet's ``args`` attribute is a
dictionary in itself.

There are two ways in which we can define the mapping for each packet argument
using the mapping list. The first and simplest way is to simply define the name
or the argument we want to have mapped to the resulting object. This will cause
the ``mapper`` to find that argument, and to store the argument under a key of
the same name, which is why we get ``args['e'] = pkt.args['e']``.

The second way to define the mapping is to use a pair of strings. Using the
pair, you define which argument you want to store, and the key name you want to
store it under. For example, the ``recv_msg`` packet has the following
mapping::

    maps['recv_msg'] = [None, [('from', 'user')], '*message']

**Note:** *Using None tells the mapper not to store the value.*

The mapping above results in the following object being given under the
``args`` key::

    {
        'user': pkt.sub.args['from'],
        'message': pkt.sub.body
    }

Remember, ``pkt.sub`` is used here because of the ``generic_recv`` method!

2.4. Tablumps parsing
---------------------
The mapping definitions can tell the parser to parse tablumps on a specific
value. This is done by putting an asterisk (``*``) at the front of the key
name!

In the example given above, the mapping definition defines the key ``*message``
for the ``pkt.sub.body`` value. As a result, the parser stores the
``pkt.sub.body`` data under the ``message`` after passing it through the
tablumps parser!

Instances of the ``ProtocolParser`` class store a ``Tablumps`` object in the
``tablumps`` attribute in instances of the class.

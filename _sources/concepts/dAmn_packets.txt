1. dAmn style packets
=====================
The deviantART messaging network chatrooms use a text-based protocol, with
messages, or packets, formatted with newlines. All packets follow the same
basic pattern, using sub-packets in the body to determine sub-commands and the
like.

1.1. Packet structure
---------------------
The basic structure of a dAmn style packet is as follows::
    
    command parameter
    argument=value
    
    body

The ``command`` value determines the packet's command. The ``parameter`` value
determines the parameter being used with the command. The packet can have
several arguments, which are key-value pairs. The body is separated from the
packet's head with two newlines. An example packet is below::

    kicked chat:Botdom
    by=photofroggy
    
    Don't spam

In the above example, the packet's ``command`` is ``"kicked"`` and the
``parameter`` is ``"chat:Botdom"``. There is one argument called ``by`` with
the value ``"photofroggy"``, and the body is ``"Don't spam"``. In quotes, the
above example looks like this::

    "kicked chat:Botdom\nby=photofroggy\n\nDon'tspam\0"

Note that all dAmn packets end with ``\0``, and some packets require a newline
before the ``NULL`` character. Packets without empty bodies do not need a
newline before the ``NULL`` character.

1.2. Viper's packet parser
--------------------------
dAmnViper has it's own packet parser which I created to turn text packets into
objects which are usable in a program. The object processes given strings as
dAmn packets, and stores information from the string in different object
attributes. This makes it easier to work with packets in other parts of the
API.

An example usage of this parser is as follows::

    >>> p = Packet("packetname mainparam\nsome=variables\nsomemore=variables\n\nMain content is placed here.")
    >>> p.cmd
    'packetname'
    >>> p.param
    'mainparam'
    >>> p.args
    {'some': 'variables', 'somemore': 'variables'}
    >>> p.body
    'Main content is placed here.'
    
To parse a sub-packet that may be stored in the the body of a packet, simply
use the following code::

    >>> subPacket = Packet(p.body)

If there is a sub-packet in the body, then the appropriate attributes will be
filled as normal, because sub packets follow the same format as normal packets.

Note that the ``sep`` parameter in this object refers to the character
separating argument keys from their values. Note that arguments are stored in
the ``args`` attribute.

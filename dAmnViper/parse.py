''' dAmnViper.parse module
    Created by photofroggy.
    
    This module provides objects for parsing data going to and from
    the dAmn server. Tablumps and packets are handled by classes here,
    and a class is provided to generate output messages for stdout
    based on packets received from dAmn.
'''

import re

class Packet(object):
    """ Use this class to parse dAmn packets.
        
        This object processes given strings as dAmn packets, and stores
        information from the string in different object attributes. This
        makes it easier to work with packets in other parts of the API.
        
        An example usage of this parser is as follows::
    
            >>> p = Packet("packetname mainparam\\nsome=variables\\nsomemore=variables\\n\\nMain content is placed here.")
            >>> p.cmd
            'packetname'
            >>> p.param
            'mainparam'
            >>> p.args
            {'some': 'variables', 'somemore': 'variables'}
            >>> p.body
            'Main content is placed here.'
        
        To parse a sub-packet that may be stored in the the body of a
        packet, simply use the following code::
            
            >>> subPacket = Packet(p.body)
        
        If there is a sub-packet in the body, then the appropriate
        attributes will be filled as normal, because sub packets follow
        the same format as normal packets.
        
        Note that the ``sep`` parameter in this object refers to the
        character separating argument keys from their values. Note that
        arguments are stored in the ``args`` attribute.
    """

    def __init__(self, data=None, sep='='):
        self.cmd, self.param, self.args, self.body, self.raw = None, None, {}, None, data
        if not data:
            return
        buff = data.partition('\n\n')
        self.body = buff[2] or None
        buff = buff[0].partition('\n')
        if not buff[0]:
            return
        if not sep in buff[0]:
            head = buff[0].partition(' ')
            self.cmd = head[0] or None
            self.param = head[2] or None
            buff = buff[2].partition('\n')
        while buff[0]:
            seg = buff[0].partition(sep)
            buff = buff[2].partition('\n')
            if not seg[1]:
                continue
            self.args[seg[0]] = seg[2]
        # And that's the end of that chapter.

class Tablumps(object):
    """ dAmn tablumps parser.
        
        dAmn sends certain information formatted in a specific manner.
        Links, images, thumbs, and other forms of data are formatted
        in strings where the different attributes of these values are
        separated by tab characters (``\\t``), and usually begin with an
        ampersand.
        
        We refer to these items as "tablumps" because of the tab
        characters being used as delimeters. The job of this class is to
        replace tablumps with readable strings, or to extract the data
        given in the tablumps.
    """
    
    expressions = None
    replace = None
    titles = None
    subs = None
    
    def __init__(self):
        """Populate the expressions and replaces used when parsing tablumps."""
        if self.expressions is not None:
            return
        # Regular expression objects used to find any complicated tablumps.
        self.expressions = [
            re.compile("&avatar\t([a-zA-Z0-9-]+)\t([0-9]+)\t"),
            re.compile("&dev\t(.)\t([a-zA-Z0-9-]+)\t"),
            re.compile("&emote\t([^\t]+)\t([0-9]+)\t([0-9]+)\t(.*?)\t([a-z0-9./=-]+)\t"),
            re.compile("&a\t([^\t]+)\t([^\t]*)\t"),
            re.compile("&link\t([^\t]+)\t&\t"),
            re.compile("&link\t([^\t]+)\t([^\t]+)\t&\t"),
            re.compile("&acro\t([^\t]+)\t(.*)&\/acro\t"),
            re.compile("&abbr\t([^\t]+)\t(.*)&\/abbr\t"),
            re.compile("&thumb\t(?P<ID>[0-9]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t"),
            re.compile("&img\t([^\t]+)\t([^\t]*)\t([^\t]*)\t"),
            re.compile("&iframe\t([^\t]+)\t([0-9%]*)\t([0-9%]*)\t&\/iframe\t"),
        ]
        self.titles = ('avatar', 'dev', 'emote', 'a', 'link', 'link', 'acronym', 'abbr', 'thumb', 'img', 'iframe')
        # Regular expression objects used to find and replace complicated tablumps.
        self.subs = [
            (re.compile("&avatar\t([a-zA-Z0-9-]+)\t([0-9]+)\t"), ":icon\\1:"),
            (re.compile("&dev\t(.)\t([a-zA-Z0-9-]+)\t"), ":dev\\2:"),
            (re.compile("&emote\t([^\t]+)\t([0-9]+)\t([0-9]+)\t(.*?)\t([a-z0-9./=-]+)\t"), "\\1"),
            (re.compile("&a\t([^\t]+)\t([^\t]*)\t"), "<a href=\"\\1\" title=\"\\2\">"),
            (re.compile("&link\t([^\t]+)\t&\t"), "\\1"),
            (re.compile("&link\t([^\t]+)\t([^\t]+)\t&\t"), "\\1 (\\2)"),
            (re.compile("&acro\t([^\t]+)\t"), "<acronym title=\"\\1\">"),
            (re.compile("&abbr\t([^\t]+)\t"), "<abbr title=\"\\1\">"),
            (re.compile("&thumb\t([0-9]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t"), ":thumb\\1:"),
            (re.compile("&img\t([^\t]+)\t([^\t]*)\t([^\t]*)\t"), "<img src=\"\\1\" alt=\"\\2\" title=\"\\3\" />"),
            (re.compile("&iframe\t([^\t]+)\t([0-9%]*)\t([0-9%]*)\t&\/iframe\t"), "<iframe src=\"\\1\" width=\"\\2\" height=\"\\3\" />"),
            (re.compile("<([^>]+) (width|height|title|alt)=\"\"([^>]*?)>"), "<\\1\\3>"),
        ]
        # Search and replace pairs used to parse simple HTML tags.
        self.replace = [
            ("&b\t", "<b>"),
            ("&/b\t", "</b>"),
            ("&i\t", "<i>"),
            ("&/i\t", "</i>"),
            ("&u\t", "<u>"),
            ("&/u\t", "</u>"),
            ("&s\t", "<s>"),
            ("&/s\t", "</s>"),
            ("&sup\t", "<sup>"),
            ("&/sup\t", "</sup>"),
            ("&sub\t", "<sub>"),
            ("&/sub\t", "</sub>"),
            ("&code\t", "<code>"),
            ("&/code\t", "</code>"),
            ("&p\t", "<p>"),
            ("&/p\t", "</p>"),
            ("&ul\t", "<ul>"),
            ("&/ul\t", "</ul>"),
            ("&ol\t", "<ol>"),
            ("&/ol\t", "</ol>"),
            ("&li\t", "<li>"),
            ("&/li\t", "</li>"),
            ("&bcode\t", "<bcode>"),
            ("&/bcode\t", "</bcode>"),
            ("&br\t", "\n"),
            ("&/a\t", "</a>"),
            ("&/acro\t", "</acronym>"),
            ("&/abbr\t", "</abbr>"),
        ]
    
    def parse(self, data):
        """ Parse any dAmn Tablumps found in our input data.
            
            This method will simply return a string with the tablumps
            parsed into readable formats.
        """
        try:
            for lump, repl in self.replace:
                data = data.replace(lump, repl)
            for expression, repl in self.subs:
                data = expression.sub(repl, data)
        except Exception:
            pass
        return data
    
    def capture(self, text):
        """ Return any dAmn Tablumps found in our input data.
            
            Rather than parsing the tablumps, this method returns the
            data given by tablumps. This only works for tablumps where
            a regular expression is used for parsing.
        """
        lumps = {}
        for key, expression in enumerate(self.expressions):
            cc = expression.findall(text)
            if not cc:
                continue
            lumps[self.titles[key]] = cc
        return lumps

class ProtocolParser(object):
    """ Protocol processor.
        
        Use methods of this class to process dAmn information. You can
        customise how different packets are handled by adding items to
        protocol.maps and protocol.messages.
        
        The ``maps`` attribute determines how the data for each packet
        is mapped into a usable dictionary and key/value pair list.
        
        The key/value pair list is referred to as ``rules``, and is
        useful when the data is required in a specific order it is
        defined in. This is used when generating messages in the
        ``logger`` method.
        
        The ``mapper`` method returns a dictionary with the following
        values::
            
            {
                'event': packet_name,
                'args': mapped_args,
                'rules': key_value_rules
            }
        
        The ``packet_name`` is usually the packet's ``cmd``, or the
        command name of the packet. In general, packet names can have
        the following formats::
        
            {pkt.cmd}
            {pkt.cmd}_{pkt.sub.cmd}
            {pkt.cmd}_{pkt.sub.cmd}_{pkt.sub.param}
        
        Where ``pkt`` is a ``Packet`` object and ``pkt.sub`` is the
        object ``Packet(pkt.body)``.
        
        By default, all packet names follow the first format. Packets
        may use other formats if their ``cmd`` values have an entry in
        the ``names`` attribute of this class.
        
        Entries in the ``names`` attribute are always iterables. The
        iterable can have at most two items, and these items can be a
        ``pkt.cmd`` and a ``pkt.sub.cmd``, in that order.
        
        If a packet's command is found in the ``names`` attribute, then
        the second format for the packet name is used. If a sub-packet's
        command is found, then the third format is used.
        
        **Packet Mapping**
        
        Packet data is mapped into a dictionary according to the objects
        in the ``maps`` attribute of this class. The ``mapper`` method
        uses the object which is stored under the packet name's
        corresponding key. Each object is a list, containing the names
        that each value will be stored under. The data is mapped as so::
            
            maps[packet_name] = [pkt.param, pkt.args, pkt.body]
        
        As an example, this is the map for the ``login`` packet::
            
            maps['login'] = ['username', ['e'], 'data']
            
        Which results in the following dictionary being returned by
        the ``mapper`` method::
            
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
        
        **Note:** *Examples beyond this point will only show the
        ``args`` portion of the returned object.*
        
        If a ``generic_{pkt.cmd}`` method is defined, the behaviour of
        the mapper can be changed for all packets with the same ``cmd``
        value.
        
        This class defines a ``generic_recv`` packet, which creates the
        mapped data using the attributes of ``pkt.sub`` instead of
        ``pkt``.
        
        **Packet Arguments Mapping**
        
        In the previous example, you may have noticed that the object
        defining the mapping for the ``login`` packet used a list to
        define how the packet's ``args`` data was mapped. This is
        because the packet's ``args`` attribute is a dictionary in
        itself.
        
        There are two ways in which we can define the mapping for each
        packet argument using the mapping list. The first and simplest
        way is to simply define the name or the argument we want to have
        mapped to the resulting object. This will cause the ``mapper``
        to find that argument, and to store the argument under a key of
        the same name, which is why we get ``args['e'] =
        pkt.args['e']``.
        
        The second way to define the mapping is to use a pair of
        strings. Using the pair, you define which argument you want to
        store, and the key name you want to store it under. For example,
        the ``recv_msg`` packet has the following mapping::
        
            maps['recv_msg'] = [None, [('from', 'user')], '*message']
        
        **Note:** *Using None tells the mapper not to store the value.*
        
        The mapping above results in the following object being given
        under the ``args`` key::
            
            {
                'user': pkt.sub.args['from'],
                'message': pkt.sub.body
            }
        
        Remember, ``pkt.sub`` is used here because of the
        ``generic_recv`` method!
        
        **Tablumps Parsing**
        
        The mapping definitions can tell the parser to parse tablumps on
        a specific value. This is done by putting an asterisk (``*``) at
        the front of the key name!
        
        In the example given above, the mapping definition defines the
        key ``*message`` for the ``pkt.sub.body`` value. As a result,
        the parser stores the ``pkt.sub.body`` data under the
        ``message`` after passing it through the tablumps parser!
        
        Instances of this class store a ``Tablumps`` object in the
        ``tablumps`` attribute in instances of this class.
    """
    maps = {
        'dAmnServer': ['version'],
        'login': ['username', ['e'], 'data'],
        'join': ['ns', ['e'] ],
        'part': ['ns', ['e', '*r'] ],
        'property': ['ns', ['p', 'by', 'ts'], '*value' ],
        'recv_msg': [None, [('from', 'user')], '*message'],
        'recv_action': [None, [('from', 'user')], '*message'],
        'recv_join': ['user', None, '*info'],
        'recv_part': ['user', ['r']],
        'recv_privchg': ['user', ['by', 'pc']],
        'recv_kicked': ['user', ['by'], '*r'],
        'recv_admin_create': [None, ['p', ('by', 'user'), ('name', 'pc'), 'privs']],
        'recv_admin_update': [None, ['p', ('by', 'user'), ('name', 'pc'), 'privs']],
        'recv_admin_rename': [None, ['p', ('by', 'user'), 'prev', ('name', 'pc')]],
        'recv_admin_move': [None, ['p', ('by', 'user'), 'prev', ('name', 'pc'), ('n', 'affected')]],
        'recv_admin_remove': [None, ['p', ('by', 'user'), ('name', 'pc'), ('n', 'affected')]],
        'recv_admin_show': [None, ['p'], 'info'],
        'recv_admin_showverbose': [None, ['p'], 'info'],
        'recv_admin_privclass': [None, ['p', 'e'], 'command'],
        'kicked': ['ns', [('by', 'user')], '*r'],
        'ping': [],
        'disconnect': [None, ['e']],
        'send': ['ns', ['e']],
        'kick': ['ns', [('u', 'user'), 'e']],
        'get': ['ns', ['p', 'e']],
        'set': ['ns', ['p', 'e']],
        'kill': ['ns', ['e']],
        'unknown': [None, None, None, None, 'packet'],
    }
    names = [('recv', 'admin')]
    messages = {
        'dAmnServer': ('** Connected to dAmn Server {0}.', False),
        'login': ('** Login as {0}: {1}.', False),
        'join': ('** Join {ns}: "{1}".', False),
        'part': ('** Part {ns}: "{1}". [{2}]', False),
        'property': ('** Got {1} for {ns}.', False),
        'recv_msg': ('<{1}> {2}',),
        'recv_action': ('* {1} {2}',),
        'recv_join': ('** {1} has joined.',),
        'recv_part': ('** {1} has left. [{2}]',),
        'recv_privchg': ('** {1} has been made a member of {3} by {2} *',),
        'recv_kicked': ('** {1} has been kicked by {2} * {3}',),
        'recv_admin_create': ('** Privilege class {3} has been created by {2} with: {4}',),
        'recv_admin_update': ('** Privilege class {3} has been updated by {2} with: {4}',),
        'recv_admin_rename': ('** Privilege class {4} has been renamed to {3} by {2}',),
        'recv_admin_move': ('** All members of {3} have been moved to {4} by {2} -- {5} affected user(s)',),
        'recv_admin_remove': ('** Privilege class {3} has been removed by {2} -- {4} affected user(s)',),
        'recv_admin_show': None,
        'recv_admin_showverbose': None,
        'recv_admin_privclass': ('** Admin command "{2}" failed: {1}',),
        'kicked': ('** You have been kicked by {1} * {2}',),
        'ping': ('** Ping...', False, True),
        'disconnect': ('** You have been disconnected * {0}', False),
        'send': ('** Send error: {1}',),
        'kick': ('** Could not kick {1}: {2}',),
        'get': ('** Could not get {1}info for {ns}: {2}', False),
        'set': ('** Could not set {1}: {2}',),
        'kill': ('** Kill error: {1}',),
        'unknown': ('** Received unknown packet in {0}: {1}', False),
    }
    
    tablumps = Tablumps
    
    def __init__(self):
        self.tablumps = self.tablumps()
    
    def evt_namespace(self, pkt):
        # Work on the namespace of an event!
        namespace = pkt.cmd
        for conditions in self.names:
            if conditions[0] == namespace:
                subline = pkt.body.split('\n')[0]
                subline = subline.split(' ')
                if not subline or not subline[0]:
                    break
                namespace = '_'.join([namespace, subline[0]])
                if len(conditions) > 1 and len(subline) > 1:
                    if conditions[1] == subline[0]:
                        namespace = '_'.join([namespace, subline[1]])
                break
        return namespace if namespace in self.maps else 'unknown'
    
    def mapper(self, pkt):
        """ Map packets to a usable data structure.
            
            Return data mapped according to the conditions defined in
            the ``maps`` attribute.
        """
        store = {'args': {}, 'rules': [], 'event': self.evt_namespace(pkt)}
        map = self.maps[store['event']]
        return getattr(self, 'gen_'+pkt.cmd, self.sort)(store, pkt, map)
        
    def sort(self, store, data, map):
        """ Sort data according to the conditions in the given map. """
        for i, cond in enumerate(map):
            if not cond: continue
            if i is 0:
                ptab = cond[0] == '*'
                if ptab: cond = cond[1:]
                val = (data.param if not ptab else self.tablumps.parse(data.param)) if data.param else ''
                store['rules'].append((cond, val))
                store['args'][cond] = val
            if i is 1:
                for item in cond:
                    if not item:
                        continue
                    argn, name = item if isinstance(item, tuple) else (item, item)
                    ptab = argn[0] == '*'
                    if ptab and argn == name: name = argn[1:]
                    val = '' if not argn in data.args.keys() else data.args[argn]
                    if ptab: val = self.tablumps.parse(val)
                    store['rules'].append((name, val))
                    store['args'][name] = val
            if i is 2:
                ptab = cond[0] == '*'
                if ptab: cond = cond[1:]
                val = (data.body if not ptab else self.tablumps.parse(data.body)) if data.body else ''
                store['rules'].append((cond, val))
                store['args'][cond] = val
            if i is 3:
                store = self.sort(store, Packet(data.body), cond)
            if i is 4:
                val = data.raw if data.raw else ''
                store['rules'].append((cond, val))
                store['args'][cond] = val
        return store
    
    def logger(self, event, data, ns, pkt):
        """ Return a log_list (channel, message[, bool(showns)[, bool(mute)]]).
            
            The message returned is based on the templates defined in
            the ``messages`` attribute of this class.
        """
        sequence = [ns, '', True, False, pkt]
        if not event in self.messages.keys():
            return None
        if hasattr(self, 'log_'+event):
            return getattr(self, 'log_'+event)(event, data, ns, pkt)
        msgtpl = self.messages[event]
        if msgtpl is None or len(msgtpl) == 0:
            return None
        data = [(item[1] if bool(item[1]) else '') for item in data]
        disp = (msgtpl[0].replace('{ns}', ns)).format(*data)
        if disp[-3:] == ' []':
            disp = disp[:-3]
        sequence[1] = disp
        msgtpl = [] if len(msgtpl) == 1 else msgtpl[1:]
        i = 2
        for item in msgtpl:
            sequence[i] = item
            i+=  1
        return sequence
    
    def gen_recv(self, store, data, map):
        # Generic recv packet mapping operations.
        store['args']['ns'] = data.param
        store['rules'].append(('ns', data.param))
        store = self.sort(store, Packet(data.body), map)
        if store['event'] in ('recv_msg', 'recv_action'):
            store['args']['raw'] = data.raw
            store['rules'].append(('raw', data.raw))
        return store

# EOF

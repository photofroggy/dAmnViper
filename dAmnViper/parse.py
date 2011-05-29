''' dAmnViper.parse module
    This module is part of the dAmnViper package.
    Created by photofroggy.
'''

import re

class Packet:
    """ Use this class to parse dAmn packets.
        Data is stored in the attributes cmd, param,
        args, body and raw.
    """

    def __init__(self, data=None, sep='='):
        self.cmd, self.param, self.args, self.body, self.raw = None, None, {}, None, data
        if not bool(data): return
        if data.find('\n\n') != -1:
            self.body = data[data.find('\n\n')+2:]
            data = data[:data.find('\n\n')]
        breaks = data.split('\n')
        if not bool(breaks): return
        if len(breaks) >= 1 and not sep in breaks[0]:
            head = breaks.pop(0).split(' ')
            self.cmd = head[0] or None
            self.param = None if len(head) < 2 else head[1]
        for line in breaks:
            if line.find(sep) == -1: continue
            self.args[line[:line.find(sep)]] = line[line.find(sep)+len(sep):]
        # And that's the end of that chapter.

class Tablumps:
    """A very simple static class used to parse or capture dAmn-style Tablumps."""
    
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
        # Parse any dAmn Tablumps found in our input data.
        try:
            for lump, repl in self.replace:
                data = data.replace(lump, repl)
            for expression, repl in self.subs:
                data = expression.sub(repl, data)
        except Exception:
            pass
        return data
    
    def capture(self, text):
        # Return any dAmn Tablumps found in our input data.
        lumps = {}
        for key, expression in enumerate(self.expressions):
            cc = expression.findall(text)
            if not cc:
                continue
            lumps[self.titles[key]] = cc
        return lumps

class Protocol:
    """ Protocol processor.
        Use methods of this class to process dAmn information.
        You can customise how different packets are handled by
        adding itemds to protocol.maps and protocol.messages.
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
        # Return pkt's data mapped according to the conditions defined in protocol.maps.
        store = {'args': {}, 'rules': [], 'event': self.evt_namespace(pkt)}
        map = self.maps[store['event']]
        return getattr(self, 'gen_'+pkt.cmd, self.sort)(store, pkt, map)
        
    def sort(self, store, data, map):
        # Sort data into store according to the conditions in map.
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
        # Return a log_list (channel, message[, bool(showns)[, bool(mute)]]).
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

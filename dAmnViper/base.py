''' dAmnViper.base module
    This module is part of the dAmnViper package.
    Created by photofroggy.
'''

import sys
import time
# Import dependencies from the API!
from dAmnViper.data import Channel
from dAmnViper.parse import Packet
from dAmnViper.parse import Protocol
from dAmnViper.stream import Connection
from dAmnViper.deviantART import Login

class dAmnSock:
    """ dAmnSock class.
        This is a base class for managing a connection
        to a dAmn server.
    """
    
    class platform:
        """Information about the dAmn Viper platform."""
        name = 'dAmn Viper'
        version = 2
        state = 'RC'
        build = 54
        stamp = '29052011-122308'
        series = 'Swift'
        author = 'photofroggy'
            
    class user:
        """User login data."""
        username = None
        password = None
        cookie = None
        token = None

    class flag:
        """Status flags are stored here"""
        connecting = False
        shaking = False
        loggingin = False
        connected = False
    
    class CONST:
        """dAmnSock style 'constants'."""
        SERVER = 'chat.deviantart.com'
        CLIENT = 'dAmnClient 0.3'
        PORT = 3900
    
    class session:
        status = False
        cookie = None
        token = None

    extras = {'remember_me':'1'}
    agent = 'dAmnViper (python 3.x) dAmnSock/1.1'
    sock = None
    
    def nullflags(self):
        self.flag.connecting = False
        self.flag.shaking = False
        self.flag.loggingin = False
        self.flag.connected = False
    
    def logger(self, ns, msg, showns=True, mute=False, pkt=None):
        if mute: return
        stamp = time.strftime('%H:%M:%S|')
        sys.stdout.write('>> {0}{1} {2}\n'.format(stamp, (ns + '|' if showns else ''), msg))
        sys.stdout.flush()
    
    def get_token(self):
        self.on_get_token()
        if not self.user.password:
            return
        self.session = Login(self.user.username, self.user.password, self.extras, self.agent)
        if self.session.status[0] == 1:
            self.user.cookie = self.session.cookie
            self.user.token = self.session.token
            self.user.password = None
        self.on_token()

    def on_get_token(self):
        """Overwrite this method to do shit when get_token is called."""
        pass
    
    def on_token(self):
        """Overwrite this method to do stuff after get_token is finished."""
        pass
    
    def connect(self):
        """Open a connection to dAmn!"""
        if self.sock and self.sock.sock:
            return
        self.sock = Connection(self.CONST.SERVER, self.CONST.CLIENT, self.CONST.PORT)
        self.sock.connect()
        self.flag.connecting = self.sock.connected()
        return self.flag.connecting
    
    def handshake(self, vals=None):
        # Should be able to define values sent in the handshake packet.
        if not self.flag.connecting:
            return False
        self.flag.shaking = True # Raise the flag, hoe.
        shake = self.CONST.CLIENT
        shake+= '\nagent='+self.agent
        if vals == None:
            shake+= '\n'
        else:
            shake+= "\n{0}\n".format("\n".join(['='.join([key, vals[key]]) for key in vals]))
        if len(shake+'\0') == self.send(shake):
            return True
        return False
    
    def login(self):
        # Send our login packet. Set the loggingin flag to true.
        self.flag.loggingin = True
        return bool(self.send('login {0}\npk={1}\n'.format(self.user.username, self.user.token)))
    
    def send(self, data):
        # Send data to dAmn!
        if self.sock == None or not self.sock.connected():
            return 0
        return self.sock.send(data)
    
    def get_packet(self):
        # Return a single packet from the queue.
        if not self.sock.connected():
            self.nullflags()
            return None
        return self.sock.get_packet()
    
    def close(self):
        # This is how we close our connection!
        if self.sock and self.sock.connected():
            self.sock.close()
    
    # PROTOCOL!
    # The methods below pretty much define the protocol for outgoing packets.

    def raw(self, data):
        # Send a raw dAmn packet.
        return self.send(data)
        
    def pong(self):
        # dAmn likes to play ping pong...
        return self.send('pong\n')
        
    def join(self, ns):
        # Send a join packet to dAmn.
        return self.send('join {0}\n'.format(ns))
        
    def part(self, ns):
        # Send a part packet to dAmn
        return self.send('part {0}\n'.format(ns))
        
    def say(self, ns, message):
        # Send a message to a dAmn channel namespace.
        return self.send('send {0}\n\nmsg main\n\n{1}'.format(ns, str(message)))
    
    def action(self, ns, message):
        # Send an action to a dAmn channel namespace.
        return self.send('send {0}\n\naction main\n\n{1}'.format(ns, str(message)))
    
    def me(self, ns, message):
        # This is just another way to do an action.
        return self.action(ns, message)
        
    def npmsg(self, ns, message):
        # Send a non-parsed message to a dAmn channel namespace.
        return self.send('send {0}\n\nnpmsg main\n\n{1}'.format(ns, str(message)))
    
    def promote(self, ns, user, pc=None):
        # Promote a user in a dAmn channel.
        return self.send('send {0}\n\npromote {1}\n{2}'.format(ns, user, '' if pc == None else '\n'+str(pc)))
    
    def demote(self, ns, user, pc=None):
        # Demote a user in a dAmn channel.
        return self.send('send {0}\n\ndemote {1}\n{2}'.format(ns, user, '' if pc == None else '\n'+str(pc)))
    
    def kick(self, ns, user, r=None):
        # Kick a user out of a dAmn channel.
        return self.send('kick {0}\nu={1}\n{2}'.format(ns, user, '' if r == None else '\n'+str(r)))
    
    def ban(self, ns, user):
        # Ban a user from a dAmn channel.
        return self.send('send {0}\n\nban {1}\n'.format(ns, user))
    
    def unban(self, ns, user):
        # Unban someone from a dAmn channel.
        return self.send('send {0}\n\nunban {1}\n'.format(ns, user))
    
    def get(self, ns, p):
        # Get a property for a dAmn channel.
        return self.send('get {0}\np={1}\n'.format(ns, p))
    
    def set(self, ns, p, val):
        # Set a property for a dAmn channel.
        return self.send('set {0}\np={1}\n\n{2}'.format(ns, p, val))
    
    def admin(self, ns, command):
        # Send an admin command to a dAmn channel. No need for multiple methods here.
        return self.send('send {0}\n\nadmin\n\n{1}'.format(ns, command))
    
    def disconnect(self):
        # Send a disconnect packet to the dAmn server.
        return self.send('disconnect\n')
        
    def kill(self, ns, r=None):
        # Send a kill packet to the dAmn server.
        return self.send('kill {0}\n{1}'.format(ns, '' if r == None else '\n'+str(r)))
    
    # END PROTOCOL METHODS
    
    def parser(self):
        # Just a shortcut for getting the Packet class.
        return Packet

class Client(dAmnSock):
    """ dAmn Client class.
        This provides a more client-like interface between
        the dAmn server and the application.
    """

    agent = 'dAmnViper (Python 3.x) Client/dAmnSock/x.x'
    channel = {}
    _protocol = Protocol

    def __init__(self, *args, **kwargs):
        # Create an instance of our protocol class. Do anything else required.
        self.protocol = self._protocol()
        self.__inst__(*args, **kwargs)
        self._lastp = time.time()
    
    def __inst__(self, *args, **kwargs):
        """Overwrite this method!"""
        self.agent = 'dAmnViper (Python 3.1) Client/dAmnSock/{0}.{1}'.format(
            self.platform.version, self.platform.build)
    
    def logger(self, ns, msg, showns=True, mute=False, pkt=None):
        # Prints messages to stdout.
        if mute: return
        stamp = time.strftime('%H:%M:%S|')
        sys.stdout.write('>> {0}{1} {2}\n'.format(stamp, (ns + '|' if showns else ''), msg))
        sys.stdout.flush()
    
    def format_ns(self, ns):
        # This takes a dAmn channel name and formats it as a raw dAmn namespace.
        ns = str(ns)
        un = self.user.username
        pre = ns[:1]
        if pre == '#':
            return 'chat:{0}'.format(ns[1:])
        if pre == '@':
            if not un:
                return 'pchat:{0}'.format(ns[1:])
            para = [ns[1:], un]
            para.sort(key=str.lower)
            return 'pchat:{0}:{1}'.format(para[0], para[1])
        if ns[:5] == 'chat:' or ns[:6] == 'pchat:':
            return ns
        return 'chat:'+ns
    
    def deform_ns(self, ns):
        # This does the opposite of format_ns()
        parts = str(ns).split(':')
        discard = self.user.username
        if parts[0].lower() == 'chat':
            return '#{0}'.format(parts[1])
        if parts[0].lower() == 'pchat':
            if not discard:
                return '@{0}:{1}'.format(parts[1], parts[2])
            parts.pop(0)
            for i in range(0,2):
                if parts[i].lower() == discard.lower():
                    parts.pop(i)
                    return '@{0}'.format(parts[0])
        if ns[:1] in ('#', '@'):
            return ns
        return '#'+ns

    def get_packets(self):
        # This implementation is simply faster than get_packet().
        retd = []
        nmeth = lambda data: data
        pkts = self.sock.get_packets()
        for raw_pkt in pkts:
            retd.append(self.process_packet(raw_pkt, nmeth))
        if retd:
            self._lastp = time.time()
        else:
            if (time.time() - self._lastp) >= 120:
                self._timeout()
        return retd
    
    def process_packet(self, raw_pkt, nmeth):
        pkt = Packet(raw_pkt)
        ns = '~Global'
        if pkt.param:
            if pkt.param[:5] in ('chat:', 'pchat'):
                ns = self.deform_ns(pkt.param)
            elif pkt.param[:6] == 'login:':
                ns = '@' + pkt.param[6:]
        data = self.protocol.mapper(pkt)
        loglist = self.protocol.logger(data['event'], data['rules'], ns, pkt)
        if loglist is not None:
            self.logger(*loglist)
        getattr(self, 'pkt_' + data['event'], nmeth)(data['args'])
        self.pkt_generic(data)
        return data
    
    def run(self, *args, **kwargs):
        """Overwrite this method to provide your own application with a main loop."""
        if not self.sock:
            return
        while self.sock.connected():
            try:
                self.mainloop(*args, **kwargs)
                self.on_loop(*args, **kwargs)
            except KeyboardInterrupt as e:
                sys.stdout.write('\n')
                self.sock.close()
                self.process_packet('disconnect\ne=force quit (^C)\n\n', lambda data: data)
                break
        while len(self.sock.packet) > 0:
            self.mainloop(*args, **kwargs)
            self.on_loop(*args, **kwargs)
    
    def mainloop(self, *args, **kwargs):
        """Overwrite this to do stuff on every iteration of the main loop!"""
        self.get_packets()

    def _timeout(self):
        self.sock.packet.append('disconnect\ne=socket timed out\n\n')
    
    def on_loop(self, *args, **kwargs):
        # Overwrite this method to do stuff at the end of each main loop.
        pass
    
    # Packet handling stuffs. Only basic shizz.
    
    def pkt_generic(self, data):
        # Overwrite this method to do stuff on every packet event.
        pass
    
    def pkt_dAmnServer(self, data):
        # What to do in the event of a handshake.
        self.flag.shaking = False
        self.login()
    
    def pkt_login(self, data):
        # What to do when we receive a login packet.
        self.flag.loggingin = False
        if data['e'] == 'ok':
            self.flag.loggingin = False
            self.flag.connecting = False
            self.flag.connected = True
            return
        self.nullflags()
        self.close()
    
    def pkt_join(self, data):
        # The client tried to join a channel.
        if data['e'] == 'ok':
            self.channel[data['ns']] = Channel(
                data['ns'], self.deform_ns(data['ns'])
            )
            return
    
    def pkt_part(self, data):
        # This is what happens when we receive a part packet.
        if data['ns'] in self.channel.keys():
            del self.channel[data['ns']]
        if len(self.channel) > 0:
            return
        if 'r' in data.keys():
            if data['r'] in ('bad data', 'bad msg', 'msg too big') or 'killed:' in data['r']:
                self.sock.packet.append('disconnect{0}e={1}{2}{3}'.format("\n", data['r'], "\n", "\n"))
                return
    
    def pkt_property(self, data):
        # Make sure properties are stored in the right places.
        if data['p'] == 'info': return
        if not data['ns'] in self.channel.keys(): return
        self.channel[data['ns']].process_property(data)
    
    def pkt_recv_join(self, data):
        # When a user joins, log them!
        self.channel[data['ns']].register_user(Packet(data['info']), data['user'])
        
    def pkt_recv_part(self, data):
        # No need to log users after they leave a channel.
        if not data['user'] in self.channel[data['ns']].member: return
        self.channel[data['ns']].member[data['user']]['con']-= 1
        if self.channel[data['ns']].member[data['user']]['con'] == 0:
            del self.channel[data['ns']].member[data['user']]
            
    def pkt_recv_kicked(self, data):
        # Get rid of users who get kicked.
        if not data['user'] in self.channel[data['ns']].member: return
        del self.channel[data['ns']].member[data['user']]
        
    def pkt_recv_privchg(self, data):
        # Got to make sure users' privclasses are up to date.
        if not data['user'] in self.channel[data['ns']].member: return
        self.channel[data['ns']].member[data['user']]['pc'] = data['pc']
    
    def pkt_disconnect(self, data):
        # dAmn also likes to disconnect clients. A lot.
        self.close()
        self.flag.connected = False
        
class ReconnectingClient(Client):
    """Persistant dAmn Client Class."""
    
    class flag(Client.flag):
        """Status flags are stored here"""
        autorejoin = True
        disconnecting = False
        reconnect = False
        quitting = False
        restart = False
        close = False
        debug = False
    
    autojoin = ['chat:Botdom']
    _disconnects = 0
    _connect_attempts = 0
    _connect_attempt_limit = 3
    
    session = None
    
    def __inst__(self):
        self.agent = 'dAmnViper (Python 3.1) ReconnectingClient/Client/dAmnSock/{0}.{1}'.format(
            self.platform.version, self.platform.build)
        self._received = time.strftime('%Y-%m-%d')
        self._connect_attempts = 0
        self.session = None
    
    def nullflags(self):
        Client.nullflags(self)
        self.flag.disconnecting = False
        self.flag.reconnect = False
        self.flag.quitting = False
        self.flag.restart = False
        self.flag.close = False
        
    def start(self, vals=None, *args, **kwargs):
        """Overwrite this method for a more customized client."""
        # We want this to be a continuous loop, so we can keep trying to connect if there are problems.
        while True:
            self._connect_attempts += 1
            if not self.authenticate(vals, *args, **kwargs):
                return
            self.logger('~Global', '** Opening a connection to dAmn.', False)
            if not self.make_connection(vals, *args, **kwargs):
                return
            # Enter the main loop of the program! Hells yeah!
            self.run(*args, **kwargs)
            # Ok, we're not connected anymore! What should we do?
            if self.attempt_reconnect(vals, *args, **kwargs):
                self.nullflags()
                continue
            break
    
    def run(self, *args, **kwargs):
        """Overwrite this method to provide your own application with a main loop."""
        if not self.sock:
            return
        while self.sock.connected():
            try:
                self.mainloop(*args, **kwargs)
                self.on_loop(*args, **kwargs)
            except KeyboardInterrupt as e:
                sys.stdout.write('\n')
                self.sock.close()
                self.flag.quitting = True
                self.process_packet('disconnect\ne=force quit (^C)\n\n', lambda data: data)
                break
        while len(self.sock.packet) > 0:
            self.mainloop(*args, **kwargs)
            self.on_loop(*args, **kwargs)
    
    def mainloop(self, *args, **kwargs):
        """Overwrite this if you want to do stuff during the main program loop."""
        self._received = time.strftime('%Y-%m-%d')
        self.get_packets()
        time.sleep(.05)
    
    def authenticate(self, vals=None, *args, **kwargs):
        if not self.user.token:
            # If we don't have an authtoken, try and grab one!
            self.logger('~Global', '** Retrieving authtoken, this may take a while...', False)
            self.get_token()
            if self.session is None:
                self.logger('~Global', '>> Insufficient login details provided.', False)
                return False
            if self.session.status[0] != 1:
                # Something went wrong! Maybe the user entered the wrong details?!
                self.logger('~Global', '>> Failed to get an authtoken.', False)
                self.logger('~Global', '>> {0}'.format(self.session.status[1]), False)
                return False
            # If we get here all is well.
            self.logger('~Global', '** Got an authtoken.', False)
        return True
    
    def attempt_reconnect(self, vals=None, *args, **kwargs):
        if self._connect_attempt_limit == 0:
            return True
        if self.flag.reconnect and self._connect_attempts < self._connect_attempt_limit:
            return True
        if self._connect_attempts >= self._connect_attempt_limit:
            n = self._connect_attempts
            self.logger('~Global', '>> Failed to connect to dAmn '+str(n)+' times. Giving up.', False)
            self.logger('~Global', '>> Make sure you entered the login details correctly.', False)
            self.logger('~Global', '>> If you already have, there may be a problem with dAmn.', False)
        return False
    
    def make_connection(self, vals=None, *args, **kwargs):
        # Actually try to connect to dAmn!
        # This simply opens a socket connection. The rest takes more effort.
        self.connect()
        if not self.flag.connecting:
            self.logger('~Global', '>> Failed to open a connection to dAmn.', False)
            return False
        # Send a handshake to the server!
        self.handshake(vals if bool(vals) else {'Client':'Viper.ReconnectingClient'})
        return True
        
    def pkt_login(self, data):
        Client.pkt_login(self, data)
        if data['e'] != 'ok':
            return
        self._connect_attempts = 0
        for ns in self.autojoin:
            self.join(self.format_ns(ns))
    
    def pkt_join(self, data):
        Client.pkt_join(self, data)
        if len(self.channel) > 0:
            return
        if data['e'] != 'ok':
            self.sock.append('disconnect\ne=no joined channels\n\n')
    
    def pkt_part(self, data):
        Client.pkt_part(self, data)
        if data['e'] != 'ok': return
        if self.channel or self.flag.disconnecting or self.flag.quitting:
            return
        self.sock.append('disconnect\ne=no joined channels\n\n')
    
    def pkt_kicked(self, data):
        del self.channel[data['ns']]
        if self.flag.disconnecting or self.flag.quitting:
            return
        if 'r' in data.keys():
            if 'autokicked' in data['r'].lower() or 'not privileged' in data['r'].lower():
                if len(self.channel) > 0:
                    return
                self.sock.append('disconnect\ne=no joined channels\n\n')
                return
        if self.flag.autorejoin:
            self.join(data['ns'])
    
    def pkt_disconnect(self, data):
        Client.pkt_disconnect(self, data)
        self._disconnects+= 1
        self.channel = {}
        if self.flag.quitting:
            self.flag.close = True
            return
        if data['e'] == 'no joined channels' and len(self.autojoin) == 0:
            return
        if self.flag.disconnecting:
            self.flag.disconnecting = False
        else:
            self.logger('~Global', '>> Experiencing an unexpected disconnect.', False)
            self.logger('~Global', '>> Attempting to reconnect in a moment.', False)
        time.sleep(1)
        self.nullflags()
        self.flag.reconnect = True
        
    def logger(self, ns, msg, showns=True, mute=False, pkt=None):
        stamp = time.strftime('%H:%M:%S')
        ns = ns + '|' if showns else ''
        if not mute or self.flag.debug:
            try:
                sys.stdout.write('{0}|{1} {2}\n'.format(stamp, ns, msg))
            except:
                sys.stdout.write('{0}| >> I failed to display a message! Sorry.\n'.format(stamp))
            sys.stdout.flush()

# EOF

''' dAmnViper.base module
    Created by photofroggy.
    
    This module provides the dAmnSock class, which acts
    as an API for connecting to and interacting with
    deviantART.com's chatrooms. This is achieved using
    Twisted.
'''

# Standard library
import sys
import time
from functools import wraps

# Twisted imports. Wooooo.
from twisted.internet import defer
from twisted.internet import reactor


# Viper imports
# Data
from dAmnViper.data import Channel
# Parsing
from dAmnViper.parse import Packet
from dAmnViper.parse import ProtocolParser
# Internets! lols.
from dAmnViper import deviantART
from dAmnViper.net import ConnectionFactory


class dAmnSock(object):
    """ The dAmnSock class provides an easy to use API for connecting
        to dAmn, and for interacting with the server.
    
        Applications using this class should extend the class to add in
        some basic functionality so that it works as they expect. The
        class can be made to work properly with only minor modifications
        as shown here::
            
            from twisted.internet import reactor
            from dAmnViper.base import dAmnSock
            
            dAmn = dAmnSock()    
            
            dAmn.user.username = 'username'
            dAmn.user.password = 'password'
            dAmn.autojoin = ['Botdom']
            
            dAmn.teardown = lambda: reactor.stop()
            
            dAmn.start()
            
            if dAmn.flag.connecting:
                reactor.run()
        
        The ``teardown`` callback needs to be defined or the application
        will hang when the connection to dAmn is lost.
        
        A way to remove the need to check the
        ``dAmnSock.flag.connecting`` flag is to define your own
        ``on_token`` method on the object, and using this to call
        ``reactor.run()``.
    """
    
    class platform:
        """Information about the dAmn Viper platform."""
        name = 'dAmn Viper'
        version = 3
        state = 'Beta'
        build = 55
        stamp = '03062011-170934'
        series = 'Twister'
        author = 'photofroggy'
            
    class user(object):
        """User login data."""
        def __init__(self):
            self.username = None
            self.password = None
            self.cookie = None
            self.token = None
    
    class flag(object):
        """Status flags are stored here"""
        
        debug = False
        
        def __init__(self):
            self.connecting = False
            self.shaking = False
            self.loggingin = False
            self.connected = False
            self.autorejoin = True
            self.disconnecting = False
            self.reconnect = False
            self.quitting = False
            self.retry = False
            self.restart = False
            self.close = False
    
    class CONST(object):
        """dAmnSock style 'constants'."""
        def __init__(self):
            self.SERVER = 'chat.deviantart.com'
            self.CLIENT = 'dAmnClient 0.3'
            self.PORT = 3900
    
    class session:
        status = (False, None)
        cookie = None
        token = None
    
    class connection:
        def __init__(self):
            self.disconnects = 0
            self.attempts = 0
            self.limit = 3
    
    class defer:
        """ Storage for Deferred and IDelayedCall objects. """
        
        def __init__(self):
            self.loop = None
            self.timeout = None
        
        def teardown(self):
            """ Stop any delayed calls from running. """
            if self.loop is None and self.timeout is None:
                return
            
            try:
                self.loop.cancel()
            except Exception as e:
                pass
            
            try:
                self.timeout.cancel()
            except Exception as e:
                pass
    
    ''' Not yet you don't, bitch!
    class oauth2:
        """ oAuth2 credentials.
            
            These are the defaults. You should define your own
            before trying to connect to dAmn using dAmnSock.
        """
        id = 25
        key = ""
        auth_type = 0
        grant_type = 0
        access_token_type = 0
    '''
    
    extras = {'remember_me':'1'}
    agent = 'dAmnViper (python) dAmnSock/1.1'
    info = {}
    
    conn = None
    io = None
    
    protocol = ProtocolParser
    
    autojoin = ['chat:Botdom']
    channel = {}
    
    timeout_delay = 120

    def __init__(self, *args, **kwargs):
        # Create an instance of our protocol class. Do anything else required.
        self.populate_objects()
        self.agent = 'dAmnViper/{0} (Python) viper/base/dAmnSock/{1}.{2}'.format(
            self.platform.series, self.platform.version, self.platform.build)
        self.init(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        """ Overwrite this method if you need to do anything
            when an instance of this class is created.
        """
        pass
    
    def populate_objects(self):
        """ Populate our objects that are used to store information and stuff. """
        self.user = dAmnSock.user()
        self.flag = dAmnSock.flag()
        self.CONST = dAmnSock.CONST()
        self.connection = dAmnSock.connection()
        self.defer = dAmnSock.defer()
        self.protocol = self.protocol()
    
    def nullflags(self):
        """ Reset all status flags in this client. """
        self.flag = dAmnSock.flag()
    
    def set_protocol(self, protocol=None):
        """ Store the given IO protocol.
        
            This is in relation to the network connection.
        """
        self.io = protocol
        
        if protocol is None:
            self.onDisconnect()
        
    def start(self, *args, **kwargs):
        """ Start the client. """
        self.nullflags()
        
        self.connection.attempts = 1
        
        # Make sure we have an authtoken.
        self.authenticate()
        
        # Set up the client's main loop.
        self.defer.loop = reactor.callLater(1, self.mainloop, args, kwargs)
    
    def makeConnection(self):
        """ Open a connection to dAmn. """
        write_pair = self.get_write_pair()
        
        # Make a connection.
        self.conn = ConnectionFactory(self, write_pair[0], write_pair[1])
        reactor.connectTCP(self.CONST.SERVER, self.CONST.PORT, self.conn)
    
    def onDisconnect(self):
        """ Determine what we should do when we have fully lost our
            connection to the server.
        """
        
        if self.flag.quitting or not self.flag.reconnect:
            
            if self.flag.quitting:
                self.defer.teardown()
                try:
                    self.teardown()
                except Exception as e:
                    pass
                return
            
            if self.flag.retry:
                self.logger('~Global', '** Attempting to connect again...', False)
                self.connection.attempts+= 1
                self.authenticate()
                return
            
            self.defer.teardown()
            try:
                self.teardown()
            except Exception as e:
                pass
            return
        
        self.connection.attempts = 1
        self.logger('~Global', '** Attempting to reconnect...', False)
        self.authenticate()
    
    def teardown(self):
        """ Override this method to do stuff when the client gives up.
            It is a good idea to use this method to call reactor.stop().
        """
        pass
    
    def authenticate(self):
        """ Fetch the authtoken for the username and password given. """
        if not self.user.token:
            # If we don't have an authtoken, try and grab one!
            self.logger('~Global', '** Retrieving authtoken, this may take a while...', False)
            self.get_token()
            return
        
        self.makeConnection()
    
    def get_token(self):
        """ This is the method that actually handles grabbing the authtoken. """
        self.on_get_token()
        
        if not self.user.password:
            self.on_token()
            return
        
        self.gotSession(deviantART.Login(self.user.username,
            self.user.password, self.extras, self.agent))
    
    def gotSession(self, session):
        """ Deferred callback for deviantART.login.
            
            Called after we have attempted to log into deviantART.com.
            At least, it will be deferred in future. At the moment it's
            all synchronous.
            
            Damn...
        """
        self.session = session
        
        if self.session.status[0] == 1:
            self.user.cookie = self.session.cookie
            self.user.token = self.session.token
            self.user.password = None
            self.logger('~Global', '** Got an authtoken.', False)
            self.makeConnection()
            # on_token called second so that reactor.run() can be used there.
            self.on_token()
            return
        
        # Something went wrong! Maybe the user entered the wrong details?!
        self.logger('~Global', '>> Failed to get an authtoken.', False)
        self.logger('~Global', '>> {0}'.format(self.session.status[1]), False)
    
    def on_get_token(self):
        """Overwrite this method to do shit when get_token is called."""
        pass
    
    def on_token(self):
        """Overwrite this method to do stuff when we have an authtoken."""
        pass
    
    def mainloop(self, args, kwargs):
        """ This is the client's main loop. """
        self.on_loop(*args, **kwargs)
        self.defer.loop = reactor.callLater(1, self.mainloop, args, kwargs)
    
    def on_loop(self, *args, **kwargs):
        """ Overwrite this if you need to do anything on the main application loop. """
        pass
    
    def timedout(self):
        """ Timeout detected.
            
            If this method gets called, then the client has not received
            any data for 2 minutes. Assume disconnected.
        """
        self.handle_pkt(Packet('disconnect\ne=socket timed out\n\n'), time.time())
    
    def login(self):
        """ Send our login packet. Set the loggingin flag to true. """
        self.flag.loggingin = True
        return self.send('login {0}\npk={1}\n'.format(self.user.username, self.user.token))
    
    def send(self, data):
        """ Send data to dAmn! """
        if self.io is None:
            return 0
        return self.io.send_packet(data)
    
    def close(self):
        """ This is how we close our connection! """
        self.set_protocol()
        
        if self.timeout_delay is not None:
            self.timeout_delay.cancel()
            self.timeout_delay = None
    
    def format_ns(self, ns):
        """ This takes a dAmn channel name and formats it as a raw
            dAmn namespace.
        """
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
        """ This does the opposite of format_ns() """
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
    
    def handle_pkt(self, packet, stamp):
        """ Handle packets as they come in. """
        if self.defer.timeout is not None:
            self.defer.timeout.cancel()
        self.defer.timeout = reactor.callLater(self.timeout_delay, self.timedout)
        
        ns = '~Global'
        
        if packet.param:
            if packet.param[:5] in ('chat:', 'pchat'):
                ns = self.deform_ns(packet.param)
            elif packet.param[:6] == 'login:':
                ns = '@' + packet.param[6:]
        
        data = self.protocol.mapper(packet)
        loglist = self.protocol.logger(data['event'], data['rules'], ns, packet)
        
        if loglist is not None:
            self.logger(*loglist, ts=stamp)
        
        getattr(self, 'pkt_' + data['event'], self.pkt_unknown)(data['args'])
        self.pkt_generic(data)
        return data
    
    # PROTOCOL OUTPUT
    # The methods below pretty much define the protocol for outgoing packets.

    def raw(self, data):
        """ Send a raw dAmn packet. """
        return self.send(data)
        
    def pong(self):
        """ Send a pong packet to the server """
        return self.send('pong\n')
        
    def join(self, ns):
        """ Send a join packet to dAmn. """
        return self.send('join {0}\n'.format(ns))
        
    def part(self, ns):
        """ Send a part packet to dAmn. """
        return self.send('part {0}\n'.format(ns))
        
    def say(self, ns, message):
        """ Send a message to a dAmn channel namespace. """
        return self.send('send {0}\n\nmsg main\n\n{1}'.format(ns, str(message)))
    
    def action(self, ns, message):
        """ Send an action to a dAmn channel namespace. """
        return self.send('send {0}\n\naction main\n\n{1}'.format(ns, str(message)))
    
    def me(self, ns, message):
        """ This is just another way to do an action. """
        return self.action(ns, message)
        
    def npmsg(self, ns, message):
        """ Send a non-parsed message to a dAmn channel namespace. """
        return self.send('send {0}\n\nnpmsg main\n\n{1}'.format(ns, str(message)))
    
    def promote(self, ns, user, pc=None):
        """ Promote a user in a dAmn channel. """
        return self.send('send {0}\n\npromote {1}\n{2}'.format(ns, user, '' if pc == None else '\n'+str(pc)))
    
    def demote(self, ns, user, pc=None):
        """ Demote a user in a dAmn channel. """
        return self.send('send {0}\n\ndemote {1}\n{2}'.format(ns, user, '' if pc == None else '\n'+str(pc)))
    
    def kick(self, ns, user, r=None):
        """ Kick a user out of a dAmn channel. """
        return self.send('kick {0}\nu={1}\n{2}'.format(ns, user, '' if r == None else '\n'+str(r)))
    
    def ban(self, ns, user):
        """ Ban a user from a dAmn channel. """
        return self.send('send {0}\n\nban {1}\n'.format(ns, user))
    
    def unban(self, ns, user):
        """ Unban someone from a dAmn channel. """
        return self.send('send {0}\n\nunban {1}\n'.format(ns, user))
    
    def get(self, ns, p):
        """ Get a property for a dAmn channel. """
        return self.send('get {0}\np={1}\n'.format(ns, p))
    
    def set(self, ns, p, val):
        """ Set a property for a dAmn channel. """
        return self.send('set {0}\np={1}\n\n{2}'.format(ns, p, val))
    
    def admin(self, ns, command):
        """ Send an admin command to a dAmn channel. No need for multiple methods here. """
        return self.send('send {0}\n\nadmin\n\n{1}'.format(ns, command))
    
    def disconnect(self):
        """ Send a disconnect packet to the dAmn server. """
        return self.send('disconnect\n')
        
    def kill(self, ns, r=None):
        """ Send a kill packet to the dAmn server. """
        return self.send('kill {0}\n{1}'.format(ns, '' if r == None else '\n'+str(r)))
    
    # END PROTOCOL OUTPUT METHODS
    # BEGIN PROTOCOL INPUT METHODS
    # These methods process incomming data.
    
    def pkt_generic(self, data):
        """ We have received a packet!
            
            Override this method to do stuff whenever a packet is
            received. If you want to do stuff when a specific packet is
            received, define a new ``pkt_*`` method for that packet.
            
            If the method you are defining already exists, then you
            should call the original method from your own definition, so
            that the client does not break.
            
            Here, the method is given a dict as returned by the
            :py:class:`ProtocolParser <dAmnViper.parse.ProtocolParser>`
            method ``mapper``. Other ``pkt_*`` methods are only given
            the data under the ``args`` key of the dict returned by the
            ``mapper`` method.
        """
        pass
    
    def pkt_unknown(self, data):
        """ We received something unexpected. Oh well. """
        pass
    
    def pkt_dAmnServer(self, data):
        """ Received a dAmnServer packet.
            
            This method calls the ``login`` method of this class and
            sets the ``shaking`` flag to ``False``.
            
            This method is essential for connecting to dAmn properly.
        """
        self.flag.shaking = False
        self.login()
        
    def pkt_login(self, data):
        """ Received a login packet.
            
            When we receive a login packet, we need to determine whether
            the login was successful or not, and act based on that.
            
            This method closes the client if the login failed.
            Otherwise, the channels listed in the ``autojoin`` attribute
            are joined.
            
            This method is essential for connecting to dAmn properly.
        """
        
        self.flag.loggingin = False
        
        if data['e'] != 'ok':
            self.nullflags()
            self.close()
            return
        
        self.flag.loggingin = False
        self.flag.connecting = False
        self.flag.connected = True
        self.connection.attempts = 0
        
        for ns in self.autojoin:
            self.join(self.format_ns(ns))
    
    def pkt_join(self, data):
        """ Received a join packet.
            
            This is sent by the server when the client tries to join a
            channel on the server.
            
            If the join was successful, a :py:class:`Channel object
            <dAmnViper.data.Channel>` is created for the channel and
            stored in the ``channel`` attribute of the client.
            
            If the join failed, the client disconnects if there are no
            other joined channels. (``naive``)
        """
        if data['e'] == 'ok':
            self.channel[data['ns']] = Channel(
                data['ns'], self.deform_ns(data['ns'])
            )
            return
        
        if len(self.channel) > 0:
            return
        
        self.handle_pkt(Packet('disconnect\ne=no joined channels\n\n'), time.time())
    
    def pkt_part(self, data):
        """ Received a part packet.
            
            Similar to ``pkt_join``. This method determines whether or
            not the client is being kicked off the server.
        """
        if data['ns'] in self.channel.keys():
            del self.channel[data['ns']]
        
        if len(self.channel) > 0:
            return
        
        if 'r' in data.keys():
            if data['r'] in ('bad data', 'bad msg', 'msg too big') or 'killed:' in data['r']:
                self.handle_pkt(
                    Packet('disconnect{0}e={1}{2}{3}'.format("\n", data['r'], "\n", "\n")),
                    time.time())
                return
        
        if data['e'] != 'ok':
            return
        
        if self.channel or self.flag.disconnecting or self.flag.quitting:
            return
        
        self.handle_pkt(Packet('disconnect\ne=no joined channels\n\n'), time.time())
    
    def pkt_property(self, data):
        """ Received a channel property packet.
            
            This method makes sure that the information received is
            stored in the right place.
        """
        if data['p'] == 'info':
            return
        
        if not data['ns'] in self.channel.keys():
            return
        
        self.channel[data['ns']].process_property(data)
    
    def pkt_recv_join(self, data):
        """ Received a recv_join packet.
            
            This happens when a user joins a channel in which the client
            is also present.
            
            This method simply stores information about the user that
            just joined.
        """
        self.channel[data['ns']].register_user(Packet(data['info']), data['user'])
        
    def pkt_recv_part(self, data):
        """ Received a recv_part packet.
            
            This happens when a user leaves a channel in which the
            client is present.
            
            Here, we remove any records of the user being in the channel.
        """
        if not data['user'] in self.channel[data['ns']].member:
            return
        
        self.channel[data['ns']].member[data['user']]['con']-= 1
        
        if self.channel[data['ns']].member[data['user']]['con'] == 0:
            del self.channel[data['ns']].member[data['user']]
            
    def pkt_recv_kicked(self, data):
        """ Received a recv_kick packet.
            
            Similar to the ``pkt_recv_part`` method.
        """
        if not data['user'] in self.channel[data['ns']].member:
            return
        del self.channel[data['ns']].member[data['user']]
        
    def pkt_recv_privchg(self, data):
        """ Received a recv_privchg packet.
            
            This happens when a user's privclass is changed. All we do
            here is make sure the user is recorded as being in that
            privclass.
        """
        if not data['user'] in self.channel[data['ns']].member:
            return
        self.channel[data['ns']].member[data['user']]['pc'] = data['pc']
    
    def pkt_kicked(self, data):
        """ Received a kicked packet.
            
            This happens when the client is kicked from a channel.
            
            Here we automatically rejoin the channel if we are permitted
            to do so.
        """
        del self.channel[data['ns']]
        if self.flag.disconnecting or self.flag.quitting:
            return
        
        if 'r' in data.keys():
            if 'autokicked' in data['r'].lower() or 'not privileged' in data['r'].lower():
                if len(self.channel) > 0:
                    return
                self.handle_pkt(Packet('disconnect\ne=no joined channels\n\n'), time.time())
                return
        
        if self.flag.autorejoin:
            self.join(data['ns'])
    
    def pkt_disconnect(self, data):
        """ Received a disconnect packet from the server.
            
            Here we make sure the client does the right thing when a
            disconnect happens.
            
            This method is required for the client to work as expected.
        """
        self.flag.connected = False
        self.connection.disconnects+= 1
        self.channel = {}
        
        if self.flag.quitting:
            self.flag.close = True
            return
        
        if data['e'] == 'no joined channels' and len(self.autojoin) == 0:
            return
        
        if not self.flag.disconnecting:
            self.log('~Global', '>> Experiencing an unexpected disconnect.', False)
            self.log('~Global', '>> Attempting to reconnect in a moment.', False)
        
        time.sleep(1)
        self.nullflags()
        self.flag.reconnect = True
    
    # END PROTOCOL METHODS
    
    def parser(self):
        """ This method returns the :py:class:`Packet class
            <dAmnViper.parse.Packet>`.
        """
        return Packet
        
    def logger(self, ns, msg, showns=True, mute=False, pkt=None, ts=None):
        """ Write output to stdout. """
        if mute and not self.flag.debug:
            return
        
        stamp = time.strftime('%H:%M:%S', time.localtime(ts))
        ns = ns + '|' if showns else ''
        
        try:
            sys.stdout.write('{0}|{1} {2}\n'.format(stamp, ns, msg))
        except:
            sys.stdout.write('{0}| >> I failed to display a message! Sorry.\n'.format(stamp))
        sys.stdout.flush()
        
    def new_logger(self, ns='~Global', showns=True, mute=False):
        """ Returns a wrapped logger method. """
        @wraps(self.logger)
        def wrapper(msg):
            return self.logger(ns, msg, showns, mute)
        return wrapper
    
    def get_write_pair(self, showns=False):
        """ Returns a pair of wrapped logger methods. """
        return (self.new_logger(showns=False), self.new_logger(showns=False, mute=(not self.flag.debug)))

# EOF

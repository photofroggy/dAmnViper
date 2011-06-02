''' Example of a very basic dAmn bot!
    Created by photofroggy
'''

import sys
from twisted.internet import reactor

from dAmnViper.base import dAmnSock
from dAmnViper.examples.util import get_input

# Extend the dAmnViper.dAmnSock class to add some functionality.

class MyClient(dAmnSock):
    
    def init(self, username, password, admin, trigger='!', autojoin=None, callbacks=None):
        """ Initialise the client.
            
            Override this method if you need to do anything when an
            instance of the object is created. Do not override __init__
            directly.
            
            This seems like bad practice but it does mean you don't have
            to remember to call the original __init__ method.
            
            In this example, we simply store the variables given to the
            constructor.
        """
        self.user.username = username
        self.user.password = password
        self._admin = admin.lower()
        self.trigger = trigger
        self.autojoin = autojoin or ['Botdom']
        self.callbacks = callbacks or Commands()
    
    def on_token(self):
        """ This method is called when dAmnViper has an authtoken.
            
            Use this method to start the reactor if needed. We can
            assume we have everything needed to connect, as this method
            is only called when dAmnViper actually succeeds in getting
            an authtoken.
            
            Technically you can achieve the same behaviour by using
            something similar to this outside of the class::
                
                dAmn.start()
                if dAmn.flag.connecting:
                    reactor.run()
            
            Using this method just makes things a little cleaner on the
            outside, but not really.
        """
        reactor.run()
    
    def teardown(self):
        """ Overriding this method is required to stop the application.
            This method is called by dAmnSock when the client has
            determined that it no longer needs to keep connected to
            dAmn, and has been fully disconnected from the server.
            
            If reactor.stop() is not called at this point, the program
            will hang indefinitely. Overriding onDisconnect is not
            recommended!
        """
        reactor.stop()
    
    def pkt_recv_msg(self, data):
        """ Basic command handling provided here.
            
            This method is called by dAmnSock when a 'recv_msg' packet
            is sent to the client by the server. By this point, dAmnSock
            should already have displayed a message in stdout reporting
            the packet.
            
            It is possible to add specific handling of certain packets
            by defining other pkt_* methods, but note that some are
            already defined, and need to be called in order for dAmnSock
            to function as expected.
            
            This example simply looks for the trigger character in the
            message, and then passes the message to a command handler
            where appropriate.
        """
        if data['message'][:len(self.trigger)] == self.trigger:
            data['message'] = data['message'][len(self.trigger):]
            data['args'] = data['message'].split(' ')
            self.callbacks.handle(
                data['args'][0].lower(), data, self)


class Commands(object):
    """ Just a simple object to hold any command callbacks. """
    
    def handle(self, cmd, data, client):
        getattr(self, 'cmd_{0}'.format(cmd),
            self.unknown_cmd)(data, client)
    
    def unknown_cmd(self, data, client):
        pass
    
    def cmd_about(self, data, dAmn):
        """Basic command callback."""
        dAmn.say(data['ns'], data['user']+': Basic dAmn Viper bot by photofroggy.')
    
    def cmd_quit(self, data, dAmn):
        """Quit command! Enter the admin name in place of 'admin'!"""
        if data['user'].lower() != dAmn._admin:
            return
        dAmn.say(data['ns'], data['user']+': Closing down!')
        dAmn.flag.quitting = True
        dAmn.disconnect()
    
    def cmd_refresh(self, data, dAmn):
        """Quit command! Enter the admin name in place of 'admin'!"""
        if data['user'].lower() != dAmn._admin:
            return
        dAmn.say(data['ns'], data['user']+': Refreshing connection!')
        dAmn.flag.disconnecting = True
        dAmn.disconnect()
        

def configure():
    """ Sort of explains itself.
        
        This is simply a method to request configuration detials from
        the user, via stdin.
    """
    sys.stdout.write('>> We need some details to be able to run the bot\n')
    
    obj = [get_input('>> Username: '),
        get_input('>> Password: '),
        get_input('>> Admin: '),
        get_input('>> Trigger: '),
        [room.strip() for room in get_input('>> Autojoin: ', True).split(',')]
    ]
    
    while '' in obj[4]:
        obj[4].remove('')
    obj[4] = obj[4] or ['Botdom']
    
    return obj


if __name__ == '__main__':
    # Create a client
    sys.stdout.write('>> This is an example bot created with dAmn Viper.\n')
    
    try:
        dAmn = MyClient(*configure(), callbacks=Commands())
    except KeyboardInterrupt as e:
        sys.stdout.write('\n')
        sys.stdout.flush()
        sys.exit(0)
    
    sys.stdout.write('>> Starting the client...\n')
    sys.stdout.flush()
    
    # Start the dAmn client.
    dAmn.start()

# EOF

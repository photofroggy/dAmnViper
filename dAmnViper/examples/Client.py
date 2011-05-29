''' This is a basic example of how to create a basic dAmn client using dAmn Viper!
    Created by photofroggy
'''

from dAmnViper.base import Client

class client(Client):

    class user(Client.user):
        username = 'username'
        password = 'password'
    
    def __inst__(self):
        self.agent = 'Basic Client/1 (Python/3.0) dAmn Viper/' + self.platform.stamp
        self.logger('~Server', '** Retrieving authtoken, this may take a while...', False)
        self.get_token()
        if self.user.token == None:
            self.logger('~Server', '>> Failed to get authtoken.', False)
            return
        self.logger('~Server', '** Got an authtoken.', False)
        self.logger('~Server', '** Starting dAmn...', False)
        self.connect()
        if not self.flag.connecting:
            return
        self.handshake({'Client':'simple'})

    def mainloop(self):
        if not self.sock:
            return
        while self.sock.connected():
            datal = self.get_packets()
            if not datal: continue
            for data in datal:
                if not data: continue
                if hasattr(self, 'evt_' + data['event']):
                    getattr(self, 'evt_' + data['event'])(data['args'])
    
    # Some basic event handlers.
    def evt_login(self, data):
        if data['e'] == 'ok':
            self.join('chat:BotLab')
    
    def evt_join(self, data):
        if data['e'] == 'ok':
            self.say(data['ns'], 'Hello, world!')

# You would obviously need to make things more complicated to make it usable.

if __name__ == '__main__':
    app = client()
    app.mainloop()
    input('>> Press enter to exit...')
# EOF

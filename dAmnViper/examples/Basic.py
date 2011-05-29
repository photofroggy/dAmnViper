''' This is and even more basic dAmn client using dAmn Viper!
    Created by photofroggy
'''

from dAmnViper.base import Client

def main(user=None, password=None):
    if not user or not password:
        return
    client = Client()
    client.user.username = user
    client.user.password = password
    client.logger('~Server', '** Connecting...', False)
    client.get_token()
    if client.user.token == None:
        client.logger('~Server', '>> Login failed.', False)
        return
    client.connect()
    if not client.flag.connecting:
        return
    client.handshake({'Client':'simple'})
    
    # Main loop!
    while client.Socket.connected():
        packets = client.get_packets()
        if not packets:
            continue
        for data in packets:
            if data['event'] == 'login' and data['args']['e'] == 'ok':
                client.join('chat:Botlab')
            if data['event'] == 'join' and data['args']['e'] == 'ok':
                client.say(data['args']['ns'], 'Hello, world!')

if __name__ == '__main__':
    main('username', 'password')
    input('>> Press enter to exit...')
# EOF
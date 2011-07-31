''' dAmnViper.test.dummy.dapi module
    Created by photofroggy.
'''


import os
import sys
import os.path

os.chdir(os.path.dirname(__file__))
os.chdir('../../../')
sys.path.insert(0, os.getcwd())

import BaseHTTPServer


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    isLeaf = True
    
    def do_GET(self):
        pass
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.payload = self.rfile.read(int(self.headers.get('Content-length', '0')))
        
        if self.path == '/':
            self.wfile.write('{"lol": "wot"}')
        
        if '/user/whoami' in self.path:
            self.wfile.write('{"username": "photofroggy", "symbol": "~"}')
        
        self.wfile.close()
    
    def log_request(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer(('',8080), Handler)
    server.serve_forever()


# EOF

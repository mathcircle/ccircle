import ccircle
import json
import socketserver
import sys
import time

import config
import game
import util

LOCAL = '--local' in sys.argv

class GameClientHandler(socketserver.BaseRequestHandler):
    """ Responds to requests from clients by unpacking messages and passing them to
        the server's state object. """

    def handle(self):
        try:
            msg = json.loads(str(self.request.recv(config.SOCKET_BUFFER_SIZE), 'utf-8'))
            msg_name = msg.get('name', None)
            if not msg_name:
                self.respond('header is missing msg_name', None)
                return

            msg_data = msg.get('data', None)
            if msg_data:
                util.log('{}  --> {} {}'.format(self.client_address[0], msg_name, msg_data))
            else:
                util.log('{}  --> {}'.format(self.client_address[0], msg_name))

            status, data = self.server.handler._respond(self.client_address[0], msg_name, msg_data)
            self.respond(status, data)

        except Exception as e:
            util.log('!! {}  -->  < {} >'.format(self.client_address[0], e))
            self.respond('server_error', None)
            return

    def respond(self, status, data=None):
        try:
            response = {'status': status}
            if data:
                response['data'] = data
                util.log('{}  <-- {} {}'.format(self.client_address[0], status, data))
            else:
                util.log('{}  <-- {}'.format(self.client_address[0], status))
            self.request.sendall(bytes(json.dumps(response), 'utf-8'))
        except Exception as e:
            util.log('!! {}  <--  < {} >'.format(self.client_address[0], e))

window = ccircle.Window('Scenario 4 Server', 1024, 768)
if not LOCAL:
    window.toggleMaximized()

HOST = config.SERVER_HOST if not LOCAL else 'localhost'
PORT = config.SERVER_PORT

util.log('>> server started on {}:{} <<'.format(HOST, PORT))
server = socketserver.TCPServer((HOST, PORT), GameClientHandler)
server.state = game.State(window.getSize())
server.handler = game.MessageHandler(server.state)
server.timeout = 1.0 / 30.0

time_last = time.perf_counter()
while window.isOpen():
    window.clear(0.1, 0.1, 0.1)

    # Respond to messages
    server.handle_request()

    # Update step
    time_now = time.perf_counter()
    server.state.update(time_now - time_last)
    time_last = time_now

    # Draw
    server.state.draw(window)

    window.update()

util.log('>> server shutting down gracefully <<')

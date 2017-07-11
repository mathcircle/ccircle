import ccircle
import json
import socketserver
import time

import config
import gameconfig
import game

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
                print('{}  --> {} {}'.format(self.client_address[0], msg_name, msg_data))
            else:
                print('{}  --> {}'.format(self.client_address[0], msg_name))

            status, data = self.server.state._respond(self.client_address[0], msg_name, msg_data)
            self.respond(status, data)

        except Exception as e:
            print('!! {}  -->  < {} >'.format(self.client_address[0], e))
            self.respond('server_error', None)
            return

    def respond(self, status, data=None):
        try:
            response = {'status': status}
            if data:
                response['data'] = data
                print('{}  <-- {} {}'.format(self.client_address[0], status, data))
            else:
                print('{}  <-- {}'.format(self.client_address[0], status))
            self.request.sendall(bytes(json.dumps(response), 'utf-8'))
        except Exception as e:
            print('!! {}  <--  < {} >'.format(self.client_address[0], e))

window = ccircle.Window('Scenario 4 Server', 1024, 768)
window.toggleMaximized()

print('TCPServer listening on {}:{}'.format(config.SERVER_HOST, config.SERVER_PORT))
server = socketserver.TCPServer((config.SERVER_HOST, config.SERVER_PORT), GameClientHandler)
server.state = game.State(window.getSize())
server.timeout = 1.0 / 30.0

time_last = time.time()
while window.isOpen():
    window.clear(0.1, 0.1, 0.1)

    # Respond to messages
    server.handle_request()

    # Update step
    time_now = time.time()
    server.state._update(time_now - time_last)
    time_last = time_now

    # Draw
    server.state._draw(window)

    window.update()

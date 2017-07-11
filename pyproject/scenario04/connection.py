import json
import select
import socket
import time

import server.config as config


class _Connection:
    """ Wraps a connection to the Scenario 4 server.
        Despite using TCP, the connection is still opened and closed for each message,
        purely for simplicity of implementation. """

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._last_msg = time.time() - config.MIN_REQUEST_WAIT

    def send(self, msg_name, msg_data=None):
        """ Send a message then wait for and return a response from the connection.
            Messages and responses are both in the form of Python dictionaries. """

        # Check arguments
        if type(msg_name) != str:
            raise TypeError('Send expected string for argument 1 (msg_name), instead got {}'.format(type(msg_name)))
        if msg_data and type(msg_data) != dict:
            raise TypeError('Send expected a dict for argument 2 (msg_data), instead got {}'.format(type(msg_data)))

        # Throttle request rate using a simple sleep
        while time.time() - self._last_msg < config.MIN_REQUEST_WAIT:
            time.sleep(config.MIN_REQUEST_WAIT)
        self._last_msg = time.time()

        # Open a connection
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self._host, self._port))
        except Exception as e:
            print('ERROR: Failed to connect to server: {}'.format(e))
            return None

        # Encode and send message
        try:
            msg = {'name': msg_name}
            if msg_data:
                msg['data'] = msg_data
            raw = bytes(json.dumps(msg), 'utf-8')
            if len(raw) > config.MAX_MESSAGE_SIZE:
                print('ERROR: Message exceeded maximum size')
                return None
            sock.send(raw)
        except Exception as e:
            print('ERROR: {}'.format(e))
            return None

        # Wait for, decode, and return reply
        try:
            response = json.loads(str(sock.recv(config.SOCKET_BUFFER_SIZE), 'utf-8'))
            status = response['status']
            if status != config.STATUS_GOOD:
                print('ERROR: Server responded with error: {}'.format(status))
                return None
            return response.get('data', None)
        except Exception as e:
            print('ERROR: {}'.format(e))
            return None


def create():
    return _Connection(config.SERVER_HOST, config.SERVER_PORT)

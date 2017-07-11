import common
from http import HTTPStatus
import http.server

DEFAULT_ENCODING = "utf-8"
CANONICAL_CONTENT_TYPE = "application/json"
HOST = common.SERVER_HOST
PORT = common.SERVER_PORT


class Handler(http.server.SimpleHTTPRequestHandler):
    """Handles HTTP GET requests to the server."""

    def write_response(self, response):
        self.wfile.write(bytes(response, DEFAULT_ENCODING))

    def do_GET(self):
        # Send response code.
        self.send_response(HTTPStatus.OK)

        # Send headers.
        self.send_header('Content-type', CANONICAL_CONTENT_TYPE)
        self.end_headers()

        # TODO: Do something with request.
        print('path={path}'.format(path=self.path))

        # Write response.
        self.write_response("Hi from the server.")

print('Server listening on {host}:{port}...'.format(host=HOST, port=PORT))
server = http.server.HTTPServer((HOST, PORT), Handler)
server.serve_forever()

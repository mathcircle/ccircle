import http.server
import socketserver
from http import HTTPStatus

HOST = "127.0.0.1"
PORT = 8000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("<html>Received GET with path {}</html>".format(self.path))

    def respond(self, data):
        data = bytes(data, "utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

with socketserver.TCPServer((HOST, PORT), Handler) as server:
    print("Running server on {}:{}".format(HOST, PORT))
    server.serve_forever()

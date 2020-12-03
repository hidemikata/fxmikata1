from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from threading import Thread
from Controller.webserver_routes import urls

address = ('localhost', 8080)


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('path = {}'.format(self.path))
        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))
        query = parse_qs(parsed_path.query)
        limit = 100
        if 'limit' in query:
            limit = query['limit'][0]

        if parsed_path.path not in urls:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'notfound')
            return

        response_body = urls[parsed_path.path](limit)

        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response_body.encode())

    def do_POST(self):
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))

        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        content_length = int(self.headers['content-length'])

        print('body = {}'.format(self.rfile.read(content_length).decode('utf-8')))

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Hello from do_POST')


def start():
    with HTTPServer(address, MyHTTPRequestHandler) as server:
        server.serve_forever()


def start_server():
    t = Thread(target=start)
    t.start()


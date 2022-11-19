from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text')
        self.end_headers()
        self.wfile.write('Look at me'.encode())


def main():
    PORT= 8000
    server= HTTPServer(('', PORT), Handler)
    print(f'Server running on port {PORT}')
    server.serve_forever()

if __name__=='__main__':
    main()
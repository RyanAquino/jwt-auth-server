import socketserver
import http.server
import ssl


httpd = socketserver.TCPServer(('localhost', 80), http.server.SimpleHTTPRequestHandler)


httpd.socket = ssl.wrap_socket(httpd.socket,
                               certfile='localhost.crt',
                               keyfile='localhost.key',
                               server_side=True
                               )

httpd.serve_forever()

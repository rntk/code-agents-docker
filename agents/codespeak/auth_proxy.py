#!/usr/bin/env python3
import http.server
import http.client
import sys

# Configuration
LISTEN_PORT = 8081
TARGET_HOST = 'localhost'
TARGET_PORT = 8080

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request('GET')

    def do_POST(self):
        self.proxy_request('POST')

    def proxy_request(self, method):
        try:
            # Prepare connection to the local tool server
            conn = http.client.HTTPConnection(TARGET_HOST, TARGET_PORT)
            
            # Read body if it's a POST request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Forward the request
            conn.request(method, self.path, body, self.headers)
            response = conn.getresponse()
            
            # Send response back to the browser
            self.send_response(response.status)
            for header, value in response.getheaders():
                # Avoid passing through transfer-encoding or connection headers that might conflict
                if header.lower() not in ['transfer-encoding', 'connection']:
                    self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())
            
        except ConnectionRefusedError:
            self.send_error(502, f"Target {TARGET_HOST}:{TARGET_PORT} is not responding. Is the tool running?")
        except Exception as e:
            self.send_error(500, f"Proxy error: {str(e)}")

def run():
    server_address = ('0.0.0.0', LISTEN_PORT)
    httpd = http.server.HTTPServer(server_address, ProxyHandler)
    print(f"Proxy started on 0.0.0.0:{LISTEN_PORT} -> http://{TARGET_HOST}:{TARGET_PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

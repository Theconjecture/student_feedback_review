import http.server
import socketserver
import webbrowser
from urllib.parse import parse_qs

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print("Received POST data:", post_data.decode('utf-8'))

            # Simulate a successful login response
            self.send_response(301)
            self.send_header('Location', '/feedback.html')
            self.end_headers()
        
        elif self.path == '/submit_review':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse_qs(post_data.decode('utf-8'))
            print("Received Review data:", form_data)

            # Redirect to the submitted page with course code and lecturer name as query parameters
            course_code = form_data['course_code'][0]
            lecturer_name = form_data['lecturer_name'][0]
            self.send_response(301)
            self.send_header('Location', f'/submitted.html?course_code={course_code}&lecturer_name={lecturer_name}')
            self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith('/review.html'):
            self.path = '/review.html'
            super().do_GET()
        else:
            super().do_GET()

handler_object = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print(f"Serving on port {PORT}")
    webbrowser.open(f'http://localhost:{PORT}/login.html')
    httpd.serve_forever()

import json
import os
import smtplib
from http.server import BaseHTTPRequestHandler, HTTPServer
from email.message import EmailMessage


class Handler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_POST(self):
        if self.path != '/send-mail':
            self.send_error(404)
            return

        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        try:
            payload = json.loads(data)
            name = payload['name']
            email = payload['email']
            message = payload['message']
        except Exception:
            self.send_error(400, 'Invalid JSON')
            return

        smtp_host = os.environ.get('SMTP_HOST')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASS')
        secure = os.environ.get('SMTP_SECURE', 'false').lower() == 'true'

        msg = EmailMessage()
        msg['Subject'] = 'Website Contact Form'
        msg['From'] = f"{name} <{email}>"
        msg['To'] = 'matthijsthart@icloud.com'
        msg.set_content(message)

        try:
            if secure:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port)
            else:
                server = smtplib.SMTP(smtp_host, smtp_port)
                server.starttls()
            if smtp_user:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            self.send_response(200)
            self._send_cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"success":true}')
        except Exception as exc:
            print('Error sending mail:', exc)
            self.send_response(500)
            self._send_cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"success":false}')


def run():
    port = int(os.environ.get('PORT', '3000'))
    server = HTTPServer(('', port), Handler)
    print(f'Server running on port {port}')
    server.serve_forever()


if __name__ == '__main__':
    run()


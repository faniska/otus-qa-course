import re
import socket


class MySocketClient:
    host = None
    response_str = ''
    response_headers = []
    response_body = ''
    response_code = None

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def __del__(self):
        if self.sock:
            self.sock.close()
            del self.sock

    def connect(self, host, port):
        self.host = host
        self.sock.connect((host, port))
        return self

    def send(self, method, path, headers=None):
        request_headers = [
            f'{method} {path} HTTP/1.1',
            f'Host: {self.host}',
        ]
        if isinstance(headers, list):
            request_headers += headers
        request_headers.append('\n')
        request = '\n'.join(request_headers)
        print(request)
        self.sock.sendall(request.encode())
        return self

    def response(self):
        prev_timeout = self.sock.gettimeout()
        response_bytes = b''
        try:
            self.sock.settimeout(1)
            while True:
                try:
                    response_bytes += self.sock.recv(4096)
                except socket.timeout:
                    self.response_str = response_bytes.decode('utf-8')
                    return self
            # unreachable
        finally:
            self.sock.settimeout(prev_timeout)

    def split_response(self):
        if self.response_str:
            response_lines = map(str.strip, self.response_str.split("\n"))
            read_header = True
            for line in response_lines:
                if not line:
                    continue
                code_search = re.search(r'HTTP/1.1 (\d+) (\w+)', line)
                if code_search:
                    self.response_code = int(code_search.groups()[0])
                if 'DOCTYPE' in line:
                    read_header = False
                if read_header:
                    self.response_headers.append(line)
                else:
                    self.response_body += line
        return {
            'body': self.response_body,
            'code': self.response_code,
            'headers': self.response_headers
        }


MySock = MySocketClient()
response = MySock.connect('opencart.xfanis.ru', 80).send(
    'GET',
    '/',
    ['Accept: text/html'],
).response().split_response()

response

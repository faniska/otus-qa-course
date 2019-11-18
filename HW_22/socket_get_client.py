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
        request_headers.append('\r\n\r\n')
        request = '\r\n'.join(request_headers)
        print(request)
        self.sock.sendall(request.encode())
        return self

    def response(self):
        prev_timeout = self.sock.gettimeout()
        response_bytes = b''
        try:
            self.sock.settimeout(1)
            read = True
            while read:
                try:
                    piece = self.sock.recv(4096)
                    response_bytes += piece
                    read = len(piece) > 0
                except socket.timeout:
                    read = False
            # unreachable
        finally:
            self.sock.settimeout(prev_timeout)
            self.response_str = response_bytes.decode('utf-8')
            return self

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
response = MySock.connect('www.protesting.ru', 80).send(
    'GET',
    '/',
    ['Accept: text/html'],
).response().split_response()

response

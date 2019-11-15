import socket
import struct


class MySocketClient:
    host = None
    response_str = ''
    response_headers = []
    response_body = ''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

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

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msg_len = self.recv_all(4)
        if not raw_msg_len:
            return None
        msg_len = struct.unpack('>I', raw_msg_len)[0]
        # Read the message data
        return self.recv_all(msg_len)

    def recv_all(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def response(self):
        response_bytes = self.recv_msg()
        if response_bytes:
            self.response_str = response_bytes.decode('utf-8')
        return self

    def split_response(self):
        if self.response_str:
            response_lines = map(str.strip, self.response_str.split("\n"))
            read_header = True
            for line in response_lines:
                if not line:
                    continue
                if line == 'e3f':
                    read_header = False
                    continue
                if read_header:
                    self.response_headers.append(line)
                else:
                    self.response_body += line
        return {'body': self.response_body, 'headers': self.response_headers}


MySock = MySocketClient()
response = MySock.connect('opencart.xfanis.ru', 80).send(
    'GET',
    '/index.php?route=product/category&path=20_27',
    ['Accept: text/html'],
).response().split_response()

response

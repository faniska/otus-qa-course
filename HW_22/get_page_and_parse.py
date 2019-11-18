from pprint import pprint

from HW_22 import MySocketClient
from HW_22 import MyHTMLParser

my_socket_client = MySocketClient()

response = my_socket_client.connect('opencart.xfanis.ru', 80). \
    send('GET', '/', ['Accept: text/html']). \
    response(). \
    split_response()

parser = MyHTMLParser()
parser.feed(response['body'])

top_by_tags = sorted(parser.all['count'].items(), key=lambda e: e[1], reverse=True)
print('Top by tags:')
pprint(top_by_tags)

print('Links:')
pprint(parser.links)

print('Images:')
pprint(parser.images)

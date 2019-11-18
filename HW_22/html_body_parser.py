from html.parser import HTMLParser
from pprint import pprint

from HW_22.socket_get_client import MySocketClient


class MyHTMLParser(HTMLParser):
    links = []
    images = []
    tags = {}

    current_data = None

    all = {
        'tag': [],
        'data': [],
        'count': {},
    }

    def handle_data(self, data):
        self.all['data'].append(data)

    def handle_starttag(self, tag, attrs):
        self.all['tag'].append(tag)
        self.count_tags(tag)
        if tag == 'a':
            self.collect_links(attrs)
        elif tag == 'img':
            self.collect_images(attrs)

    def count_tags(self, tag):
        if tag not in self.all['count']:
            self.all['count'][tag] = 1
        else:
            self.all['count'][tag] += 1

    def collect_links(self, attrs):
        for attr in attrs:
            if attr[0] == 'href':
                if not self.validate_link(attr[0]):
                    self.links.append(attr[1])

    def validate_link(self, link):
        return any([
            link in self.links,
            '#' == link[0],
            'javascript:' == link[:11],
        ])

    def collect_images(self, attrs):
        for attr in attrs:
            if attr[0] == 'src':
                if not self.validate_image(attr[0]):
                    self.images.append(attr[1])

    def validate_image(self, img):
        return img in self.images



response = MySocketClient().connect('opencart.xfanis.ru', 80).send(
    'GET',
    '/',
    ['Accept: text/html'],
).response().split_response()


parser = MyHTMLParser.feed(response['body'])

top_by_tags = sorted(parser.all['count'].items(), key=lambda e: e[1], reverse=True)
print('Top by tags:')
pprint(top_by_tags)

print('Links:')
pprint(parser.links)


print('Images:')
pprint(parser.images)


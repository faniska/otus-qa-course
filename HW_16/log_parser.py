import argparse
import re
import json

parser = argparse.ArgumentParser(description='Process access logs')
parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
parser.add_argument('-d', dest='folder', action='store', help='Path to log folder')

args = parser.parse_args()

dict_ip = {}

request_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS']
def_res_dict = {m: 0 for m in request_methods}
res = {}
total = {'count': 0, 'methods': dict(def_res_dict), 'requests': {}, 'errors': {'client': {}, 'server': {}}}


def append_error(total, request, code, error_type):
    if code not in total['errors'][error_type]:
        total['errors']['client'][code] = {}
    if request not in total['errors'][error_type][code]:
        total['errors'][error_type][code][request] = 1
    else:
        total['errors'][error_type][code][request] += 1


with open(args.file) as file:
    for index, line in enumerate(file.readlines()):
        ip = None
        method = 'GET'

        ip_v4_search = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        if ip_v4_search:
            ip = ip_v4_search.group()
        else:
            # print(f'IPv4 N/A: {line}')
            continue

        method_search = re.search(r'\] \"({})'.format('|'.join(request_methods)), line)
        if method_search:
            method = method_search.groups()[0]
        else:
            # print(f'Method N/A: {line}')
            continue

        request_search = re.search(r'\] \"(({}).*?)\"'.format('|'.join(request_methods)), line)
        if request_search:
            request = request_search.groups()[0]
            if request not in total['requests']:
                total['requests'][request] = 1
            else:
                total['requests'][request] += 1

            code_search = re.search(r'\" (\d+) (\d+)', line)
            if code_search:
                code = int(code_search.groups()[0])
                if 400 <= code < 500:
                    append_error(total, request, code, 'client')
                elif 500 <= code < 600:
                    append_error(total, request, code, 'server')

        if ip not in res:
            res[ip] = {
                'methods': dict(def_res_dict),
                'count': 0
            }

        res[ip]['methods'][method] += 1
        res[ip]['count'] += 1
        total['count'] += 1
        total['methods'][method] += 1

sorted_by_count = sorted(res.items(), key=lambda r: r[1]['count'], reverse=True)

top_10_count = sorted_by_count[:10]
print(json.dumps(total['errors'], indent=4))

print('Общее число обработанных запросов {}'.format(total['count']))
print('Кол-во запросов по методу:')
for method, count in total['methods'].items():
    print(f'\t{method}: {count}')
print('-----')

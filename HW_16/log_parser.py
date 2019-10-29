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
total = {'count': 0, 'methods': dict(def_res_dict)}
errors = {'client': {}, 'server': {}}


def append_error(errors, request, code, ip, error_type):
    if request not in errors[error_type]:
        errors[error_type][request] = {'count': 0, 'code': {}, 'ip': {}}
    errors[error_type][request]['count'] += 1
    if code not in errors[error_type][request]['code']:
        errors[error_type][request]['code'][code] = 1
    else:
        errors[error_type][request]['code'][code] += 1
    if ip not in errors[error_type][request]['ip']:
        errors[error_type][request]['ip'][ip] = 1
    else:
        errors[error_type][request]['ip'][ip] += 1


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
        if ip == '127.0.0.1':
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
            code_search = re.search(r'\" (\d+) (\d+)', line)
            if code_search:
                code = int(code_search.groups()[0])
                if 400 <= code < 500:
                    append_error(errors, request, code, ip, 'client')
                elif 500 <= code < 600:
                    append_error(errors, request, code, ip, 'server')

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
sorted_by_client_error = sorted(errors['client'].items(), key=lambda e: e[1]['count'], reverse=True)
sorted_by_server_error = sorted(errors['server'].items(), key=lambda e: e[1]['count'], reverse=True)

result_json = {
    'total': total,
    'top_10_ip': sorted_by_count[:10],
    'top_10_client_errors': sorted_by_client_error[:10],
    'top_10_server_errors': sorted_by_server_error[:10]
}
with open('result_json.json', 'w') as json_file:
    json_file.write(json.dumps(result_json, indent=4))

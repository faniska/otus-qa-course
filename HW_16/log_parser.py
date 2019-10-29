import argparse
import re
import json
import glob

parser = argparse.ArgumentParser(description='Process access logs')
parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
parser.add_argument('-d', dest='folder', action='store', help='Path to log folder')


class LogParser:
    request_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS']

    res = {}
    total = {'count': 0, 'methods': {}}
    errors = {'client': {}, 'server': {}}
    args = parser.parse_args()
    log_file_list = []

    def __init__(self):
        self.total['methods'] = {m: 0 for m in self.request_methods}
        if self.args.file:
            self.log_file_list += [self.args.file]
        if self.args.folder:
            self.log_file_list += glob.glob('{}/*.log'.format(self.args.folder))

    def parse_files(self):
        for file_path in self.log_file_list:
            print(f'Parse: {file_path}')
            self.parse_file(file_path)
        return self

    def parse_file(self, file_path):
        with open(file_path) as file:
            for index, line in enumerate(file.readlines()):
                ip_v4_search = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                if ip_v4_search:
                    ip = ip_v4_search.group()
                else:
                    # print(f'IPv4 N/A: {line}')
                    continue
                if ip == '127.0.0.1':
                    continue
                method_search = re.search(r'\] \"({})'.format('|'.join(self.request_methods)), line)
                if method_search:
                    method = method_search.groups()[0]
                else:
                    # print(f'Method N/A: {line}')
                    continue

                request_search = re.search(r'\] \"(({}).*?)\"'.format('|'.join(self.request_methods)), line)
                if request_search:
                    request = request_search.groups()[0]
                    code_search = re.search(r'\" (\d+) (\d+)', line)
                    if code_search:
                        code = int(code_search.groups()[0])
                        if 400 <= code < 500:
                            self.append_error(request, code, ip, 'client')
                        elif 500 <= code < 600:
                            self.append_error(request, code, ip, 'server')

                if ip not in self.res:
                    self.res[ip] = {
                        'methods': {m: 0 for m in self.request_methods},
                        'count': 0
                    }

                self.res[ip]['methods'][method] += 1
                self.res[ip]['count'] += 1
                self.total['count'] += 1
                self.total['methods'][method] += 1

        return self

    def append_error(self, request, code, ip, error_type):
        if request not in self.errors[error_type]:
            self.errors[error_type][request] = {'count': 0, 'code': {}, 'ip': {}}
        self.errors[error_type][request]['count'] += 1
        if code not in self.errors[error_type][request]['code']:
            self.errors[error_type][request]['code'][code] = 1
        else:
            self.errors[error_type][request]['code'][code] += 1
        if ip not in self.errors[error_type][request]['ip']:
            self.errors[error_type][request]['ip'][ip] = 1
        else:
            self.errors[error_type][request]['ip'][ip] += 1

    def save_result(self):
        sorted_by_count = sorted(self.res.items(), key=lambda r: r[1]['count'], reverse=True)
        sorted_by_client_error = sorted(self.errors['client'].items(), key=lambda e: e[1]['count'], reverse=True)
        sorted_by_server_error = sorted(self.errors['server'].items(), key=lambda e: e[1]['count'], reverse=True)

        result_json = {
            'total': self.total,
            'top_10_ip': sorted_by_count[:10],
            'top_10_client_errors': sorted_by_client_error[:10],
            'top_10_server_errors': sorted_by_server_error[:10]
        }
        with open('result_json.json', 'w') as json_file:
            json_file.write(json.dumps(result_json, indent=4))


log_parser = LogParser()
log_parser.parse_files().save_result()

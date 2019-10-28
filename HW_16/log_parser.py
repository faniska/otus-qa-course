import argparse
import re
import json

parser = argparse.ArgumentParser(description='Process access logs')
parser.add_argument('-f', dest='file', action='store', help='Path to logfile')
parser.add_argument('-d', dest='folder', action='store', help='Path to log folder')

args = parser.parse_args()

dict_ip = {}

request_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
def_res_dict = {m: 0 for m in request_methods}
res = {}

with open(args.file) as file:
    for index, line in enumerate(file.readlines()):
        ip = None
        method = 'GET'

        ip_v4_search = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        if ip_v4_search:
            ip = ip_v4_search.group()

        method_search = re.search(r'\] \"({})'.format('|'.join(request_methods)), line)
        if method_search:
            method = method_search.groups()[0]

        if ip not in res:
            res[ip] = dict(def_res_dict)

        res[ip][method] += 1

print(json.dumps(res, indent=4))

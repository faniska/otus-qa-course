import os
import subprocess


def show_package_version(package):
    subprocess.check_call(f'pip3 freeze | grep {package}', shell=True)


def show_dir_content(path):
    subprocess.check_call(f'ls {path}', shell=True)


print('Network Interfaces')
subprocess.check_call(['netstat', '-i'])
print('----------')

print('Default Routing')
subprocess.check_call(['netstat', '-rn'])
print('----------')

print('Processor Usage')
cmd = """ps -A -o %cpu | awk '{s+=$1} END {print s "%"}'"""
subprocess.check_call(cmd, shell=True)
print('----------')

print('Processor Info')
subprocess.check_call(['sysctl', '-n', 'machdep.cpu.brand_string'])
print('----------')

print('Process Info')
subprocess.check_call('ps aux | grep [p]ython', shell=True)
print('----------')

print('All Processes')
subprocess.check_call(['ps', 'aux'])
print('----------')

print('Show apache2 status')
try:
    subprocess.check_call(['service', 'apache2', 'status'])
except FileNotFoundError as e:
    print('Command not found')
print('----------')

print('Port 6942 status')
subprocess.check_call('lsof -i :6942', shell=True)
print('----------')

print('Show python package version')
show_package_version('requests')
print('----------')

print('Show dir content')
show_dir_content('/')
print('----------')

print('Show current directory')
subprocess.check_call(['pwd'])
print('----------')

print('Show kernel version')
subprocess.check_call('uname -r', shell=True)
print('----------')

print('Show operating system version')

if os.uname()[0] == 'Darwin':
    subprocess.check_call('sw_vers', shell=True)
elif os.uname()[0] == 'Linux':
    subprocess.check_call('lsb_release -d', shell=True)

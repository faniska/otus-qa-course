import subprocess

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
print('--   --------')

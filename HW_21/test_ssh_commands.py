import time

import paramiko
import pytest
import requests

from assets.project_logger import ProjectLogger


class TestSSH:
    host = '192.168.64.2'
    user = 'opencart'
    password = 'opencart1'
    logger = ProjectLogger('SSH').logger

    @pytest.fixture()
    def ssh_client(self, request):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.user, password=self.password)
        request.addfinalizer(client.close)
        return client

    def test_apache2_status(self, ssh_client: paramiko.SSHClient):
        ssh_client.exec_command('sudo service apache2 restart')
        time.sleep(5)
        stdin, stdout, stderr = ssh_client.exec_command('sudo service apache2 status')
        data = stdout.read()
        response = data.decode('utf-8')
        assert 'Active: active (running)' in response

    def test_mysql_status(self, ssh_client: paramiko.SSHClient):
        ssh_client.exec_command('sudo service mysql restart')
        time.sleep(5)
        stdin, stdout, stderr = ssh_client.exec_command('sudo service mysql status')
        data = stdout.read()
        response = data.decode('utf-8')
        assert 'Active: active (running)' in response, 'Service inactive'

    def test_restart_server(self, ssh_client: paramiko.SSHClient):
        self.logger.debug(f'Reboot server and check site status')
        ssh_client.exec_command('sudo reboot')
        time.sleep(30)
        attempt = 0
        while attempt < 10:
            time.sleep(5)
            attempt += 1
            self.logger.debug(f'Attempt: {attempt}')
            try:
                x = requests.head('http://opencart.ubuntu-vm.localhost')
                self.logger.debug(f'Status: {x.status_code}')
            except requests.exceptions.RequestException as e:
                self.logger.error(e)
                continue
            if x.status_code == 200:
                break

        assert x.status_code == 200, 'Wrong status code'

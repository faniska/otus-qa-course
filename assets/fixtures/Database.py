import pymysql
import pytest


class Database:

    @pytest.fixture
    def db_cursor(self, request):
        password = request.config.getoption("--db-password")
        if not password:
            raise UserWarning('Please set DB password')
        db_params = {
            'host': '95.216.187.7',
            'user': 'opencart-test-user',
            'db': 'opencart',
            'password': password
        }
        connection = pymysql.connect(**db_params)
        request.addfinalizer(connection.close)
        return connection.cursor()

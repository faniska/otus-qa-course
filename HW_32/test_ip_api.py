import json

import pytest
import requests
import requests_mock


@pytest.mark.parametrize('ip_address', ['24.48.0.1', '178.204.157.15'])
def test_get_ip(ip_address):
    """
    Без мока сервис возвращает Canada, Russia
    С моком - всегда Russia
    """
    mock_dict = {
        'country': 'Russia',
        'countryCode': 'RU'
    }
    url = f"http://ip-api.com/json/{ip_address}"
    with requests_mock.mock() as mock:
        mock.get(url, text=json.dumps(mock_dict))
    response = requests.get(url).json()
    assert response.get('country') == 'Russia'

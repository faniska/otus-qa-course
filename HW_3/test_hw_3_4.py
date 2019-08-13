import pytest

from HW_3.api_client import APIClient


@pytest.fixture(scope="module")
def api_client(request):
    base_url = request.config.getoption("--url")
    return APIClient(base_address=base_url)


@pytest.fixture(scope="module")
def expected_encoding(request):
    return request.config.getoption("--encoding").upper()


def test_check_page_encoding(api_client, expected_encoding):
    """
    Check if response encoding is as expected
    """
    response = api_client.get()

    assert response.encoding.upper() == expected_encoding

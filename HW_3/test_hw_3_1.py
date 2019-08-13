import pytest

from HW_3.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    base_url = 'https://dog.ceo/'
    return APIClient(base_address=base_url)


@pytest.mark.parametrize('number', [2, 3, 4])
def test_api_check_number_of_messages(api_client, number):
    """
    Check if api returns as many pictures as specified in the parameters
    """
    res = api_client.get(path="api/breed/hound/images/random/" + str(number)).json()
    assert len(res['message']) == number


@pytest.mark.parametrize("input_data, expected_type", [(None, str), (2, list)])
def test_api_check_type_of_message(api_client, input_data, expected_type):
    """
    Check if api returns url to image if no number given and returns list of urls if number given
    :return:
    """
    path = 'api/breed/hound/images/random/'
    if isinstance(input_data, int):
        path += str(input_data)
    res = api_client.get(path=path).json()
    assert isinstance(res['message'], expected_type)


def test_api_check_breed_list(api_client):
    """
    Check if api correctly returns bread list
    """
    res = api_client.get(path='api/breeds/list/all').json()
    assert res['status'] == 'success'


@pytest.mark.parametrize("breed, expected_status", [('hound', 'success'), ('hound2', 'error')])
def test_api_check_breed(api_client, breed, expected_status):
    """
    Check if api returns response with correct status
    :return:
    """
    res = api_client.get(path='api/breed/{}/images'.format(breed)).json()
    assert res['status'] == expected_status


@pytest.mark.parametrize("breed, sub_bread_exists", [('hound', True), ('bulldog', True), ('chihuahua', False)])
def test_api_check_sub_breed(api_client, breed, sub_bread_exists):
    """
    Check if api correctly return sub-breeds by breed
    """
    res = api_client.get(path='api/breeds/list/all'.format(breed)).json()
    assert bool(res['message'][breed]) == sub_bread_exists

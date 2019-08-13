import pytest


@pytest.mark.parametrize('number', [2, 3, 4])
def test_api_check_number_of_messages(api_client, number):
    """
    Check if api returns as many pictures as specified in the parameters
    """
    res = api_client.get(path="api/breed/hound/images/random/" + str(number)).json()
    assert len(res['message']) == number


#def test_api_ckeck_type_of_message()

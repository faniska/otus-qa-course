import pytest

from HW_3.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    base_url = 'https://jsonplaceholder.typicode.com/'
    return APIClient(base_address=base_url)


def test_api_check_fields_list(api_client):
    """
    Check json scheme
    """
    fields = ['userId', 'id', 'title', 'body']
    post = api_client.get(path='posts/1').json()
    assert set(post.keys()) == set(fields)


@pytest.mark.parametrize('user_id', [1, 2])
def test_api_check_user_filter(api_client, user_id):
    """
    Check if api correctly filters posts by user id
    """
    posts = api_client.get(path='posts', params={'userId': user_id}).json()
    user_ids = [p['userId'] for p in posts]
    assert set(user_ids) == set([user_id])


@pytest.mark.parametrize('post_id, expected_status_code', [(1, 200), (10000000, 404)])
def test_check_api_status_code(api_client, post_id, expected_status_code):
    """
    Check if api returns correct status code
    """
    res = api_client.get(path=f'posts/{post_id}')
    assert res.status_code == expected_status_code


@pytest.mark.parametrize('post_id', [1, 2])
def test_check_api_comments(api_client, post_id):
    """
    Check if api correctly filters posts by post id
    """
    posts = api_client.get(path='comments', params={'postId': post_id}).json()
    post_ids = [p['postId'] for p in posts]
    assert set(post_ids) == set([post_id])


@pytest.mark.parametrize('user_id', [1, 2])
def test_check_api_existing_email(api_client, user_id):
    """
    Check if users have email
    """
    res = api_client.get(path=f'users/{user_id}').json()
    email = res.get('email')
    assert isinstance(email, str) and '@' in email

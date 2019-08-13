# import pytest
#
# from HW_3.api_client import APIClient
#
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--url",
#         action="store",
#         default="https://dog.ceo/",
#         help="This is request url"
#     )
#
#
# @pytest.fixture(scope="session")
# def api_client(request):
#     base_url = request.config.getoption("--url")
#     return APIClient(base_address=base_url)

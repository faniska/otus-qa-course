import os
import pkgutil

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        required=True,
        help="This is request url"
    )

    parser.addoption(
        "--browser",
        action="store",
        required=True,
        help="browser: chrome or firefox"
    )
    parser.addoption(
        "--timeout",
        action="store",
        default=10,
        help="Implicit waiting time"
    )
    parser.addoption(
        "--db-password",
        action="store",
        default=False,
        help="DB Password"
    )


@pytest.mark.usefixtures("environment_info")
@pytest.fixture(scope='session', autouse=True)
def configure_html_report_env(request, environment_info):
    request.config._metadata.update(
        {
            "python_packages": environment_info[0],
            "path_value": environment_info[1]
        })
    yield


@pytest.fixture(scope="session")
def environment_info():
    python_packages = [pkg.name for pkg in pkgutil.iter_modules() if pkg.ispkg is True]
    path_value = os.environ['PATH']
    return python_packages, path_value

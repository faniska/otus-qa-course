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
        "--use-proxy",
        action="store",
        default=False,
        help="Implicit waiting time"
    )

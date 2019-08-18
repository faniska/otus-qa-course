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

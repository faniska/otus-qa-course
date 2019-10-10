# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def get_data_types(request):
    print("\nGetting data types by {}".format(request.node))
    return {
        'list': [1, 2, 3],
        'tuple': (1, 2, 3),
        'set': {1, 2, 3},
        'dict': {'first_name': 'Alex', 'last_name': 'Turner'},
        'str': 'Some Test String',
        'int': 10,
    }


@pytest.fixture(scope='module')
def module_fixture(request):
    print("{} fixture output - start\n-----".format(request.scope))

    def module_finalizer():
        print("\n-----\n{} fixture output - finish".format(request.scope))

    request.addfinalizer(module_finalizer)


@pytest.fixture(scope='session')
def session_fixture(request):
    print("{} fixture output - start\n-----".format(request.scope))

    def session_finalizer():
        print("\n-----\n{} fixture output - finish".format(request.scope))

    request.addfinalizer(session_finalizer)


def test_1_list_length(session_fixture, module_fixture, get_data_types):
    """
    Check len of given list
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert len(get_data_types['list']) == 3


def test_2_tuple_value(session_fixture, module_fixture, get_data_types):
    """
    Check if the first element of the given tuple is equal to 1
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert get_data_types['tuple'][0] == 1


def test_3_sum_list_values(session_fixture, module_fixture, get_data_types):
    """
    Check if the sum of given list values numbers is equal to 6
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert sum(get_data_types['list']) == 6


def test_4_dict_name_check(session_fixture, module_fixture, get_data_types):
    """
    Check if the given dictionary contains the name Alex
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert 'Alex' == get_data_types['dict']['first_name']


def test_5_dict_items_len(session_fixture, module_fixture, get_data_types):
    """
    Check if the given dictionary contains at least 2 values
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert len(get_data_types['dict'].values()) >= 2


def test_6_dict_check_fullname(session_fixture, module_fixture, get_data_types):
    """
    Check if the fullname from dict is equal to Alex Turner
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    fullname = '{first_name} {last_name}'.format(**get_data_types['dict'])
    assert fullname == 'Alex Turner'


def test_7_str_check_word(session_fixture, module_fixture, get_data_types):
    """
    Check if given string contains the Test word
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert 'Test' in get_data_types['str']


def test_8_is_integer_even(session_fixture, module_fixture, get_data_types):
    """
    Check if the given number is even
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert get_data_types['int'] % 2 == 0


def test_9_check_set_difference(session_fixture, module_fixture, get_data_types):
    """
    Check if there is at least one difference between two sets
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert len(get_data_types['set'].difference({2, 3})) > 0


def test_10_check_set_intersection(session_fixture, module_fixture, get_data_types):
    """
    Check if number of intersecting values of sets is equal to 2
    :param session_fixture: fixture for test session
    :param module_fixture: fixture for the module
    :param get_data_types: function fixture to prepare and get test data
    :return:
    """
    assert len(get_data_types['set'].intersection({2, 3})) == 2

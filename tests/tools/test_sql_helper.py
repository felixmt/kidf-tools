# python3 -m pytest -v --cov

"""modules imports
"""
import os
import pytest
from unittest import mock
from tools.sql_helper import sql_helper

@pytest.fixture
def sql_helper_object():
    """instantiate object as a fixture
    """
    return sql_helper()

# @pytest.fixture
# def example_date():
#     """ instantiate date as a fixture
#     """
#     return datetime.date(2022, 3, 7)

@pytest.fixture
def example_db_env():
    """ instantiate db env as a fixture
    """
    return "env_test"

def test_constructor(example_db_env):
    """test_constructor
    """
    instance = sql_helper("env_test")
    assert instance.db_env == example_db_env

    instance = sql_helper()
    assert isinstance(instance, sql_helper)

@mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)  # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
@mock.patch("psycopg2.connect")
def test_get_connection(sql_helper_object):
    # expected = [['fake', 'row', 1], ['fake', 'row', 2]]
    # with mock.patch('psycopg2.connect') as mock_connect:
    # mock_cur = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
    # mock_cur.fetchall.return_value = expected  # return this when calling cur.fetchall()

    result = sql_helper_object.get_connection()
    result_alchemy = sql_helper_object.get_connection("alchemy")
    # print(result)
    # print(type(result))
    # print(result_alchemy)
    # print(type(result_alchemy))
    assert os.environ["DB_HOSTNAME"] == "prospective"
    assert result == result_alchemy

@mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)  # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
@mock.patch("psycopg2.connect")
def test_select(mock_connect, sql_helper_object):
    expected = [['fake', 'row', 1], ['fake', 'row', 2]]
    query = "select * from test"
    params = []
    
    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
    mock_cur.fetchall.return_value = expected  # return this when calling cur.fetchall()

    result = sql_helper_object.select(query, params, True)

    assert result == expected

# def test_first_dow_in_a_month(date_helper_object, example_date):
#     """test_first_dow_in_a_month
#        looking for the first monday (0) in the month of march 2022
#     """
#     date = date_helper_object.first_dow_in_a_month(2022, 3, 0)

#     assert date == example_date

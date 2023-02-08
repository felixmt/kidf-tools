# python3 -m pytest -v --cov

"""modules imports
"""
import os
from unittest import mock
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pytest
from tools.sql_helper import sql_helper

### fixtures ###
@pytest.fixture
def sql_helper_object():
    """instantiate object as a fixture
    """
    return sql_helper()

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
### end fixtures


@mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
# why need clear=True explained here https://stackoverflow.com/a/67477901/248616
@mock.patch("psycopg2.connect")
def test_get_connection(sql_helper_object):
    """ test get connection
    """
    result = sql_helper_object.get_connection()
    result_alchemy = sql_helper_object.get_connection("alchemy")

    assert os.environ["DB_HOSTNAME"] == "prospective"
    assert result == result_alchemy


@mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
# why need clear=True explained here https://stackoverflow.com/a/67477901/248616
@mock.patch("psycopg2.connect")
def test_select(mock_connect, sql_helper_object):
    """ test select
    """
    expected = [['fake', 'row', 1], ['fake', 'row', 2]]
    query = "select * from test"
    params = []

    mock_con = mock_connect.return_value
    mock_cur = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
    mock_cur.fetchall.return_value = expected  # return this when calling cur.fetchall()

    result = sql_helper_object.select(query, params)

    assert result == expected

    result = sql_helper_object.select(query, params, return_sql_as_text = True)

    assert isinstance(result, str)


@mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective.database.com",
                              "DB_USER": "user",
                              "DB_PASSWORD": "passwd",
                              "DB_NAME": "name",
                              "DB_PORT": "10"}, clear=True)
# why need clear=True explained here https://stackoverflow.com/a/67477901/248616
@mock.patch("pandas.read_sql_query")
def test_select_into_dataframe(mock_read_sql, sql_helper_object):
    """ test select
    """
    df_expected = pd.DataFrame({"name": "df name",
                                'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
                                'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
    # df_expected['Coordinates'] = list(zip(df_expected.Longitude, df_expected.Latitude))
    # df_expected['Coordinates'] = df_expected['Coordinates'].apply(Point)
    # gdf_expected = gpd.GeoDataFrame(df_expected, geometry="Coordinates")

    query = "select * from test"
    params = {}

    mock_read_sql.return_value = df_expected

    result = sql_helper_object.select_into_dataframe(query, params)

    pd.testing.assert_frame_equal(result, df_expected)

    # mock_read_sql.return_value = gdf_expected
    # result = sql_helper_object.select_into_dataframe(query, params, is_geodataframe = True)

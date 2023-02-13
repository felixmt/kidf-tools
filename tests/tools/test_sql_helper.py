# python3 -m pytest -k TestSqlHelper -q tests/tools/test_sql_helper.py
"""modules imports
"""
import os
from unittest import mock
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from psycopg2.sql import SQL
import pytest
from tools.sql_helper import sql_helper

class TestSqlHelper:
    """ class to test navitia helper
    """
    ### fixtures ###
    @pytest.fixture
    @mock.patch.dict(os.environ, {"DB_SCHEMA": "db_schema"}, clear=True)
    def sql_helper_object(self):
        """instantiate object as a fixture
        """
        return sql_helper()

    @pytest.fixture
    def example_db_env(self):
        """ instantiate db env as a fixture
        """
        return "env_test"
    ### end fixtures ###

    def test_constructor(self, example_db_env):
        """test_constructor
        """
        instance = sql_helper(example_db_env)
        assert instance.db_env == example_db_env
        assert isinstance(instance, sql_helper)

        instance = sql_helper()
        assert isinstance(instance, sql_helper)


    @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
    # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    @mock.patch("psycopg2.connect")
    def test_get_connection(self, sql_helper_object):
        """ test get connection
        """
        result = sql_helper_object.get_connection()
        result_alchemy = sql_helper_object.get_connection("alchemy")

        assert os.environ["DB_HOSTNAME"] == "prospective"
        assert result == result_alchemy


    @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
    # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    @mock.patch("psycopg2.connect")
    def test_select(self, mock_connect, sql_helper_object):
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
    @mock.patch("geopandas.read_postgis")
    def test_select_into_dataframe(self, mock_read_postgis, mock_read_sql, sql_helper_object):
        """ test select
        """
        df_expected = pd.DataFrame({"name": "df name",
                                    "Latitude": [-34.58, -15.78, -33.45, 4.60, 10.48],
                                    "Longitude": [-58.66, -47.91, -70.66, -74.08, -66.86]})
        df_expected['Coordinates'] = list(zip(df_expected.Longitude, df_expected.Latitude))
        df_expected['Coordinates'] = df_expected['Coordinates'].apply(Point)
        gdf_expected = gpd.GeoDataFrame(df_expected, geometry="Coordinates")

        query = "select * from test"
        params = {}

        mock_read_sql.return_value = df_expected
        result = sql_helper_object.select_into_dataframe(query, params)
        pd.testing.assert_frame_equal(result, df_expected)

        mock_read_postgis.return_value = gdf_expected
        result = sql_helper_object.select_into_dataframe(query, params, is_geodataframe = True)
        pd.testing.assert_frame_equal(result, gdf_expected)


    @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
    # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    @mock.patch("psycopg2.connect")
    def test_insert(self, mock_connect, sql_helper_object):
        """ test insert
        """
        expected = 0
        query = "insert into test values (%s, %s, %s)"
        params = [1, 2, 3]

        result = sql_helper_object.insert(query, params=params)

        result = sql_helper_object.insert(query, params)

        assert result == expected


    # @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
    # # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    # @mock.patch("psycopg2.connect")
    # def test_insert_batch(mock_connect, sql_helper_object):
    #     """ test insert
    #     """
    #     query = "insert into test %s"
    #     tuples = [tuple([1, 2, 3]), tuple([2, 4, 6])]

    #     mock_con = mock_connect.return_value
    #     mock_cur = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
    #     mock_cur.fetchall.return_value = 1  # return this when calling cur.fetchall()

    #     sql_helper_object.insert_batch(query, tuples=tuples)

    #     # assert


    @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective.database.com",
                                "DB_USER": "user",
                                "DB_PASSWORD": "passwd",
                                "DB_NAME": "name",
                                "DB_PORT": "10"}, clear=True)
    # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    @mock.patch("pandas.DataFrame.to_sql")
    @mock.patch("geopandas.GeoDataFrame.to_postgis")
    def test_insert_from_dataframe(self, mock_to_postgis, mock_to_sql, sql_helper_object):
        """ test select
        """
        schema_name = "tst"
        table_name = "test"
        df_data = pd.DataFrame({"name": "df name",
                                    'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
                                    'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
        df_data['Coordinates'] = list(zip(df_data.Longitude, df_data.Latitude))
        df_data['Coordinates'] = df_data['Coordinates'].apply(Point)
        gdf_data = gpd.GeoDataFrame(df_data, geometry="Coordinates")

        sql_helper_object.insert_from_dataframe(schema_name, table_name, df_data)

        with pytest.raises(BaseException) as error:
            sql_helper_object.insert_from_dataframe(
                        schema_name, table_name, df_data, is_geodataframe=True)
        assert "Unknown column geom" in str(error.value)


        sql_helper_object.insert_from_dataframe(
                        schema_name, table_name, gdf_data, is_geodataframe=True,
                        geometry_column="Coordinates")


    @mock.patch.dict(os.environ, {"DB_HOSTNAME": "prospective"}, clear=True)
    # why need clear=True explained here https://stackoverflow.com/a/67477901/248616
    @mock.patch("psycopg2.connect")
    def test_create(self, mock_connect, sql_helper_object):
        """ test create
        """
        schema_name = "schema_test"
        table_name  = "table_test"
        columns = ["id", "name", "description"]

        sql_helper_object.create(schema_name, table_name, columns)


    def test_format_query(self, sql_helper_object):
        """ test format query
        """
        query = "select * from {schema}.my_table"

        query_formatted = sql_helper_object.format_query(query)

        assert isinstance(query_formatted, SQL)
        assert "db_schema" in str(query_formatted)

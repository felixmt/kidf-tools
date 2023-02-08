"""modules imports
"""
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from psycopg2.sql import SQL
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import geopandas as gpd
import yaml
from yaml.loader import SafeLoader
from tools.log_helper import log_helper
from tools.decorators.deprecations import deprecated_param

class sql_helper:
    """various tools to interact with databases
    """
    def __init__(self, db_env: str = ""):
        load_dotenv()
        self.db_env = db_env
        self.db_schema=os.getenv('DB_SCHEMA')
        self.db_schema_gps_data=os.getenv('DB_SCHEMA_GPS_DATA')
        self.db_schema_sig=os.getenv('DB_SCHEMA_SIG')
        self.db_schema_insee=os.getenv('DB_SCHEMA_INSEE')
        self.db_schema_operator=os.getenv('DB_SCHEMA_OPERATOR')
        self.db_schema_administrative_zone=os.getenv('DB_SCHEMA_ADMINISTRATIVE_ZONE')
        self.db_schema_calendar=os.getenv('DB_SCHEMA_CALENDAR')
        self.db_schema_gtfs=os.getenv('DB_SCHEMA_GTFS')
        self.db_schema_idfm=os.getenv('DB_SCHEMA_IDFM')
        self.db_schema_keoreport=os.getenv('DB_SCHEMA_KEOREPORT')
        self.log_manager = log_helper()

    def get_connection(self, connection_type: str = "psycopg2"):
        """initialize connection
        @returns: connection
        """
        # get database connection infos
        try:
            db_prefix = "DB" + ("_" if self.db_env != "" else "") + self.db_env
            if os.getenv(db_prefix + "_HOSTNAME") is None:
                with open('.env.yml') as f:
                    env = yaml.load(f, Loader=SafeLoader)
                    database = env['databases'][self.db_env]
            else:
                database = {}
                database['user'] = os.getenv(db_prefix + "_USER")
                database['password'] = os.getenv(db_prefix + "_PASSWORD")
                database['host'] = os.getenv(db_prefix + "_HOSTNAME")
                database['port'] = os.getenv(db_prefix + "_PORT")
                database['name'] = os.getenv(db_prefix + "_NAME")
        except BaseException as error:
            self.log_manager.set_error(
                        "Connection error (postgreSQL) : could not read connection information. " \
                        + str(error))
            raise ConnectionError(str(
                        "Connection error (postgreSQL) : could not read connection information."))\
                        from None

        # instantiate connection
        try:
            if connection_type == "alchemy":
                db_uri: str = "postgresql+psycopg2://"
                db_uri = db_uri + \
                            str(database['user']) + ":" + \
                            str(database['password']) + "@" + \
                            str(database['host']) + ":" + \
                            str(database['port']) + "/" + \
                            str(database['name'])
                return create_engine(db_uri, echo=True)

            connection = psycopg2.connect(user=database['user'],
                                        password=database['password'],
                                        host=database['host'],
                                        port=database['port'],
                                        database=database['name']
                                        # , connect_timeout=1
                                        )

            return connection
        except psycopg2.Error as error:
            self.log_manager.set_error("psycopg2 : Connection error (PostgreSQL) : " \
                        + str(error))
            raise ConnectionError(
                        str("psycopg2 : Connection to the database could not be established"))\
                            from None
        except BaseException as error:
            self.log_manager.set_error("Connection error (PostgreSQL) : " \
                        + str(error))
            raise ConnectionError(str("Connection to the database could not be established"))\
                        from None


    @deprecated_param(version="0.0.4",
                  reason="auto detection of params type",
                  deprecated_args="params_as_array",
                  deprecated_args_positions="3")
    def select(self, query: str, params: list|dict, params_as_array: bool = True
                , return_sql_as_text: bool = False):
        """select into array
        @returns: list
        """
        connection = self.get_connection()

        if isinstance(params, list):
            params = tuple(params)

        cursor = connection.cursor()
        query_formatted = self.format_query(query)

        try:
            cursor.execute(query_formatted, params)

            if not return_sql_as_text:
                records = cursor.fetchall()
                return records
            else:
                query_as_sql = str(cursor.query).replace('"b\"', "").replace("\\n", "\n")\
                            .replace("\t", "").replace('b"', "")\
                            .replace("b'\n", "").replace("\\'", "'")

                if query_as_sql[len(query_as_sql) - 1] in ("'", '"'):
                    query_as_sql = query_as_sql[0:len(query_as_sql) - 1]
                return query_as_sql
        except psycopg2.Error as error:
            self.log_manager.set_error("Select error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(str(query_formatted))
            self.log_manager.set_error(" ".join(str(item) for item in params))
            raise BaseException("Select error (PostgreSQL) : " + str(error)) from None
        finally:
            # closing database connection.
            if connection:
                if cursor:
                    cursor.close()
                connection.close()


    def select_into_dataframe(self, query: str, params: dict, is_geodataframe = False):
        """select into pandas dataframe
        @returns: dataframe
        """
        connection = self.get_connection("alchemy")
        query_formatted = self.format_query(query, False)
        try:
            if is_geodataframe:
                return gpd.read_postgis(query_formatted, con=connection, params=params
                            , geom_col="geom", crs="4326")
            return pd.read_sql_query(query_formatted, con=connection, params=params)
        except psycopg2.Error as error:
            self.log_manager.set_error("Select into dataframe error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(str(query_formatted))
            self.log_manager.set_error(" ".join(str(item) for item in params))
            raise BaseException("select into dataframe error (PostgreSQL) : " +\
                        str(error)) from None
        # finally:
        #     # closing database connection.
        #     if connection:
        #         connection.close()


    def insert(self, query: str, params_list: list = None, sequence: str = None
                , params_dict: dict = None
    ):
        """insert, update, crate, alter queries (writing queries)
        @returns: int | None
        """
        connection = self.get_connection()

        if params_list is None and params_dict is None:
            self.log_manager.set_error("Insert error (PostgreSQL) : params have to be passed \
                        to insert function")
            raise ValueError("Database request error (insert) : params have to be passed \
                        to insert function") from None

        params = params_dict
        if params is None:
            params = tuple(params_list)

        query_formatted = self.format_query(query)
        try:
            cursor = connection.cursor()

            # print(query)
            # print(params)
            cursor.execute(query_formatted, params)

            sequence_id: int = 0
            if sequence is not None:
                schema="{schema}"
                query_formatted = self.format_query(f"SELECT currval('{schema}.{sequence}');")
                cursor.execute(query_formatted)
                result = cursor.fetchone()
                sequence_id = result[0] if isinstance(result, tuple) else 0

            connection.commit()

            return sequence_id
        except psycopg2.Error as error:
            self.log_manager.set_error("Insert error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(str(query_formatted))
            if params_dict is not None:
                self.log_manager.set_error(str(params_dict))
            else:
                self.log_manager.set_error(" ".join(str(item) for item in params_list))
            raise BaseException("Insert error (PostgreSQL) : " + str(error)) from None
        except BaseException as error:
            self.log_manager.set_error("Insert error base exception (PostgreSQL) : " + str(error))
            self.log_manager.set_error(str(query_formatted))
            if params_dict is not None:
                self.log_manager.set_error(str(params_dict))
            else:
                self.log_manager.set_error(" ".join(str(item) for item in params_list))
            raise BaseException(
                "Insert error base exception (PostgreSQL) : " + str(error)
            ) from None
        finally:
            # closing database connection.
            if connection is not None:
                if cursor:
                    cursor.close()
                connection.close()

    def insert_batch(self, query: str, tuples: list):
        """insert a batch of data
        @returns: void
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            execute_values(cursor, query, tuples)

            connection.commit()

        except psycopg2.Error as error:
            self.log_manager.set_error("Insert batch psycopg2 error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(query)
            # self.log_manager.set_error(str(tuples))
            raise BaseException("Insert batch psycopg2 error (PostgreSQL) : " \
                        + str(error)) from None
        except BaseException as error:
            self.log_manager.set_error("Insert batch other error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(query)
            raise BaseException("Insert batch other error (PostgreSQL) : " + str(error)) from None
        finally:
            # closing database connection.
            if connection:
                if cursor:
                    cursor.close()
                connection.close()

    def insert_from_dataframe(self, schema_name: str, table_name: str,
                df_data, is_geodataframe = False, geometry_column: str = "geom",
                crs: str = "4326", if_exists="replace", chunk_size=10000):
        """select into pandas dataframe
        @returns: None
        """
        connection = self.get_connection("alchemy")
        try:
            if is_geodataframe:
                df_data.set_geometry(geometry_column)
                df_data.set_crs(epsg=crs)
                df_data.to_postgis(table_name, connection, schema=schema_name, if_exists=if_exists,\
                            index=False, chunksize=chunk_size, method="multi")
            else:
                df_data.to_sql(table_name, connection, schema=schema_name, if_exists=if_exists,\
                            index=False, chunksize=chunk_size, method="multi")
        except psycopg2.Error as error:
            self.log_manager.set_error("Insert from dataframe error (PostgreSQL) : " + str(error))
            raise BaseException("Insert from dataframe error (PostgreSQL) : " +\
                        str(error)) from None
        # finally:
        #     # closing database connection.
        #     if connection:
        #         connection.close()
    
    def create(self, schema_name: str, table_name: str, columns: list):
        """create table
        @returns: void
        """
        connection = self.get_connection()
        query = f"create table if not exists {schema_name}.{table_name} ("
        for idx, column in enumerate(columns):
            if column not in ("", " "):
                if idx > 0 :
                    query = query + ","
                query = query + column + " varchar null"
        query = query + ");"

        query = query + f"GRANT SELECT ON TABLE {schema_name}.{table_name} TO marketing_analysts;"

        try:
            query = self.format_query(query)
        except BaseException as error:
            raise ValueError("Sql helper format_query function error : " + str(error)) from None
        try:
            cursor = connection.cursor()

            cursor.execute(query)

            connection.commit()

        except psycopg2.Error as error:
            self.log_manager.set_error("Create table error (PostgreSQL) : " + str(error))
            self.log_manager.set_error(str(query))
            self.log_manager.set_error(schema_name + "." + table_name)
            self.log_manager.set_error(" ".join(str(item) for item in columns))
            raise BaseException("Create table error (PostgreSQL) : " + str(error)) from None

        finally:
            # closing database connection.
            if connection:
                if cursor:
                    cursor.close()
                connection.close()

    def format_query(self, query: str, convert_to_sql: bool = True):
        query = query.format(
                    schema=self.db_schema, schema_gps_data=self.db_schema_gps_data,
                    schema_insee=self.db_schema_insee, schema_sig=self.db_schema_sig,
                    schema_administrative_zone=self.db_schema_administrative_zone,
                    schema_operator=self.db_schema_operator,
                    schema_idfm=self.db_schema_idfm,
                    schema_gtfs=self.db_schema_gtfs,
                    schema_keoreport=self.db_schema_keoreport,
                    schema_calendar=self.db_schema_calendar)
        if convert_to_sql is True:
            return SQL(query)

        return query

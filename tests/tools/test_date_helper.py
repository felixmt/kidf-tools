# python3 -m pytest -k TestSqlHelper -q tests/tools/test_sql_helper.py
"""modules imports
"""
import os
from unittest import mock
import pytest
from tools.date_helper import date_helper

class TestDateHelper:
    @pytest.fixture
    def date_helper_object():
        """instantiate object as a fixture
        """
        return date_helper()

    @pytest.fixture
    def example_date():
        """ instantiate date as a fixture
        """
        return datetime.date(2022, 3, 7)


    def test_constructor():
        """test_constructor
        """
        instance = date_helper()
        assert isinstance(instance, date_helper)

    def test_first_dow_in_a_month(date_helper_object, example_date):
        """test_first_dow_in_a_month
        looking for the first monday (0) in the month of march 2022
        """
        date = date_helper_object.first_dow_in_a_month(2022, 3, 0)

        assert date == example_date
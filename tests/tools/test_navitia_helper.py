# python3 -m pytest -k TestNavitiaHelper -q tests/tools/test_navitia_helper.py
"""modules imports
"""
import os
from unittest import mock
import pytest
from tools.navitia_helper import navitia_helper

class TestNavitiaHelper:
    """ class to test navitia helper
    """
    ### fixtures ###
    @pytest.fixture
    @mock.patch.dict(os.environ, {"NAVITIA_URL": "https://navitia.io/"}, clear=True)
    def navitia_helper_object(self):
        """instantiate object as a fixture
        """
        return navitia_helper()
    ### end fixtures ###

    @mock.patch.dict(os.environ, {"NAVITIA_URL": "https://navitia.io/"}, clear=True)
    def test_constructor(self):
        """test_constructor
        """
        instance = navitia_helper()

        assert instance.url == os.environ['NAVITIA_URL']
        assert isinstance(instance, navitia_helper)


    @mock.patch("requests.get")
    def test_get_journey(self, mock_requests_get, navitia_helper_object):
        """ test read file to dataframe
        """
        expected = mock_requests_get.return_value
        result = navitia_helper_object.get_journey(
            2.39,
            48.10,
            2.42,
            49.10,
            "20221002T121212",
            ["orlyval"],
            True
        )

        assert result == expected.json()


    @mock.patch("requests.get")
    def test_get_isochron(self, mock_requests_get, navitia_helper_object):
        """ test read file to dataframe
        """
        expected = mock_requests_get.return_value
        result = navitia_helper_object.get_journey(
            2.39,
            48.10,
            2.42,
            49.10,
            "20221002T121212",
            ["orlyval"],
            True
        )

        assert result == expected.json()

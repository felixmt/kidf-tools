# python3 -m pytest -v --cov

"""modules imports
"""
import os
from unittest import mock
import pandas as pd
import pytest
from tools.file_helper import file_helper

class TestFileHelper:
    """ class to test file helper
    """
    ### fixtures ###
    @pytest.fixture
    @mock.patch.dict(os.environ, {"OUTPUT_FOLDER": "output_folder_test"}, clear=True)
    def file_helper_object(self):
        """instantiate object as a fixture
        """
        return file_helper()

    @pytest.fixture
    def example_output_folder(self):
        """ instantiate db env as a fixture
        """
        return "output_folder_test"

    @pytest.fixture
    def example_dataframe(self):
        """ dataframe example
        """
        return pd.DataFrame({"name": ["Jojo", "Nono", "Dudu"],
                                    "lastname": ["Anton", "Duton", "Jonton"]})
    ### end fixtures ###

    @mock.patch.dict(os.environ, {"OUTPUT_FOLDER": "output_folder_test"}, clear=True)
    def test_constructor(self, example_output_folder):
        """test_constructor
        """
        instance = file_helper()

        assert instance.output_folder == example_output_folder
        assert isinstance(instance, file_helper)


    @mock.patch("pandas.read_excel")
    @mock.patch("pandas.read_csv")
    def test_read_file_to_dataframe(self, mock_read_csv, mock_read_excel,
                                    example_dataframe, file_helper_object):
        """ test read file to dataframe
        """
        file_path = "./"
        file_extension = "csv"

        mock_read_csv.return_value = example_dataframe
        result = file_helper_object.read_file_to_dataframe(file_path, file_extension)
        pd.testing.assert_frame_equal(result, example_dataframe)

        mock_read_excel.return_value = example_dataframe
        result = file_helper_object.read_file_to_dataframe(file_path, "xlsx")
        pd.testing.assert_frame_equal(result, example_dataframe)

        with pytest.raises(BaseException) as error:
            result = file_helper_object.read_file_to_dataframe(file_path, "xlsax")
        assert "File extension error" in str(error.value)


    @mock.patch("pandas.DataFrame.to_csv")
    def test_write_dataframe_to_csv(self, mock_to_csv, example_dataframe,
                                    example_output_folder, file_helper_object):
        """ test select
        """
        # expected = mock_to_csv.return_value
        result = file_helper_object.write_dataframe_to_csv(example_dataframe)
        assert example_output_folder in result


    @mock.patch("builtins.open")
    def test_write_csv(self, mock_file_open, file_helper_object):
        """ test select
        """
        expected = mock_file_open.return_value.__enter__.return_value
        result = file_helper_object.write_csv("test", [])
        assert result == expected


    @mock.patch("builtins.open")
    def test_write_file(self, mock_file_open, file_helper_object):
        """ test select
        """
        expected = mock_file_open.return_value.__enter__.return_value
        result = file_helper_object.write_file("file test", "txt")
        assert result == expected


    @mock.patch("openpyxl.Workbook")
    def test_write_xlsx(self, mock_openpyxl, example_output_folder, file_helper_object):
        """ test select
        """
        result = file_helper_object.write_xlsx(
                    ["sheet1"], [["name"]], [[["toto"], ["dudu"], ["juju"]]])
        assert example_output_folder in result

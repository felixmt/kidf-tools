""" modules imports
"""
import os
from dotenv import load_dotenv
import requests
from tools.log_helper import log_helper

class navitia_helper:
    """ Service to deal with Navitia API
    """
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('NAVITIA_URL')
        # self.token=os.getenv('NAVITIA_TOKEN')s
        self.log_manager = log_helper()

    def get_journey(
            self,
            longitude_start: float,
            latitude_start: float,
            longitude_end: float,
            latitude_end: float,
            request_datetime: str,
            forbidden_uris: list,
            force_walking: bool = False):
        """get navitia journey
        @returns: json \
        """

        headers = {
            "content-type": "application/json; charset=UTF-8",
            # 'Authorization': 'Basic {}'.format(base64.b64encode(self.token))
        }

        params = {
            'from': str(longitude_start) + ';' + str(latitude_start),
            'to': str(longitude_end) + ';' + str(latitude_end),
            'max_duration': 14400,
            # add forbidden uris
            'forbidden_uris[]': forbidden_uris
        }

        if force_walking:
            params['direct_path'] = "only"
            params['direct_path_mode[]'] = "walking"

        if request_datetime is not None:
            request_datetime = str(request_datetime).replace(
                " ", "T").replace(
                ":", "").replace(
                "-", "")
            params['datetime'] = request_datetime

        try:
            response = requests.get(
                self.url + 'journeys',
                params=params,
                headers=headers,
                timeout=10) # 10 secs
            raw_data = response.json()
            # print(response.url)

            return raw_data
        except requests.exceptions.RequestException as error:
            self.log_manager.set_error("Journey error : " + str(error))
            self.log_manager.set_error("from : " + str(longitude_start) +\
                        ";" + str(latitude_start) +\
                        " to : " + str(longitude_end) + ";" + str(latitude_end) +\
                        " datetime : " + request_datetime)
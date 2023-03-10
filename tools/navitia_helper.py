""" modules imports
"""
import os
from dotenv import load_dotenv
import requests
import yaml
from yaml.loader import SafeLoader
from tools.log_helper import log_helper

class navitia_helper:
    """ Service to deal with Navitia API
    """
    def __init__(self):
        load_dotenv()
        self.log_manager = log_helper()
        if os.getenv("NAVITIA_URL") is None:
            try:
                with open(".env.yml", encoding="utf-8") as file:
                    env = yaml.load(file, Loader=SafeLoader)
                    self.url = env["navitia"]["url"]
            except BaseException as error:
                self.log_manager.set_error("Environment file not found : " \
                            + str(error))
                raise ConnectionError("Environment file not found : " + str(error))\
                            from None
        else:
            self.url = os.getenv('NAVITIA_URL')
        # self.token=os.getenv('NAVITIA_TOKEN')s

    def get_journey(
            self,
            longitude_start: float,
            latitude_start: float,
            longitude_end: float,
            latitude_end: float,
            request_datetime: str = "",
            forbidden_uris: list[str] = [""],
            force_walking: bool = False,
            force_car: bool = False,
            stop_end: str = ""):
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

        if stop_end is not None and stop_end != "":
            params['to'] = stop_end

        if force_walking:
            params['direct_path'] = "only"
            params['direct_path_mode[]'] = "walking"
        elif force_car:
            params['direct_path'] = "only"
            params['direct_path_mode[]'] = "car_no_park"
            params['max_car_no_park_direct_path_duration'] = 100000

        if request_datetime != "":
            request_datetime = str(request_datetime).replace(
                " ", "T").replace(
                ":", "").replace(
                "-", "")
            params['datetime'] = request_datetime

        try:
            response = requests.get(
                str(self.url) + 'journeys',
                params=params,
                headers=headers,
                timeout=10) # 10 secs

            return response.json()
        except requests.exceptions.RequestException as error:
            self.log_manager.set_error("Journey error : " + str(error))
            self.log_manager.set_error("from : " + str(longitude_start) +\
                        ";" + str(latitude_start) +\
                        " to : " + str(longitude_end) + ";" + str(latitude_end) +\
                        " datetime : " + str(request_datetime))


    def get_isochron(
            self,
            longitude: float,
            latitude: float,
            min_duration: int,
            max_duration: int,
            request_datetime: str = ""):
        """get navitia isochron
        @returns: json \
        """
        headers = {
            "content-type": "application/json; charset=UTF-8",
            # 'Authorization': 'Basic {}'.format(base64.b64encode(self.token))
        }

        params = {
            'from': str(longitude) + ';' + str(latitude),
            'max_duration': max_duration,
            'min_duration': min_duration
        }

        if request_datetime is not None:
            request_datetime = str(request_datetime).replace(
                " ", "T").replace(
                ":", "").replace(
                "-", "")
            params['datetime'] = request_datetime

        try:
            response = requests.get(
                str(self.url) + 'isochrones',
                params=params,
                headers=headers,
                timeout=10)

            # /!\ G??rer les erreurs
            if response.status_code != 200:
                # print('Status:', response.status_code, 'Erreur de requ??te')
                self.log_manager.set_error("Navitia isochron request error : "
                                           + str(response.json()))
                # print(response['error']['message'])

            return response.json()
        except requests.exceptions.RequestException as error:
            self.log_manager.set_error("Isochron error : " + str(error))
            raise Exception ("Isochron error : " + str(error)) from None

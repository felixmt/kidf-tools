""" modules imports
"""
import os
from dotenv import load_dotenv
import requests
from tools.log_helper import log_helper

class open_route_helper:
    """ service to manage open route api calls
    """
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('OPEN_ROUTE_SERVICE_URL')
        self.token = os.getenv('OPEN_ROUTE_SERVICE_TOKEN')
        self.log_manager = log_helper()

    def get_isochron(
            self,
            longitude: float,
            latitude: float,
            max_duration: int,
            mode: int = 1):
        """get open route service isochron
        @returns: json \
        """
        params = {
            "locations": [[longitude, latitude]],
            "range": [max_duration]
        }
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml,\
                img/png; charset=utf-8',
            'Authorization': self.token,
            'Content-Type': 'application/json; charset=utf-8'
        }
        url = str(self.url)
        if mode == 1:
            url = url + 'foot-walking'
        elif mode == 3:
            url = url + 'driving-hgv'
        elif mode == 4:
            url = url + 'cycling-regular'
        elif mode == 5:
            url = url + 'cycling-electric'

        # if request_datetime != "":
        #     params['datetime'] = request_datetime

        try:
            response = requests.post(url, json=params, headers=headers, timeout=2)

            # /!\ Gérer les erreurs
            if response.status_code != 200:
                self.log_manager.set_error("Isochron error. Status:"\
                            + str(response.status_code) + " - erreur de requête")
                response = response.json()
                error_message = "Isochron error status " + str(response.status_code)\
                            + ". Open route service post request error : "
                # print(type(response))
                if "reason" in response:
                    error_message = error_message + str(response.reason)

                # print(404, response['error']['message'])
                self.log_manager.set_error(str(error_message))
                raise Exception(str(error_message)) from None

            return response.json()
        except requests.exceptions.RequestException as error:
            self.log_manager.set_error("Open route request error : " + str(error))
            raise Exception("Open route request error : " + str(error)) from None

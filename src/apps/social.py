import os
import logging

import requests
from flask import make_response


def get_query_params(queryParam) -> str:
    if not queryParam:
        return ""
    return f"?{str(queryParam, 'utf-8')}"


class Social:
    def __init__(self):
        self.host = os.getenv("SOCIAL_HOST")

    def getResponseJson(self, response):
        if response.status_code == 503 or not response.text:
            return {"message": "social service is currently unavailable,"
                    " please try again later", "status": 503}
        return response.json()

    def get(self, url, body, headers, query_params):
        url = f"{self.host}{url}{get_query_params(query_params)}"
        logging.info(f"SOCIAL | GET | {url}")
        response = requests.get(url, json=body, headers=headers)
        return make_response(self.getResponseJson(response),
                             response.status_code)

    def post(self, url, body, headers, query_params):
        response = requests.post(f"{self.host}{url}"
                                 f"{get_query_params(query_params)}",
                                 json=body,
                                 headers=headers)
        logging.info(f"SOCIAL | POST | {url}")
        logging.debug(f"BODY: {body}")
        return make_response(self.getResponseJson(response),
                             response.status_code)

    def patch(self, url, body, headers, query_params):
        response = requests.patch(f"{self.host}{url}"
                                  f"{get_query_params(query_params)}",
                                  json=body,
                                  headers=headers)
        logging.info(f"SOCIAL | PATCH | {url}")
        logging.debug(f"BODY: {body}")
        return make_response(self.getResponseJson(response),
                             response.status_code)

    def delete(self, url, body, headers, query_params):
        response = requests.delete(f"{self.host}{url}"
                                   f"{get_query_params(query_params)}",
                                   headers=headers)
        logging.info(f"SOCIAL | DELETE | {url}")
        return make_response(self.getResponseJson(response),
                             response.status_code)

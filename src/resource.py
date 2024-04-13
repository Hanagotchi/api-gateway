import logging
from flask import request, make_response  # type: ignore
from flask_restful import Resource

from src.apps.users import Users
from src.apps.measurements import Measurements
from src.apps.plants import Plants


def getExtraData():
    if request.is_json:
        body = request.json
    else:
        body = {}
    print(f"en get extract data headers: {request.headers}")
    headers = dict(request.headers)
    if 'Host' in headers:
        headers.pop('Host')  # Invalid header
    query_params = request.query_string
    return body, headers, query_params


SERVICE_MAP = {
    "users": Users(),
    "measurements": Measurements(),
    "device-plant": Measurements(),
    "plants": Plants(),
    "plant-type": Plants(),
    "logs": Plants(),
    "login": Users(),
    # TODO: Add the new service
    "socal": Measurements()
}


def getCorrectEndpoint(url: str):
    values = url.split("/")
    return SERVICE_MAP.get(values[0]) if len(values) else None


class Gateway(Resource):
    def get(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            logging.error(f"Resource not found for url {url}")
            return make_response({"message": "not found"}, 404)
        return resource.get(url, *getExtraData())

    def post(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            logging.error(f"Resource not found for url {url}")
            return make_response({"message": "not found"}, 404)
        return resource.post(url, *getExtraData())

    def patch(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            logging.error(f"Resource not found for url {url}")
            return make_response({"message": "not found"}, 404)
        return resource.patch(url, *getExtraData())

    def delete(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            logging.error(f"Resource not found for url {url}")
            return make_response({"message": "not found"}, 404)
        return resource.delete(url, *getExtraData())

    def put(self, url):
        resource = getCorrectEndpoint(url)
        if not resource:
            logging.error(f"Resource not found for url {url}")
            return make_response({"message": "not found"}, 404)
        return resource.put(url, *getExtraData())

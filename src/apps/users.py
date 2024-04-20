import http.client
import os
import logging
import jwt

import requests
from flask import make_response


TOKEN_FIELD_NAME = "x-access-token"


def get_query_params(queryParam) -> str:
    if not queryParam:
        return ""
    return f"?{str(queryParam, 'utf-8')}"


def _get_token(headers: dict):
    keyName = None
    for key in headers.keys():
        if key.lower() == TOKEN_FIELD_NAME:
            keyName = key
    if not keyName:
        return None
    return headers.get(keyName)


def process_header(headers):
    token = _get_token(headers)
    if not token:
        return {"message":
                "no token provided",
                "status": http.client.UNAUTHORIZED}
    try:
        jwt.decode(token, os.getenv("JWT_SECRET"),
                   algorithms=[os.getenv("HASH_ALGORITHM"), ])
    except jwt.ExpiredSignatureError:
        return {"message":
                "expired token",
                "status": http.client.UNAUTHORIZED}
    except jwt.InvalidTokenError:
        return {"message":
                "invalid token",
                "status": http.client.FORBIDDEN}
    return None


class Users:
    def __init__(self):
        self.host = os.getenv("USERS_HOST")

    def getResponseJson(self, response):
        if response.status_code == 503 or not response.text:
            return {"message": "users service is currently unavailable, please"
                    "try again later", "status": 503}
        return response.json()

    def get(self, url, body, headers, query_params):
        url = f"{self.host}{url}{get_query_params(query_params)}"
        token_error_response = process_header(headers)
        if token_error_response:
            return make_response(token_error_response,
                                 token_error_response.get("status"))
        response = requests.get(url, json=body, headers=headers)
        headers = dict(response.headers)
        logging.info(f"USERS | GET | {url}")
        response = make_response(self.getResponseJson(response),
                                 response.status_code)
        response.headers[TOKEN_FIELD_NAME] = headers.get(TOKEN_FIELD_NAME)
        return response

    def post(self, url, body, headers, query_params):
        if not (url.startswith("login")):
            token_error_response = process_header(headers)
            if token_error_response:
                return make_response(token_error_response,
                                     token_error_response.get("status"))
        response = requests.post(f"{self.host}{url}"
                                 f"{get_query_params(query_params)}",
                                 json=body,
                                 headers=headers)
        logging.info(f"USERS | POST | {url}")
        logging.debug(f"BODY: {body}")
        headers = dict(response.headers)
        response = make_response(self.getResponseJson(response),
                                 response.status_code)
        if headers.get(TOKEN_FIELD_NAME):
            response.headers[TOKEN_FIELD_NAME] = headers.get(TOKEN_FIELD_NAME)
        return response

    def patch(self, url, body, headers, query_params):
        url = f"{self.host}{url}{get_query_params(query_params)}"
        token_error_response = process_header(headers)
        if token_error_response:
            return make_response(token_error_response,
                                 token_error_response.get("status"))
        response = requests.patch(url, json=body, headers=headers)
        logging.info(f"USERS | PATCH | {url}")
        logging.debug(f"BODY: {body}")
        headers = dict(response.headers)
        response = make_response(self.getResponseJson(response),
                                 response.status_code)
        response.headers[TOKEN_FIELD_NAME] = headers.get(TOKEN_FIELD_NAME)
        return response

    def delete(self, url, body, headers, query_params):
        token_error_response = process_header(headers)
        if token_error_response:
            return make_response(token_error_response,
                                 token_error_response.get("status"))
        url = f"{self.host}{url}{get_query_params(query_params)}"
        response = requests.delete(url, headers=headers)
        logging.info(f"USERS | DELETE | {url}")
        headers = dict(response.headers)
        response = make_response(self.getResponseJson(response),
                                 response.status_code)
        response.headers[TOKEN_FIELD_NAME] = headers.get(TOKEN_FIELD_NAME)
        return response

from __future__ import absolute_import, unicode_literals, division

import hashlib
import hmac
import time

import requests

from quadriga.exceptions import RequestError


class RestClient(object):
    """REST client which handles HMAC SHA256 authentication.

    :param url: The QuadrigaCX URL.
    :type url: str | unicode
    :param api_key: The QuadrigaCX API key.
    :type api_key: str | unicode
    :param api_secret: The QuadrigaCX API secret.
    :type api_secret: str | unicode
    :param client_id: The QuadrigaCX client ID (the number used for login).
    :type client_id: int | str | unicode
    :param timeout: The number of seconds to wait for QuadrigaCX to respond.
    :type timeout: int | float
    :param session: The requests session object.
    :type session: requests.Session
    """

    _http_ok = {200, 201, 202}

    def __init__(self, url, api_key, api_secret, client_id, timeout, session):
        self._url = url
        self._api_key = str(api_key)
        self._hmac_key = str(api_secret).encode('utf-8')
        self._client_id = str(client_id)
        self._timeout = timeout
        self._session = session

    def _handle_response(self, response):
        """Handle the response from QuadrigaCX.

        :param response: The response from QuadrigaCX.
        :type response: requests.models.Response
        :return: The JSON response body.
        :rtype: dict
        :raise QuadrigaRequestError: If HTTP OK was not returned.
        """
        http_code = response.status_code
        if http_code not in self._http_ok:
            raise RequestError(
                response=response,
                message='[HTTP {}] {}'.format(
                    http_code, response.reason
                )
            )
        try:
            body = response.json()
        except ValueError:
            raise RequestError(
                response=response,
                message='[HTTP {}] response body: {}'.format(
                    http_code, response.text
                )
            )
        else:
            if 'error' in body:
                error_code = body['error'].get('code', '?')
                raise RequestError(
                    response=response,
                    message='[HTTP {}][ERR {}] {}'.format(
                        response.status_code,
                        error_code,
                        body['error'].get('message', 'no error message')
                    ),
                    error_code=error_code
                )
            return body

    def get(self, endpoint, params=None):
        """Send an HTTP GET request to QuadrigaCX.

        :param endpoint: The API endpoint.
        :type endpoint: str | unicode
        :param params: The request parameters.
        :type params: dict
        :return: The JSON response body from QuadrigaCX.
        :rtype: dict
        :raise QuadrigaRequestError: If HTTP OK was not returned.
        """
        response = self._session.get(
            url=self._url + endpoint,
            params=params,
            timeout=self._timeout
        )
        return self._handle_response(response)

    def post(self, endpoint, payload=None):
        """Send an HTTP POST request to QuadrigaCX.

        :param endpoint: The API endpoint.
        :type endpoint: str | unicode
        :param payload: The JSON request payload.
        :type payload: dict
        :return: The JSON response body from QuadrigaCX.
        :rtype: dict
        :raise QuadrigaRequestError: If HTTP OK was not returned.
        """
        nonce = int(time.time() * 10000)
        hmac_msg = str(nonce) + self._client_id + self._api_key
        signature = hmac.new(
            key=self._hmac_key,
            msg=hmac_msg.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if payload is None:
            payload = {}
        payload['key'] = self._api_key
        payload['nonce'] = nonce
        payload['signature'] = signature

        response = self._session.post(
            url=self._url + endpoint,
            json=payload,
            timeout=self._timeout
        )
        return self._handle_response(response)

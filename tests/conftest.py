from __future__ import absolute_import, unicode_literals, division

import time
import mock
import pytest

from quadriga import QuadrigaClient


test_vars = {
    'api_key': 'test_api_key',
    'api_secret': 'test_api_secret',
    'client_id': 'test_client_id',
    'nonce': 14914812560000,
    'timeout': 123456789,
    'sig': '6d39de3ac91dd6189993059be99068d2290d90207ab4aeca26dcbbccfef7b57d'
}


def pytest_namespace():

    def with_hmac(payload):
        payload.update({
            'key': test_vars['api_key'],
            'nonce': test_vars['nonce'],
            'signature': test_vars['sig']
        })
        return payload

    test_vars['with_hmac'] = with_hmac
    return test_vars


@pytest.fixture(autouse=True)
def patch_time(monkeypatch):
    mock_time = mock.MagicMock()
    mock_time.return_value = test_vars['nonce'] // 10000
    monkeypatch.setattr(time, 'time', mock_time)


@pytest.fixture(autouse=True)
def logger():
    logger = mock.MagicMock()

    def debug_called_with(message):
        logger.debug.assert_called_with(message)

    logger.debug_called_with = debug_called_with
    return logger


# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def response():
    response = mock.MagicMock()
    response.status_code = 200
    return response


# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def session(response):
    session = mock.MagicMock()
    session.get.return_value = response
    session.post.return_value = response

    def get_called_with(endpoint, params=None):
        session.get.assert_called_with(
            url=QuadrigaClient.url + endpoint,
            params=params,
            timeout=test_vars['timeout']
        )
    session.get_called_with = get_called_with

    def post_called_with(endpoint, payload=None):
        payload = payload or {}
        payload.update({
            'key': test_vars['api_key'],
            'nonce': test_vars['nonce'],
            'signature': test_vars['sig']
        })
        session.post.assert_called_with(
            url=QuadrigaClient.url + endpoint,
            json=payload,
            timeout=test_vars['timeout']
        )
    session.post_called_with = post_called_with
    return session

# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def client(session, logger):
    return QuadrigaClient(
        api_key=test_vars['api_key'],
        api_secret=test_vars['api_secret'],
        client_id=test_vars['client_id'],
        timeout=test_vars['timeout'],
        session=session,
        logger=logger
    )

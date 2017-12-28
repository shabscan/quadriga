from __future__ import absolute_import, unicode_literals, division

import json

import mock
import pytest

from quadriga.version import __version__


def test_client_version(client):
    assert client.version == __version__


def test_get_balance(client, session, logger):
    client.get_account_balance()
    session.post_called_with(endpoint='/balance')
    logger.debug_called_with("get account balance")


def test_get_ticker(client, session, logger):
    client.order_book('btc_cad').get_ticker()
    session.get_called_with(
        endpoint='/ticker',
        params={'book': 'btc_cad'}
    )
    logger.debug_called_with('btc_cad: get ticker')


def test_get_public_orders_grouped(client, session, logger):
    client.order_book('btc_cad').get_public_orders(group=True)
    session.get_called_with(
        endpoint='/order_book',
        params={'book': 'btc_cad', 'group': 1}
    )
    logger.debug_called_with('btc_cad: get public orders')


def test_get_public_orders_not_grouped(client, session, logger):
    client.order_book('btc_cad').get_public_orders(group=False)
    session.get_called_with(
        endpoint='/order_book',
        params={'book': 'btc_cad', 'group': 0}
    )
    logger.debug_called_with('btc_cad: get public orders')


def test_get_public_trades_by_hour(client, session, logger):
    client.order_book('btc_cad').get_public_trades()
    session.get_called_with(
        endpoint='/transactions',
        params={'book': 'btc_cad', 'time': 'hour'}
    )
    logger.debug_called_with('btc_cad: get public trades')


def test_get_public_trades_by_minute(client, session, logger):
    client.order_book('btc_cad').get_public_trades(time_frame='minute')
    session.get_called_with(
        endpoint='/transactions',
        params={'book': 'btc_cad', 'time': 'minute'}
    )
    logger.debug_called_with('btc_cad: get public trades')


def test_get_user_orders(client, session, logger):
    client.order_book('btc_cad').get_user_orders()
    session.post_called_with(
        endpoint='/open_orders',
        payload={'book': 'btc_cad'}
    )
    logger.debug_called_with('btc_cad: get user orders')


def test_get_user_trades_no_params(client, session, logger, response):
    response.json.return_value = []
    book = client.order_book('btc_cad')
    assert [] == book.get_user_trades()
    session.post_called_with(
        endpoint='/user_transactions',
        payload={
            'book': 'btc_cad',
            'limit': 0,
            'offset': 0,
            'sort': 'desc'
        }
    )
    logger.debug_called_with('btc_cad: get user trades')


def test_get_user_trades_with_params(client, session, logger, response):
    response.json.return_value = [1, 2]
    book = client.order_book('btc_cad')
    assert [1] == book.get_user_trades(limit=1, offset=1, sort='asc')
    session.post_called_with(
        endpoint='/user_transactions',
        payload={
            'book': 'btc_cad',
            'limit': 1,
            'offset': 1,
            'sort': 'asc'
        }
    )
    logger.debug_called_with('btc_cad: get user trades')


def test_buy_market_order(client, session, logger):
    book = client.order_book('btc_cad')
    book.buy_market_order(10)
    session.post_called_with(
        endpoint='/buy',
        payload={
            'book': 'btc_cad',
            'amount': 10
        }
    )
    logger.debug_called_with("buy 10 btc at market price cad")

    output = client.buy_market_order(20, 'eth_cad')
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/buy',
        json={
            'book': 'eth_cad',
            'amount': 20,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] buy 20 at market price for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.buy_market_order(1, 'invalid_book')


def test_buy_limit_order(requests_post, logger):
    client = mock_session()
    output = client.buy_limit_order(10, 5)
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/buy'),
        json={
            'book': test_order_book,
            'amount': 10,
            'price': 5,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] buy 10 at price of 5 for btc_usd")

    output = client.buy_limit_order(20, 1, 'eth_cad')
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/buy'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'price': 1,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] buy 20 at price of 1 for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.buy_limit_order(1, 10, 'invalid_book')


def test_sell_market_order(requests_post, logger):
    client = mock_session()
    output = client.sell_market_order(10)
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/sell'),
        json={
            'book': test_order_book,
            'amount': 10,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] sell 10 at market price for btc_usd")

    output = client.sell_market_order(20, 'eth_cad')
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/sell'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] sell 20 at market price for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.sell_market_order(10, 'invalid_book')


def test_sell_limit_order(requests_post, logger):
    client = mock_session()
    output = client.sell_limit_order(10, 5)
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/sell'),
        json={
            'book': test_order_book,
            'amount': 10,
            'price': 5,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] sell 10 at price of 5 for btc_usd")

    output = client.sell_limit_order(20, 1, 'eth_cad')
    assert output == test_response_body
    requests_post.assert_called_with(
        endpoint='/sell'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'price': 1,
            'key': test_api_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug_called_with(
        "[client: test_client_id] sell 20 at price of 1 for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.sell_limit_order(1, 10, 'invalid_book')



# def test_request_fail_1(monkeypatch):
#     mock_get = mock.MagicMock()
#     error_body = {'error': {'code': '123', 'message': 'failed'}}
#     set_response(mock_get, code=200, body=error_body)
#     monkeypatch.setattr(requests, 'get', mock_get)
#
#     client = mock_session()
#     with pytest.raises(RequestError) as error:
#         client.get_ticker()
#     assert error.value.url == quadriga_url
#     assert error.value.headers == test_request_headers
#     assert error.value.http_code == 200
#     assert error.value.error_code == '123'
#     assert str(error.value) == '[HTTP 200][ERR 123] failed'
#
#
# def test_request_fail_2(monkeypatch):
#     mock_get = mock.MagicMock()
#     set_response(mock_get, code=400)
#     monkeypatch.setattr(requests, 'get', mock_get)
#
#     client = mock_session()
#     with pytest.raises(RequestError) as error:
#         client.get_ticker()
#     assert error.value.url == quadriga_url
#     assert error.value.headers == test_request_headers
#     assert error.value.http_code == 400
#     assert error.value.error_code is None
#     assert str(error.value) == '[HTTP 400] {}'.format(test_response_reason)
#
#
# def test_request_fail_3(monkeypatch):
#     mock_get = mock.MagicMock()
#     mock_response = set_response(mock_get, code=200, body='foo')
#     mock_response.json.side_effect = ValueError
#     monkeypatch.setattr(requests, 'get', mock_get)
#
#     client = mock_session()
#     with pytest.raises(RequestError) as error:
#         client.get_ticker()
#     assert error.value.url == quadriga_url
#     assert error.value.headers == test_request_headers
#     assert error.value.http_code == 200
#     assert error.value.error_code is None
#     assert str(error.value) == '[HTTP 200] response body: foo'
#
#
#

#
#

#
# def test_lookup_order(requests_post, logger):
#     client = mock_session()
#     output = client.lookup_orders('foobar')
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/lookup_order'),
#         json={
#             'id': 'foobar',
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] look up order foobar")
#
#
# def test_cancel_order(requests_post, logger):
#     client = mock_session()
#     output = client.cancel_order('foobar')
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/cancel_order'),
#         json={
#             'id': 'foobar',
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] cancel order foobar")
#
#
# def test_get_deposit_address(requests_post, logger):
#     client = mock_session()
#     output = client.get_deposit_address('ether')
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/ether_deposit_address'),
#         json={
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] get deposit address for ether")
#
#     output = client.get_deposit_address('bitcoin')
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/bitcoin_deposit_address'),
#         json={
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] get deposit address for bitcoin")
#
#     output = client.get_deposit_address('litecoin')
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/litecoin_deposit_address'),
#         json={
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] get deposit address for litecoin")
#
#     with pytest.raises(InvalidCurrencyError):
#         client.get_deposit_address('invalid_currency')
#
#
# def test_withdraw(requests_post, logger):
#     client = mock_session()
#     output = client.withdraw('ether', 1000, test_deposit_address)
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/ether_withdrawal'),
#         json={
#             'address': test_deposit_address,
#             'amount': 1000,
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] withdraw 1000 ethers to test_address")
#
#     output = client.withdraw('bitcoin', 1000, test_deposit_address)
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/bitcoin_withdrawal'),
#         json={
#             'address': test_deposit_address,
#             'amount': 1000,
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] withdraw 1000 bitcoins to test_address")
#
#     output = client.withdraw('litecoin', 1000, test_deposit_address)
#     assert output == test_response_body
#     requests_post.assert_called_with(
#         endpoint='/litecoin_withdrawal'),
#         json={
#             'address': test_deposit_address,
#             'amount': 1000,
#             'key': test_api_key,
#             'nonce': test_nonce,
#             'signature': mock.ANY
#         }
#     )
#     logger.debug_called_with(
#         "[client: test_client_id] withdraw 1000 litecoins to test_address")
#
#     with pytest.raises(InvalidCurrencyError):
#         client.withdraw('invalid_currency', 1000, test_deposit_address)

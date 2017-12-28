from __future__ import absolute_import, unicode_literals, division

import logging

import requests

from quadriga.exceptions import (
    InvalidOrderBookError
)
from quadriga.order_book import OrderBook
from quadriga.rest_client import RestClient
from quadriga.version import __version__


class QuadrigaClient(object):
    """Python client for QuadrigaCX `REST API v2`_.

    :param api_key: The QuadrigaCX API key.
    :type api_key: str | unicode
    :param api_secret: The QuadrigaCX API secret.
    :type api_secret: str | unicode
    :param client_id: The QuadrigaCX client ID (the number used for login).
    :type client_id: int | str | unicode
    :param timeout: The number of seconds to wait for QuadrigaCX to respond.
    :type timeout: int | float
    :param session: Custom requests.Session object to send requests with. If
        not set, "requests.Session()" is used by default.
    :type session: requests.Session
    :param logger: Custom logger to log debug messages with. If not set,
        "logging.getLogger('quadriga')" is used by default.
    :type logger: logging.Logger

    .. note:

        Parameters **api_key**, **api_secret** and **client_id** are optional
        if only the public API is needed. See the documentation_ for details.

    .. _REST API v2: https://www.quadrigacx.com/api_info
    .. _documentation: https://quadriga.readthedocs.io/en/latest/public.html

    """

    version = __version__

    url = 'https://api.quadrigacx.com/v2'

    order_books = (
        'btc_cad',
        'btc_usd',
        'eth_cad',
        'eth_btc',
        'ltc_cad',
        'bch_cad',
        'btg_cad',
    )

    def __init__(self,
                 api_key=None,
                 api_secret=None,
                 client_id=None,
                 timeout=None,
                 session=None,
                 logger=None):
        self._rest_client = RestClient(
            url=self.url,
            api_key=api_key,
            api_secret=api_secret,
            client_id=client_id,
            timeout=timeout,
            session=session or requests.Session()
        )
        self._logger = logger or logging.getLogger('quadriga')

    def __repr__(self):
        return '<QuadrigaClient v{}>'.format(__version__)

    def _log(self, message):
        """Log a debug message.

        :param message: The message to log.
        :type message: str | unicode
        """
        self._logger.debug(message)

    def order_book(self, name):
        """Return the order book of the given name.

        :param name: The name of the order book.
        :param name: str | unicode
        :return: The order book.
        :rtype: quadriga.order_book.OrderBook
        """
        if name not in self.order_books:
            raise InvalidOrderBookError(
                'Invalid order book \'{}\'. Choose from {}.'
                .format(name, self.order_books)
            )
        return OrderBook(name, self._rest_client, self._logger)

    def get_account_balance(self):
        """Return the user's account balance.

        :return: The user's account balance.
        :rtype: dict
        """
        self._log("get account balance")
        return self._rest_client.post(endpoint='/balance')

    def lookup_orders(self, order_ids):
        """Look up one or more orders by their IDs.

        :param order_ids: List of order IDs (64 hexadecmial characters each).
        :type order_ids: [str | unicode]
        :return: The order details.
        :rtype: [dict]
        """
        self._log('look up order(s) {}'.format(order_ids))
        return self._rest_client.post(
            endpoint='/lookup_order',
            payload={'id': order_ids}
        )

    def cancel_order(self, order_id):
        """Cancel an open order by its ID.

        :param order_id: The order ID (64 hexadecmial characters).
        :type order_id: str | unicode
        :return: True if the order has been cancelled.
        :rtype: bool
        """
        self._log('cancel order {}'.format(order_id))
        return self._rest_client.post(
            endpoint='/cancel_order',
            payload={'id': order_id}
        )

    def get_bitcoin_deposit_address(self):
        """Return the user's bitcoin deposit address on QuadrigaCX.

        :return: The user's bitcoin deposit address.
        :rtype: str | unicode
        """
        self._log('get bitcoin deposit address')
        return self._rest_client.post(endpoint='/bitcoin_deposit_address')

    def get_ether_deposit_address(self):
        """Return the user's ethereum deposit address on QuadrigaCX.

        :return: The user's bitcoin deposit address.
        :rtype: str | unicode
        """
        self._log('get ether deposit address')
        return self._rest_client.post(endpoint='/ether_deposit_address')

    def get_litecoin_deposit_address(self):
        """Return the user's litecoin deposit address on QuadrigaCX.

        :return: The user's litecoin deposit address.
        :rtype: str | unicode
        """
        self._log('get litecoin deposit address')
        return self._rest_client.post(endpoint='/litecoin_deposit_address')

    def withdraw_bitcoin(self, amount, address):
        """Withdraw bitcoin from QuadrigaCX to the given wallet address.

        :param amount: The withdrawal amount.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param address: The bitcoin wallet address.
        :type address: str | unicode

        .. warning:
            Specifying incorrect wallet address may result in permanent loss
            of coins. Be careful!
        """
        self._log('withdraw {} bitcoins to {}'.format(amount, address))
        return self._rest_client.post(
            endpoint='/bitcoin_withdrawal',
            payload={'address': address, 'amount': amount}
        )

    def withdraw_ether(self, amount, address):
        """Withdraw ether from QuadrigaCX to the given wallet address.

        :param amount: The withdrawal amount.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param address: The ethereum wallet address.
        :type address: str | unicode

        .. warning:
            Specifying incorrect wallet address may result in permanent loss
            of coins. Be careful!
        """
        self._log('withdraw {} ethers to {}'.format(amount, address))
        return self._rest_client.post(
            endpoint='/ether_withdrawal',
            payload={'address': address, 'amount': amount}
        )

    def withdraw_litecoin(self, amount, address):
        """Withdraw litecoin from QuadrigaCX to given wallet address.

        :param amount: The withdrawal amount.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param address: The litecoin wallet address.
        :type address: int | float | str | unicode | decimal.Decimal

        .. warning:
            Specifying incorrect wallet address may result in permanent loss
            of coins. Be careful!
        """
        self._log('withdraw {} litecoins to {}'.format(amount, address))
        return self._rest_client.post(
            endpoint='/litecoin_withdrawal',
            payload={'address': address, 'amount': amount}
        )

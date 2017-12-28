from __future__ import absolute_import, unicode_literals, division


class OrderBook(object):
    """Represents an order book on QuadrigaCX."""

    def __init__(self, name, rest_client, logger):
        self._name = name
        self._major, self._minor = name.split('_')
        self._rest_client = rest_client
        self._logger = logger

    def __repr__(self):
        return '<OrderBook {}>'.format(self._name.upper())

    def _log(self, message):
        """Log a debug message.

        :param message: The message to log.
        :type message: str | unicode
        """
        self._logger.debug("{}: {}".format(self._name, message))

    @property
    def name(self):
        """Return the name of the order book.

        :return: The name of the order book.
        :rtype: str | unicode
        """
        return self._name

    def get_ticker(self):
        """Return the latest ticker information.

        :return: The latest ticker information.
        :rtype: dict
        """
        self._log('get ticker')
        return self._rest_client.get(
            endpoint='/ticker',
            params={'book': self._name}
        )

    def get_public_orders(self, group=False):
        """Return all public orders that are currently open.

        :param group: If set to True (default: False), orders with the same
            price are grouped together.
        :type group: bool
        :return: All public orders that are currently open.
        :rtype: dict
        """
        self._log('get public orders')
        return self._rest_client.get(
            endpoint='/order_book',
            params={'book': self._name, 'group': int(group)}
        )

    def get_public_trades(self, time_frame='hour'):
        """Return all public trades (transactions) completed recently.

        :param time_frame: The time frame. Allowed values are "minute" for the
            trades in the last minute, or "hour" for those in the last hour
            (default: "hour").
        :type time_frame: str | unicode
        :return: All public trades that were completed recently.
        :rtype: [dict]
        """
        self._log('get public trades')
        return self._rest_client.get(
            endpoint='/transactions',
            params={'book': self._name, 'time': time_frame}
        )

    def get_user_orders(self):
        """Return the list of user's orders that are currently open.

        :return: The list of user's open orders.
        :rtype: [dict]
        """
        self._log('get user orders')
        return self._rest_client.post(
            endpoint='/open_orders',
            payload={'book': self._name}
        )

    def get_user_trades(self, limit=0, offset=0, sort='desc'):
        """Return the user's trade (transaction) history.

        :param limit: The maximum number of trades to return. If set to 0 or
            lower, all trades are returned (default: 0).
        :type limit: int
        :param offset: The number of trades to skip.
        :type offset: int
        :param sort: The method to sort the result by date and time. Allowed
            values are "desc" for descending order and "asc" for ascending
            order (default: "desc").
        :type sort: str | unicode
        :return: The user's trade history.
        :rtype: [dict]
        """
        self._log('get user trades')
        res = self._rest_client.post(
            endpoint='/user_transactions',
            payload={
                'book': self._name,
                'limit': limit,
                'offset': offset,
                'sort': sort
            }
        )
        # TODO Workaround for the broken limit param in QuadrigaCX API
        return res[:limit] if len(res) > limit > 0 else res

    def buy_market_order(self, amount):
        """Place a buy order at market price in the order book.

        :param amount: The amount of major currency to buy at market price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :return: The total amount of major currency purchased and a set of
            amount/price pairs, one for each order matched in the trade.
        :rtype: dict
        """
        amount = str(amount)
        self._log("buy {} at market price".format(amount))
        return self._rest_client.post(
            endpoint='/buy',
            payload={'book': self._name, 'amount': amount}
        )

    def buy_limit_order(self, amount, price):
        """Place a buy order at the given limit price in the order book.

        :param amount: The amount of major currency to buy at the limit price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param price: The limit price to buy at.
        :type price: int | float | str | unicode | decimal.Decimal
        :return: The details of the order placed.
        :rtype: dict
        """
        amount = str(amount)
        self._log("buy {} at limit price {}".format(amount, price))
        return self._rest_client.post(
            endpoint='/buy',
            payload={'book': self._name, 'amount': amount, 'price': price}
        )

    def sell_market_order(self, amount):
        """Place a sell order at market price in the order book.

        :param amount: The amount of major currency to sell at market price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :return: The total amount of minor currency acquired in sale and a set
            of amount/price pairs, one for each order matched in the trade.
        :rtype: dict
        """
        amount = str(amount)
        self._log("sell {} at market price".format(amount))
        return self._rest_client.post(
            endpoint='/sell',
            payload={'book': self._name, 'amount': amount}
        )

    def sell_limit_order(self, amount, price):
        """Place a sell order at the given limit price in the order book.

        :param amount: The amount of major currency to sell at the limit price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param price: The limit price to sell at.
        :type price: int | float | str | unicode | decimal.Decimal
        :return: The details of the order placed.
        :rtype: dict
        """
        amount = str(amount)
        self._log("sell {} {} at price of {} {}".format(
            amount, self._major, price, self._minor
        ))
        return self._rest_client.post(
            endpoint='/sell',
            payload={'book': self._name, 'amount': amount, 'price': price}
        )

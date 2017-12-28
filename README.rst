Python Client for QuadrigaCX
----------------------------

.. image:: https://travis-ci.org/joowani/quadriga.svg?branch=master
    :target: https://travis-ci.org/joowani/quadriga

.. image:: https://badge.fury.io/py/quadriga.svg
    :target: https://badge.fury.io/py/quadriga
    :alt: Package version

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://github.com/joowani/quadriga
    :alt: Python Versions

.. image:: https://coveralls.io/repos/github/joowani/quadriga/badge.svg?branch=master
    :target: https://coveralls.io/github/joowani/quadriga?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/github/issues/joowani/quadriga.svg
    :target: https://github.com/joowani/quadriga/issues
    :alt: Issues Open

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/joowani/quadriga/master/LICENSE
    :alt: MIT License

|

Introduction
============

**Quadriga** is an unofficial Python client for Canadian cryptocurrency
exchange platform QuadrigaCX_. It wraps `REST API v2`_ using the `requests`_
library.

.. _QuadrigaCX: https://www.quadrigacx.com
.. _REST API v2: https://www.quadrigacx.com/api_info
.. _requests: https://github.com/requests/requests

Requirements
============

- Python 2.7, 3.4, 3.5 or 3.6
- Pip_ installer
- QuadrigaCX API secret, API key and client ID

.. _Pip: https://pip.pypa.io/

Installation
============

To install a stable version from PyPi_:

.. code-block:: bash

    ~$ pip install quadriga

To install the latest version directly from GitHub_:

.. code-block:: bash

    ~$ pip install -e git+git@github.com:joowani/quadriga.git@master#egg=quadriga

You may need to use ``sudo`` depending on your environment.

.. _PyPi: https://pypi.python.org/pypi/quadriga
.. _GitHub: https://github.com/joowani/quadriga


Getting Started
===============

Here are some usage examples:

.. code-block:: python

    from quadriga import QuadrigaClient

    # Initialize the QuadrigaCX client
    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
        default_book='btc_usd'
    )

    # Get the latest trading summary
    client.get_ticker()

    # Get all public open orders
    client.get_public_orders()

    # Get recently completed public trades
    client.get_public_trades()

    # Get the user's open orders
    client.get_user_orders()

    # Get the user's completed trades
    client.get_user_trades()

    # Get the user's account balance
    client.get_account_balance()

    # Buy 10 bitcoins at the market price
    client.buy_market_order(10)

    # Buy 10 bitcoins at limit price of $1000 USD
    client.buy_limit_order(10, 1000)

    # Sell 20 bitcoins at the market price
    client.sell_market_order(20)

    # Sell 20 bitcoins at limit price of $1300 USD
    client.sell_limit_order(20, 1300)

    # Look up an order by its ID
    client.lookup_order('order_id')

    # Cancel an open order by its ID
    client.cancel_order('order_id')

    # Return the deposit address used for funding bitcoin
    client.get_deposit_address('bitcoin')

    # Return the deposit address used for funding ether
    client.get_deposit_address('ether')

    # Return the deposit address used for funding litecoin
    client.get_deposit_address('litecoin')

    # Withdraw 15 bitcoins from QuadrigaCX to the given address
    client.withdraw('bitcoin', 15, 'my_bitcoin_withdrawal_address')

    # Withdraw 20 ethers from QuadrigaCX to the given address
    client.withdraw('ether', 20, 'my_ether_withdrawal_address')

    # Withdraw 50 litecoins from QuadrigaCX to the given address
    client.withdraw('litecoin', 50, 'my_litecoin_withdrawal_address')

Check out the full `API documentation`_ for more details!

Contributing
============

Please have a look at this page_ before submitting a pull request. Thanks!

.. _API documentation:
    http://quadriga.readthedocs.io/en/master/index.html
.. _page:
    http://quadriga.readthedocs.io/en/master/contributing.html

Donation
========

If you found this library useful, feel free to donate!

* **BTC**: 3QG2wSQnXNbGv1y88oHgLXtTabJwxfF8mU
* **ETH**: 0x1f90a2a456420B38Bdb39086C17e61BF5C377dab
* **ADA**:


Disclaimer
==========

The author(s) of this project is in no way affiliated with QuadrigaCX, and
shall not accept any liability, obligation or responsibility whatsoever for
any cost, loss or damage arising from the use of this client. Please use at
your own risk!

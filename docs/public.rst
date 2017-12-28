Public API
==========

If you only need *public* API, **api_key**, **api_secret** and **client_id**
parameters are not required when initializing :class:`quadriga.QuadrigaClient`:

.. code-block:: python

    # Initialize the client without the credentials or the client ID
    client = QuadrigaClient(default_book='btc_usd')

    # Public API calls are allowed
    client.get_summary()
    client.get_public_orders()
    client.get_public_trades()

    # Private (user-specific) API calls fail:
    client.get_balance()
    client.get_orders()
    client.get_trades()

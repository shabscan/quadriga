from __future__ import absolute_import, unicode_literals


class QuadrigaError(Exception):
    """Base class for all **quadriga** exceptions."""


class RequestError(QuadrigaError):
    """Raised when a request to QuadrigaCX fails."""

    def __init__(self, response, message, error_code=None):
        self.url = response.url
        self.body = response.text
        self.headers = response.headers
        self.http_code = response.status_code
        self.error_code = error_code
        self.error_msg = message
        Exception.__init__(self, message)


class InvalidCurrencyError(QuadrigaError):
    """Raised when an invalid currency is given."""


class InvalidOrderBookError(QuadrigaError):
    """Raised when an invalid order book name is given."""


class InvalidTimeFrameError(QuadrigaError):
    """Raised when an invalid time frame is given."""


class InvalidSortMethodError(QuadrigaError):
    """Raised when an invalid sorting method is given."""

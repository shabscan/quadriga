Quadriga
--------

Welcome to the documentation for **quadriga**!

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

.. _Pip: https://pip.pypa.io

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


Contents
========

.. toctree::
    :maxdepth: 1

    overview
    api
    errors
    logging
    public
    contributing
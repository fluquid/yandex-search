=============
Yandex Search
=============

.. image:: https://img.shields.io/pypi/v/yandex-search.svg
        :target: https://pypi.python.org/pypi/yandex-search

.. image:: https://img.shields.io/travis/fluquid/yandex-search.svg
        :target: https://travis-ci.org/fluquid/yandex-search

.. image:: https://codecov.io/github/fluquid/yandex-search/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fluquid/yandex-search

.. image:: https://requires.io/github/fluquid/yandex-search/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fluquid/yandex-search/requirements/?branch=master

.. image:: http://fluquid.com:8000/api/badge/github.com/fluquid/yandex-search/status.svg?branch=master
    :alt: Build Status
    :target: http://fluquid.com:8000/github.com/fluquid/yandex-search

Search library for yandex.ru search engine.

Yandex allows **10,000 searches per day** when registered with a validated (international) mobile number.

Example
-------
::

    >>> yandex = yandex_search.Yandex(api_user='asdf', api_key='asdf')
    >>> yandex.search('"Interactive Saudi"').items
    [{
          "snippet": "Your Software Development Partner In  Saudi   Arabia . Since our early days in 2003, our main goal in  Interactive   Saudi   Arabia  has been: \"To earn customer respect and maintain long-term loyalty\".",
          "url": "http://www.interactive.sa/en",
          "title": "Interactive   Saudi   Arabia  Limited",
          "domain": "www.interactive.sa"
    }]

Getting Started
---------------
* register account: https://passport.yandex.ru/registration

  * use google translate addon (right-click "translate page")
    * provide an (international) mobile phone number to unlock 10k queries/day

* configure yandex: https://xml.yandex.ru/settings.xml

  * Navigate to "Settings"

    * switch language to english in bottom left (En/Ru)
    * enter email for "Email notifications"
    * set "Search type" to "Worldwide"
    * set "Main IP-address" to your querying machine
    * "I accept the terms of License Agreement"
    * Save

  * Navigate to "Test"

    * "? user = " is your credentials username
    * "& key = " is your crednetials key


Notes
-----
* Yandex highlights matching terms, leading to extra whitespace from `' '.join`

Alternatives
------------
* pyyaxml is py2-only and was giving me grief ;)

Documentation
-------------
search operators:

* https://yandex.com/support/search/how-to-search/search-operators.html

settings:

* https://xml.yandex.ru/settings.xml

docs:

* https://tech.yandex.ru/xml/doc/dg/concepts/restrictions-docpage/
* https://yandex.com/support/search/robots/search-api.html

==
Yandex Search
==

.. image:: https://img.shields.io/pypi/v/yandex-search.svg
        :target: https://pypi.python.org/pypi/yandex-search

.. image:: https://img.shields.io/travis/fluquid/yandex-search.svg
        :target: https://travis-ci.org/fluquid/yandex-search

.. image:: https://codecov.io/github/fluquid/yandex-search/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fluquid/yandex-search

Access to yandex.ru search engine for world-wide web searches.

When signing up with yandex.ru with a validated (international) mobile number, it allows 10k searches per day!

Example
--
>>> yandex = yandex_search.Yandex()
>>> yandex.search('"Interactive Saudi"')
{"results": [{
      "snippet": "Your Software Development Partner In  Saudi   Arabia . Since our early days in 2003, our main goal in  Interactive   Saudi   Arabia  has been: \"To earn customer respect and maintain long-term loyalty\".",
      "url": "http://www.interactive.sa/en",
      "title": "Interactive   Saudi   Arabia  Limited",
      "domain": "www.interactive.sa"
    }]
}

Getting Started
--
* register account: https://passport.yandex.ru/registration
  * use google translate addon (right-click "translate page")
* configure yandex: https://xml.yandex.ru/settings.xml
  * find "key" under "test"
  * set IP to your querying machine


Notes:
--
* Yandex highlights matching terms, leading to extra whitespace from `' '.join`

Alternatives
--
* pyyaxml is py2-only and was giving me grief ;)

Documentation
--
search operators:
    https://yandex.com/support/search/how-to-search/search-operators.html
settings:
    https://xml.yandex.ru/settings.xml
docs:
    https://tech.yandex.ru/xml/doc/dg/concepts/restrictions-docpage/
    https://yandex.com/support/search/robots/search-api.html

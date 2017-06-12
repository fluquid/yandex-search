# -*- coding: utf-8 -*-
"""
python library to interact with yandex.ru search engine
"""

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.3.2'

import os
import logging
import json

import requests
from lxml import etree
import six


class YandexResults(object):
    """
    results object
    TODO: date
    TODO: found[phrase, strict, all]
    """
    def __init__(self, date, reqid, found, items):
        self.date = date
        self.reqid = reqid
        self.found = found
        self.items = items

    def __str__(self):
        return json.dumps({
            'date': self.date,
            'reqid': self.reqid,
            'found': self.found,
            'items': '[items]'})


class YandexException(Exception):
    """
    generic yandex error, please see below for specific error cases
    https://tech.yandex.ru/xml/doc/dg/reference/error-codes-docpage/
    """
    def __init__(self, code, message):
        super(Exception, self).__init__(message)
        self.code = code


class NoResultsException(YandexException):
    """ error with the query/params passed """
    pass


class QueryException(YandexException):
    """ error with the query/params passed """
    pass


class ConfigException(YandexException):
    """ error with yandex configuration, needs to be addressed before
    any future requests """
    pass


class RateLimitException(YandexException):
    """ rate limit was exceeded, need to wait """
    pass


class Yandex(object):
    """
    initialize Yandex object with credentials.

    if no credentials provided, falls back to environment variables
    `YANDEX_USER` and `YANDEX_KEY`.
    """
    def __init__(self, api_user=None, api_key=None):
        self.api_user = api_user or os.environ['YANDEX_USER']
        self.api_key = api_key or os.environ['YANDEX_KEY']

    def _fetch_xml(self, query, page=0, group_by_domain=False):
        """ fetch xml from yandex web service """
        URL = 'https://yandex.com/search/xml'
        GROUPBY_FLAT = 'attr="".mode=flat.groups-on-page=100.docs-in-group=1'
        GROUPBY_DEEP = 'attr=d.mode=deep.groups-on-page=100.docs-in-group=1'
        params = {
            'user': self.api_user,
            'key': self.api_key,
            'query': query,
            'l10n': 'en',
            'sortby': 'rlv',
            'filter': 'none',
            'maxpassages': 5,
            'page': page,
            'groupby': GROUPBY_DEEP if group_by_domain else GROUPBY_FLAT
        }
        res = requests.get(URL, params=params)
        xml = res.content
        return xml

    def _raise_on_error(self, tree, xml):
        """ analyze response for errors and raise appropriate exception """
        errors = tree.xpath('//error')
        if errors:
            error = errors[0]
            try:
                code = int(error.attrib['code'])
            except (KeyError, ValueError) as e:
                logging.exception(e)
                raise Exception('unable to parse error code: ' +
                                (xml if six.PY2 else xml.decode('utf-8')))

            message = ' '.join(error.xpath('.//text()'))

            if code == 15:
                raise NoResultsException(code, message)

            elif code in (20, 31, 33, 34, 42, 43, 44, 48, 100):
                raise ConfigException(code, message)

            elif code in (32, 55):
                raise RateLimitException(code, message)

            elif code in (1, 2, 15, 18, 19, 37):
                raise QueryException(code, message)

            else:
                raise Exception('unknown error code %d "%s"', code, message)

    def _get_items(self, tree):
        """
        extract search results from response
        NOTE: currently flattens groups
        response:
          ['date'], reqid, found[*], found-human, found-docs[*],
          found-docs-human
        """
        docs = tree.xpath('//response/results/grouping/group/doc')
        for doc in docs:
            res = dict(
                url=doc.xpath('./url/text()')[0],
                domain=doc.xpath('./domain/text()')[0],
                title=' '.join(doc.xpath('./title//text()')),
                snippet=' '.join(doc.xpath('./passages//text()')))
            yield res

    def _parse_xml(self, xml):
        """ parse information from xml into YandexResult object """
        root = etree.XML(xml)
        self._raise_on_error(root, xml)

        # request = root.xpath('./request')
        # query, page, sortby, maxpassages, groupings

        date = root.xpath('./response/@date')[0]
        reqid = root.xpath('./response/reqid/text()')[0]
        founds = root.xpath('./response/found')
        found = {f.xpath('./@priority')[0]: f.xpath('./text()')[0]
                 for f in founds}
        items = list(self._get_items(root))
        return YandexResults(date, reqid, found, items)

    def search(self, query, page=0, group_by_domain=False):
        """
        make search request to yandex.ru

        - query: query string
            https://yandex.com/support/search/how-to-search/search-operators.html
        - returns a generator of SearchItems (dicts).
        - raises YandexException on errors.
        """
        logging.info('query "%s"', query)
        xml = self._fetch_xml(query=query,
                              page=page,
                              group_by_domain=group_by_domain)
        return self._parse_xml(xml)

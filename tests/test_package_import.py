import pytest
import yandex_search as yd
from httmock import all_requests, HTTMock


def test_package_metadata():
    assert yd.__author__
    assert yd.__email__


def test_xml_parse():
    @all_requests
    def response_success(url, request):
        xml = open('tests/success.xml', 'rb').read()
        return {'status_code': 200,
                'content': xml}

    with HTTMock(response_success):
        yandex = yd.Yandex(api_user='fake', api_key='fake')
        results = yandex.search(query='asdf')
        assert results.found['strict'] == '7'
        assert len(results.items) == 7
        for item in results.items:
            assert 'url' in item
            assert 'title' in item
            assert 'snippet' in item
            assert 'domain' in item


def test_credential_error():
    @all_requests
    def response_credential(url, request):
        xml = open('tests/credential_error.xml', 'rb').read()
        return {'content': xml}

    with HTTMock(response_credential):
        yandex = yd.Yandex(api_user='fake', api_key='fake')
        with pytest.raises(yd.ConfigException):
            yandex.search(query='asdf')


def test_no_results():
    @all_requests
    def response_credential(url, request):
        xml = open('tests/noresults_error.xml', 'rb').read()
        return {'content': xml}

    with HTTMock(response_credential):
        yandex = yd.Yandex(api_user='fake', api_key='fake')
        with pytest.raises(yd.NoResultsException):
            yandex.search(query='asdf')

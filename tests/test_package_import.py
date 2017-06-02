import yandex_search


def test_package_metadata():
    assert yandex_search.__author__
    assert yandex_search.__email__
    assert yandex_search.__version__

def test_xml_parse():
    xml = open('tests/success.xml', 'rb').read()
    yandex = yandex_search.Yandex(api_user='fake', api_key='fake')
    results = yandex._parse_xml(xml)
    assert results.found['strict'] == '7'
    assert len(results.items) == 7
    for item in results.items:
        assert 'url' in item
        assert 'title' in item
        assert 'snippet' in item
        assert 'domain' in item

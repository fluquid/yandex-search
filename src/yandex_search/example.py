#!/usr/bin/env python
import __init__ as yandex_search
import json

yandex = yandex_search.Yandex()

results = yandex.search('"Albert Einstein"')
print(results)
print(json.dumps(results.items,
                 sort_keys=True,
                 indent=4,
                 separators=(',', ': ')))

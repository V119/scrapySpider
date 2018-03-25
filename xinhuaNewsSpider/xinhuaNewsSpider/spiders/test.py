from __future__ import print_function

import json
import optparse
import sys
import urllib

from scrapy_jsonrpc.jsonrpc import jsonrpc_client_call, JsonRpcError
from six.moves.urllib.parse import urljoin

host = "127.0.0.1"
port = "6023"


def get_wsurl(path):
    return urljoin("http://%s:%s/" % (host, port), path)


def json_get(path):
    url = get_wsurl(path)
    return json.loads(urllib.request.urlopen(url).read())


def cmd_list_resources():
    """list-resources - list available web service resources"""
    for x in json_get('crawler/engine/open_spiders'):
        print(x)


if __name__ == "__main__":
    cmd_list_resources()

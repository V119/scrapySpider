import re

import json
from scrapy import Selector


def get_dom_html(response, domid, type_name='html'):
    sel = Selector(response)

    body_div = sel.xpath('//script/text()').extract()
    for body_html in body_div:
        # noinspection PyBroadException
        try:
            body_html = body_html.strip()
            text = ''
            if body_html.startswith('FM.view'):
                p_body = re.compile('^\s*FM\.view\(\{(.*)\}\)')
                json_html = p_body.search(body_html.replace('\n', '').replace('\t', ''))
                if json_html:
                    text = json.loads('{' + json_html.group(1) + '}')
            else:
                continue

            if 'domid' in text and domid in text['domid']:
                hot_html = text[type_name]

                return hot_html
        except:
            print('get domid ' + domid + ' error!!')

    return None


def get_page_conf_info(response, key):
    body_text = response.text
    p_key = re.compile(r'\$CONFIG\[\'' + key + '\'\]=\'(.*)\'')
    # noinspection PyBroadException
    try:
        value = p_key.search(body_text).group(1)
        if value:
            return value

    except:
        return None

    return None


def union_list(*str_list):
    s = set()
    for str_ in str_list:
        s.update(str_)

    return list(s)

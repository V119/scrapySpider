#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import ssl
from http import cookiejar
import http.cookiejar
import urllib

import re

from doubanTopic import settings


def login(user_name, password, cookie_file):
    """
    :param user_name:
    :param password:
    :return:
    """

    login_url = 'https://accounts.douban.com/login'

    login_data = {
        'source': 'None',
        'redir': 'https://www.douban.com',
        'form_email': user_name,
        'form_password': password,
        'login': '登陆'
    }

    try:
        captcha_id, captcha_code = get_captcha()
        login_data['captcha-solution'] = captcha_code
        login_data['captcha-id'] = captcha_id
    except:
        print('There is no code')

    cookie_jar = cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener2 = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener2)

    login_data = urllib.parse.urlencode(login_data)
    http_headers = settings.DEFAULT_REQUEST_HEADERS
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(login_url, data=login_data.encode(), headers=http_headers)
    response = urllib.request.urlopen(req)
    cookie_jar.save(cookie_file, ignore_discard=True, ignore_expires=True)

    # text = response.read().decode('utf-8')

    # print(text)


def get_captcha():
    url = 'https://accounts.douban.com/login'
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    data = urllib.request.urlopen(url, context=gcontext).read().decode()
    p = re.compile('name=\"captcha-id\"\s+value=\"(.*)\"')
    try:
        captcha_id = p.search(data).group(1)
        code_url = 'https://www.douban.com/misc/captcha?id=' + captcha_id + '&size=s'
        code_local_path = 'code.jpg'
        urllib.request.urlretrieve(code_url, code_local_path)
        captcha_code = input('input code!!!\n')
        return captcha_id, captcha_code
    except:
        return None


if __name__ == '__main__':
    user_name = 'yanghaov119@126.com'
    password = 'yanghao1004'
    cookie_file = 'douban_login_cookies'
    login(user_name, password, cookie_file)


def get_login_cookie(url):
    """
    :param url:
    :return:
    """

    cookie_file = settings.COOKIE_FILE

    if not os.path.exists(cookie_file):
        user_name = settings.USER_NAME
        passwd = settings.PASSWORD
        login(user_name, passwd, cookie_file)

    try:
        cookie_jar = http.cookiejar.LWPCookieJar(cookie_file)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        print('Load cookie succeeded')
    except http.cookiejar.LoadError:
        return None
    else:
        cookie_d = {}
        for cookie in cookie_jar:
            domain = cookie.domain
            if url.find(domain) > 0:
                cookie_d[cookie.name] = cookie.value
        return cookie_d

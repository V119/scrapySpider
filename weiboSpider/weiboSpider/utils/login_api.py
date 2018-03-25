#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from weiboSpider import settings

__author__ = 'Yh'

try:
    import os
    import sys
    import urllib
    import http.cookiejar
    import base64
    import re
    import hashlib
    import json
    import rsa
    import binascii
except ImportError:
    print(sys.stderr, "%s" % (sys.exc_info()))
    sys.exit(1)


def get_su(user_name):
    """
    :param user_name:
    :return:转换后的用户名
    """
    # html字符转义
    username_ = urllib.parse.quote(user_name).encode()
    username = base64.encodebytes(username_)[:-1].decode()
    return username


def get_prelogin_status(user_name):
    """
    :param user_name:
    :return:得到prelogin的准备数据，servertime, nonce, rsakv
    """
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' \
                   + get_su(user_name) \
                   + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
    data = urllib.request.urlopen(prelogin_url).read().decode()
    print('step1: Load prelogin url')
    p = re.compile('\((.*)\)')

    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonec = data['nonce']
        rsakv = data['rsakv']
        return servertime, nonec, rsakv
    except:
        print('Getting prelogin status err')
        return None


def get_sp_rsa(password, servertime, nonce):
    """
    该函数对应ssologin.js的这一段
        request.servertime = me.servertime;
        request.nonce = me.nonce;
        request.pwencode = "rsa2";
        request.rsakv = me.rsakv;
        var RSAKey = new sinaSSOEncoder.RSAKey();
        RSAKey.setPublic(me.rsaPubkey, "10001");
        password = RSAKey.encrypt([me.servertime, me.nonce].join("\t") + "\n" + password)
    :param password:
    :param servertime:
    :param nonce:
    :return: password
    """
    # 这个值可以在prelogin上得到，因为是固定的，所以写死
    pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F' \
             '915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F67398' \
             '84B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    rsa_key = 65537  # 10001的十进制
    message_ = str(servertime) + '\t' + str(nonce) + '\n' + password
    message = message_.encode()
    key = rsa.PublicKey(int(pubkey, 16), rsa_key)
    encrypt_pwd = rsa.encrypt(message, key)

    return binascii.b2a_hex(encrypt_pwd)


def do_login(user_name, password, cookie_file):
    """
    :param user_name:
    :param password:
    :param cookie_file:
    :return:
    """
    # Post表单提交的数据
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'pagerefer': 'http://login.sina.com.cn/sso/logout.php?'
                     'entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
        'vsnf': '1',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv': '',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '202',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    cookie_jar = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener2 = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    try:
        servertime, nonce, rsakv = get_prelogin_status(user_name)
    except:
        return

    login_data['su'] = get_su(user_name)
    login_data['sp'] = get_sp_rsa(password, servertime, nonce)
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['rsakv'] = rsakv
    login_data = urllib.parse.urlencode(login_data)
    http_headers = {
        'Accept': 'test/javascript, application/javascript,application/ecmascript, '
                  'application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN, zh; q=0.8, en-US; q=0.5, en; q=0.3',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0(Windows NT 10.0; Win64'
                      '; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    req = urllib.request.Request(login_url, data=login_data.encode(), headers=http_headers)
    response = urllib.request.urlopen(req)
    # noinspection PyBroadException
    try:
        text = response.read().decode('gbk')
    except:
        text = response.read().decode('utf-8')
    print('step2: Signin with post_data')
    p = re.compile('location\.replace\([\'\"](.*?)[\'\"]\)')
    try:
        login_url2 = p.search(text).group(1)  # http://passport.weibo.com/wbsso/login/.../
        req2 = urllib.request.Request(login_url2, headers=http_headers)
        data = urllib.request.urlopen(req2).read().decode('gbk')
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar.save(cookie_file, ignore_discard=True, ignore_expires=True)
            print('step3: Save cookies after login succeeded')
            return 1
        else:
            return 0
    except:
        return 0


def get_login_cookie(url):
    """
    :param url:
    :return:
    """

    cookie_file = settings.COOKIE_FILE

    if not os.path.exists(cookie_file):
        user_name = settings.USER_NAME
        passwd = settings.PASSWORD
        do_login(user_name, passwd, cookie_file)

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


def load_cookie(cookie_file):
    """
    :param cookie_file:
    :return:
    """
    try:
        cookie_jar = http.cookiejar.LWPCookieJar(cookie_file)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        cookie_support = urllib.request.HTTPCookieProcessor(cookie_jar)
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        print('Load cookie succeeded')
        return 1
    except http.cookiejar.LoadError:
        return 0


def login(user_name, passwd, cookie_file):
    """
    :param user_name:
    :param passwd:
    :param cookie_file:
    :return:
    """
    if os.path.exists(cookie_file) and load_cookie(cookie_file):
        return 1
    else:
        return do_login(user_name, passwd, cookie_file)


def test_with_mayun():
    test_url = 'http://weibo.com/mayun'
    response_ = urllib.request.urlopen(test_url).read()
    try:
        global response
        response = response_.decode('gbk')
    except UnicodeDecodeError:
        response = response_.decode()
    # print response
    p = re.compile(r'\$CONFIG\[\'uid\'\]')
    if not p.search(response):
        print('Please Login')
    else:
        nick_p = re.compile(r'\$CONFIG\[\'nick\'\]=\'(.*)\'')
        nick = nick_p.search(response).group(1)
        print(nick, ' ', 'Already Login')


if __name__ == '__main__':
    test_with_mayun()
    if login(settings.USER_NAME, settings.PASSWORD, settings.COOKIE_FILE):
        print('Login Weibo succeeded')
        test_with_mayun()
    else:
        print('Login Weibo failed')

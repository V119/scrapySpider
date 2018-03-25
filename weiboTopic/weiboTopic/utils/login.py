#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os


def get_cookies(file_path):
    if not os.path.exists(file_path):
        print("没有cookies文件")
        return

    cookie_d = {}

    with open(file_path) as f:
        data = f.read()
        json_obj = json.loads(data)
        for cookie in json_obj:
            if 'name' in cookie and 'value' in cookie:
                cookie_d[cookie['name']] = cookie['value']

    return cookie_d

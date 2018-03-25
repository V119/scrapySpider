#!/usr/bin python3
# -*- coding: utf-8 -*-
import hashlib


# 产生MD5码
def md5_code(src):
    if not src:
        raise ValueError('参数不能为空!!')

    m = hashlib.md5()
    if isinstance(src, str):
        m.update(src.encode())
    elif isinstance(src, bytes):
        m.update(src)
    elif isinstance(src, int):
        m.update(str(src).encode())
    else:
        raise TypeError("need str or bytes")

    md5value = m.hexdigest()

    return md5value

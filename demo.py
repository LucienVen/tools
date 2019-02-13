#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests

r = requests.get('https://www.baidu.com')
print(r)
print(r.text)
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 使用sm.ms 实现图床上传脚本
# API DOC FROM https://sm.ms/doc/

import requests
import json
import sys
import os

upload_url = 'https://sm.ms/api/upload';
# 获取图片

# 检查图片参数是否输入
if 2 > len(sys.argv):
    sys.exit('Missing image parameters...')
elif 2 < len(sys.argv):
    sys.exit('Too more image parameters...')
else:
    # 获取图片路径
    path = sys.argv[1]


# 检查图片是否存在
if os.path.exists(path):
    files = {'smfile': open(path, 'rb')}
    # 发起请求
    r = requests.post(upload_url, files=files)
    if r.status_code == requests.codes.ok:
        # 把字符串装换成字典
        return_data = json.loads(r.text)
        if return_data['code'] == 'success':
            print('upload photo success!')
            # 输出
            print(return_data['data']['url'])
else:
    sys.exit('File Not Found')
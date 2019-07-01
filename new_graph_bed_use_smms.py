#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 使用sm.ms 实现图床上传脚本
# API DOC FROM https://sm.ms/doc/
# 支持传入宽度width信息，进行尺寸缩放

import requests
import json
import sys
import os
# 引入PIL库，实现图片缩放
from PIL import Image


# 图片缩放
def zoom(origin_file, width):
    set_width = width
    im = Image.open(origin_file)
    # 获得图像尺寸:
    w, h = im.size

    # 缩放倍率
    prop = w / set_width
    set_height = h / prop

    # 缩放
    im.thumbnail((set_width, set_height))
    # 返回image对象
    return im

# 图片上传
def upload(path, upload_url='https://sm.ms/api/upload'):
    files = {'smfile': open(path, 'rb')}
    # 发起请求
    r = requests.post(upload_url, files=files)
    if r.status_code == requests.codes.ok:
        # 把字符串装换成字典
        return_data = json.loads(r.text)
        if return_data['code'] == 'success':
            return {'status': 'success', 'data': return_data['data']['url']}
        else:
            return_data = json.loads(r.text)
            # sys.exit(return_data)
            return {'status': 'error', 'data': return_data}



def main():
    upload_url = 'https://sm.ms/api/upload'
    # 检查图片参数是否输入
    try:
        origin_file = sys.argv[1];
    except IndexError:
        sys.exit('Missing parameters')

    # 检查图片是否存在
    if os.path.exists(origin_file) is not True:
        sys.exit('File Not Exists')


    # 检查是否传入限定宽度数据
    try:
        set_width = sys.argv[2]
        # 获取文件后缀
        file_suffix = os.path.splitext(origin_file)[-1][1:]
        # 获取文件名（不带后缀）
        base_filename = os.path.splitext(origin_file)[0]
        # 获取处理后的图片对象
        im = zoom(origin_file, int(set_width))
        # 存储缩放后的新图片到本地
        new_filename = '_'.join([base_filename, 'prop']) + '.' +file_suffix
        im.save(new_filename, file_suffix)

        # 调用上传
        res = upload(new_filename, upload_url)
        print(res)

    except IndexError:
        res = upload(origin_file, upload_url)
        print(res)

if __name__ == "__main__":
    main()
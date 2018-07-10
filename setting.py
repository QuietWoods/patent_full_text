# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 9:03
# @Author  : QuietWoods
# @FileName: setting.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import os
"""
路径设置
"""
# 工程根目录，注意此处以初次调用这个变量的元素为准，工程起始目录定位在main，若有修改请注意这个位置
BASE_PATH = os.path.split(__file__)[0]
# 验证码模型地址
CAPTCHA_MODEL_NAME = os.path.join(BASE_PATH, 'res', 'captcha', 'sipo3.job')
# 是否使用代理
USE_PROXY = False
# 请求超时，单位秒
TIMEOUT = 10
# 请求延时，单位秒
DOWNLOAD_DELAY = 1

if __name__ == '__main__':
    print(os.path.split(__file__))
    print(BASE_PATH)
    print(CAPTCHA_MODEL_NAME)
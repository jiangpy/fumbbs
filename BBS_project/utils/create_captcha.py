#! /usr/bin/env python
# coding:utf-8

import string
import random

# 随机生成固定位数的随机验证码
def create_captcha():
    count = 4
    list1 = string.letters+string.digits
    return ''.join(random.sample(list1,count))

# 随机生成固定位数的数字验证码
def number_captcha():
    count = 6
    list1 = string.digits
    return ''.join(random.sample(list1,count))

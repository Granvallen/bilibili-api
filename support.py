# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17  16:34:00 2018

@author: Granvallen
"""

import urllib.error
import urllib.request
import urllib.parse
import json
import zlib
import time
import math
import hashlib
import sys
import os
import re
import logging


def getRE(content, regexp):
    """
    正则匹配re.findall函数封装
    """
    return re.findall(regexp, content, re.S)

def getREsearch(content, regexp):
    """
    正则匹配re.search函数封装
    """
    return re.search(regexp, content, re.S)

def getREsub(content, repl, regexp):
    """
    正则匹配re.sub函数封装
    """
    return re.sub(regexp, repl, content, re.S)

def getURLContent(url, cookie=''):
    """
    从url获取内容, 返回内容字符串
    """
    while True:
        flag = True
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'Referer': 'https://www.bilibili.com',
                'Cookie': cookie
            }
            req = urllib.request.Request(url, headers=headers)
            page = urllib.request.urlopen(req)
            content = page.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logging.error('服务器表示并没有找到网站...code:{}'.format(e.code))
                return ''
            elif e.code == 403:
                logging.error('服务器傲娇地拒绝了访问请求...code:{}'.format(e.code))
                return ''
            flag = False
            time.sleep(5)
        except urllib.error.URLError as e:
            logging.error('请检查网络连接...')
            return ''
        if flag: 
            break
        logging.info('尝试重新连接...')
    if page.getheader('Content-Encoding') == 'gzip':
        content = str(zlib.decompress(content, 16+zlib.MAX_WBITS), 'utf-8')
    return content

class JsonInfo():
    """
    处理json数据类
    """
    def __init__(self, content, pre_deal=lambda x:x):
        self.info = json.loads(pre_deal(content))
        self.error = False
        # 1
        if 'code' in self.info and self.info['code'] != 0:
            
            if 'msg' in self.info:
                logging.error("code={0}, msg={1}".format(self.info['code'], self.info['msg']))
                self.ERROR_MSG = self.info['message']
            elif 'error' in self.info:
                logging.error("code={0}, msg={1}".format(self.info['code'], self.info['error']))
                self.ERROR_MSG = self.info['error']
            self.error = True
        # 2
        if 'error' in self.info and 'code' in self.info['error']:
            logging.error("code={0}, msg={1}".format(self.info['error']['code'], self.info['error']['message']))
            self.ERROR_MSG = self.info['error']['message']
            self.error = True


    def getValue(self, *keys):
        if len(keys) == 0:
            return None
        if keys[0] in self.info:
            temp = self.info[keys[0]]
        else:
            return None
        if len(keys) > 1:
            for key in keys[1:]:
                if type(temp) == dict and key in temp:
                    temp = temp[key]
                else:
                    return None
        return temp

    def __getitem__(self, keys):  # 重载 []
        if not isinstance(keys, tuple):
            keys = (keys,)

        if len(keys) == 0:
            return None

        if keys[0] in self.info:
            temp = self.info[keys[0]]
        else:
            return None

        if len(keys) > 1:
            for key in keys[1:]:
                if type(temp) == dict and key in temp:
                    temp = temp[key]
                else:
                    return None
        return temp

    def keys(self):
        return self.info.keys()

def num2time(num):
    """
    对视频发布时间格式化
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(num))

def num2duration(num):
    """
    对视频时长的格式化
    """
    m = num // 60
    s = num - m*60
    return '{0:0>2}:{1:0>2}'.format(m, s)
    # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(num))

def UrlEncode(content):
    """
    urllib.parse.quote函数的封装, 字符串URL编码
    """
    return urllib.parse.quote(content)

def getSign(params, secretkey):
    """
    获取API的签名sign, 获取视频源地址需要
    """
    return hashlib.md5(bytes(params + secretkey, 'utf8')).hexdigest()

if __name__ == "__main__":
    pass
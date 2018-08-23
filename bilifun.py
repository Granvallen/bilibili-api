#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19  22:59:00 2018

@author: Granvallen
"""

from bilibili import *
import os

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    aid = getREsearch(sys.argv[1], r'av(\d+)')
    if aid:
        aid = int(aid.group(1))
        pid = getREsearch(sys.argv[1], r'p=(\d+)')
        pid = int(pid.group(1)) if pid else 1
    else:
        content = getURLContent(sys.argv[1])
        aid = getREsearch(content, r'AV(\d+)')
        if aid:
            aid = int(aid.group(1))
        else:
            logging.error('查找视频av号失败 >_<')
        pid = 1
    mpvPlayVideo(aid, pid)


if __name__ == "__main__":
    main()
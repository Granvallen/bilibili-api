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
    aid = getAid(sys.argv[1])
    pid = getREsearch(sys.argv[1], r'p=(\d+)')

    if not pid:
        pid = 1

    mpvPlayVideo(aid, pid)


if __name__ == "__main__":
    main()
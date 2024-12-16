#!/usr/bin/python
# coding: utf-8
#
# Name:		~/.zshrc-sazae/python/sazae_extract_common_parts.py
# Version:	v03
# Time-stamp:   <2021.10.03-18:13:20-JST>
#
# Copyright (C) 2017-2021  Seiichiro HATA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#                                  概要
#
# 引数の先頭からの共通部分を抽出し，表示します。
#
# 例：> echo 'abcdef\nabcghi\nabcjkl' | ./sazae_extract_common_part.py
#     abc


############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v03'
PYTHON_VERSION = sys.version_info[0]


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: ' + sys.argv[0] + ' [strings]')
        print('Options:')
        print('  -h, --help            show this message and exit')
        print('  -v, --version         show version number and exit')
        exit(0)
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print(sys.argv[0] + ' ' + VERSION)
        exit(0)


############################################################
# GET CANDIDATES
############################################################


candidates = sys.stdin.read().splitlines()


############################################################
# EXTRACT COMMON PART
############################################################


def adjust_backlash(s):
    s = s.replace('\\', '\\\\')
    # s = s.replace('\\\\~', '\\~')
    s = s.replace('\\\\}', '\\}')
    s = s.replace('\\\\|', '\\|')
    s = s.replace('\\\\{', '\\{')
    s = s.replace('\\\\`', '\\`')
    # s = s.replace('\\\\_', '\\_')
    # s = s.replace('\\\\^', '\\^')
    s = s.replace('\\\\]', '\\]')
    # s = s.replace('\\\\\\', '\\\\')
    s = s.replace('\\\\[', '\\[')
    s = s.replace('\\\\?', '\\?')
    s = s.replace('\\\\>', '\\>')
    # s = s.replace('\\\\=', '\\=')
    s = s.replace('\\\\<', '\\<')
    s = s.replace('\\\\;', '\\;')
    # s = s.replace('\\\\:', '\\:')
    # s = s.replace('\\\\/', '\\/')
    # s = s.replace('\\\\-', '\\-')
    # s = s.replace('\\\\,', '\\,')
    s = s.replace('\\\\*', '\\*')
    s = s.replace('\\\\)', '\\)')
    s = s.replace('\\\\(', '\\(')
    s = s.replace("\\\\'", "\\'")
    s = s.replace('\\\\&', '\\&')
    # s = s.replace('\\\\%', '\\%')
    s = s.replace('\\\\$', '\\$')
    s = s.replace('\\\\#', '\\#')
    s = s.replace('\\\\"', '\\"')
    s = s.replace('\\\\!', '\\!')
    s = s.replace('\\\\ ', '\\ ')
    # s = s.replace('\\\\n', '\\n')
    s = s.replace('\\\\t', '\\t')
    return s


def extract_common_part(c):
    for i in range(len(c)):
        c[i] = adjust_backlash(c[i])
    if(PYTHON_VERSION == 2):
        u = c[0].decode('utf-8')
    else:
        u = c[0]
    for i in range(len(u)+1):
        if(PYTHON_VERSION == 2):
            t = u[0:i].encode('utf-8')
        else:
            t = u[0:i]
        for j in range(len(c)):
            if(j == 0):
                continue
            if(not c[j].startswith(t)):
                return i - 1
    return i


p = extract_common_part(candidates)
if(PYTHON_VERSION == 2):
    print(candidates[0].decode('utf-8')[0:p].encode('utf-8'))
else:
    print(candidates[0][0:p])

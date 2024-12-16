#!/usr/bin/python
# coding: utf-8
#
# Name:		~/.zshrc-sazae/python/sazae_separate_partial_variable.py
# Version:	v02
# Time-stamp:   <2021.10.03-10:12:48-JST>
#
# Copyright (C) 2018-2021  Seiichiro HATA
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
# 引数を部分変数に分解して表示します。
#
# 例：> ./sazae_separate_partial_command.py 'a$b c${d}e'
#     'a'
#     '$b'
#     ' c'
#     '${d}'
#     'e'


############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v02'
PYTHON_VERSION = sys.version_info[0]
NOT_ESCAPED = '^((.*[^\\\\])?(\\\\\\\\)*)?'


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: ' + sys.argv[0] + ' [string]')
        print('Options:')
        print('  -h, --help            show this message and exit')
        print('  -v, --version         show version number and exit')
        exit(0)
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print(sys.argv[0] + ' ' + VERSION)
        exit(0)


############################################################
# GET STRING
############################################################


if(PYTHON_VERSION == 2):
    string = sys.argv[1].decode('utf-8')
else:
    string = sys.argv[1]


############################################################
# SEPARATE
############################################################


# 部分文字列を表示
def print_string(s):
    if(PYTHON_VERSION == 2):
        print(s.encode('utf-8'))
    else:
        print(s)


# 分割
temp = ''  # 部分文字列
unit = ''  # 変数の判定
for c in list(string):
    if(re.match(NOT_ESCAPED + '$', temp) and c == '\''):
        temp = temp + c
        if(unit == ''):
            unit = '\''
        elif(unit == '\''):
            unit = ''
    elif(re.match(NOT_ESCAPED + '\\$$', temp) and re.match('^[_a-zA-Z]$', c)):
        if(unit == ''):
            print_string(re.sub('\\$$', '', temp))
            temp = '$' + c
            unit = '$'
        else:
            temp = '$' + c
    elif(re.match(NOT_ESCAPED + '\\${$', temp) and re.match('^[_a-zA-Z]$', c)):
        if(unit == ''):
            print_string(re.sub('\\${$', '', temp))
            temp = '${' + c
            unit = '${'
        else:
            temp = temp + c
    elif(re.match(NOT_ESCAPED + '$', temp) and
         re.match('^[^_a-zA-Z0-9{}]$', c)):
        if(unit == '$'):
            print_string(temp)
            temp = c
            unit = ''
        else:
            temp = temp + c
    elif(re.match(NOT_ESCAPED + '$', temp) and c == '}'):
        if(unit == '${'):
            print_string(temp + c)
            temp = ''
            unit = ''
        else:
            temp = temp + c
    else:
        temp = temp + c
print_string(temp)

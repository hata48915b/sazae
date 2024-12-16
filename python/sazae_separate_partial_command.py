#!/usr/bin/python
# coding: utf-8
#
# Name:		~/.zshrc-sazae/python/sazae_separate_partial_command.py
# Version:	v04
# Time-stamp:   <2021.10.03-10:24:42-JST>
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
# 引数を部分コマンドに分解して表示します。
#
# 例：> ./sazae_separate_partial_command.py 'a`echo b`c$(echo d)e'
#     'a'
#     '`echo b`'
#     'c'
#     '$(echo d)'
#     'd'


############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v04'
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


# 文字列のユニットを判断
def judge_unit(unit, char):
    unit = unit + char
    for c in unit:
        # c = '|"|`|(|)
        if(c == '\''):
            unit = re.sub('\'[^\']*\'', '', unit, 1)
        elif(c == '"'):
            unit = re.sub('"[^"]*"', '', unit, 1)
        elif(c == '`'):
            unit = re.sub('`[^`]*`', '', unit, 1)
        elif(c == '('):
            unit = re.sub('\\([^\\(\\)]*\\)', '', unit, 1)
        elif(c == ')'):
            unit = re.sub('\\)', '', unit, 1)
    return unit


# 分割
temp = ''  # 部分文字列
unit = ''  # コマンドの判定
for c in list(string):
    if(re.match(NOT_ESCAPED + '$', temp) and c == '`'):
        if(unit == ''):
            print_string(temp)
            temp = c
        elif(unit == '`'):
            print_string(temp + c)
            temp = ''
        else:
            temp = temp + c
    elif(re.match(NOT_ESCAPED + '$', temp) and c == '('):
        if(unit == ''):
            if(re.match(NOT_ESCAPED + '\\$$', temp)):
                print_string(re.sub('\\$$', '', temp))
                temp = '$' + c
            else:
                print_string(temp)
                temp = c
        else:
            temp = temp + c
    elif(re.match(NOT_ESCAPED + '$', temp) and c == ')'):
        if(unit == '('):
            print_string(temp + c)
            temp = ''
        else:
            temp = temp + c
    else:
        temp = temp + c
    if(re.match('^[\'`\\(\\)]$', c)):
        if(re.match(NOT_ESCAPED + '$', temp)):
            unit = judge_unit(unit, c)
print_string(temp)

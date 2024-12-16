#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/python/sazae_get_grep_key.py
# Version:      v06
# Time-stamp:   <2021.10.03-18:10:49-JST>
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
# ls形式の正規表現を，grep形式の正規表現に変換します。
#
# 例：> ./sazae_get_grep_style_regexp.py '.a+b$c?d*e'f'g"h"i'
#     \.a\+b\$c.?d.*efghi

############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v06'
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
# MAIN
############################################################


_key = sys.argv[1]
_key = _key.replace('.', '\\.')
_key = _key.replace('+', '\\+')

_temp = ''
_unit = 'N'
for _char in _key:
    if(_unit == 'S'):
        if(_char == "'"):
            _unit = 'N'
        elif(_char == '?'):
            _temp = _temp + '\\?'
        else:
            _temp = _temp + _char
    elif(_unit == 'D'):
        if((_char == '"') and re.match(NOT_ESCAPED + '$', _temp)):
            _unit = 'N'
        elif((_char == '*') and re.match(NOT_ESCAPED + '$', _temp)):
            _temp = _temp + '.*'
        elif((_char == '?') and re.match(NOT_ESCAPED + '$', _temp)):
            _temp = _temp + '.'
        else:
            _temp = _temp + _char
    else:
        if((_char == "'") and re.match(NOT_ESCAPED + '$', _temp)):
            _unit = 'S'
        elif((_char == '"') and re.match(NOT_ESCAPED + '$', _temp)):
            _unit = 'D'
        elif((_char == '*') and re.match(NOT_ESCAPED + '$', _temp)):
            _temp = _temp + '.*'
        elif((_char == '?') and re.match(NOT_ESCAPED + '$', _temp)):
            _temp = _temp + '.'
        else:
            _temp = _temp + _char
_key = _temp

_key = _key.replace('\\', '\\\\')
_key = _key.replace("\\\\'", "'")
_key = _key.replace('\\\\"', '\\\\\\"')
_key = _key.replace('\\\\$', '\\\\\\$')

print(_key)

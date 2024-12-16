#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/python/sazae__git_decode_utf8.py
# Version:      v01
# Time-stamp:   <2021.10.05-10:05:28-JST>
#
# Copyright (C) 2021  Seiichiro HATA
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
# "git ls-files"の結果を漢字に変換します。
#
# 例: > git ls-files | ./sazae_git_ls_files.py
#     abcdef.py
#     あいう.py


############################################################
# IMPORT
############################################################


import sys
import re
import codecs


############################################################
# CONSTANT
############################################################


VERSION = 'v01'
PYTHON_VERSION = sys.version_info[0]


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: (stdout) | ' + sys.argv[0] + ' [option]')
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


while(True):
    try:
        if(PYTHON_VERSION == 2):
            i = raw_input()
        else:
            i = input()
        i = re.sub('^"', '', i)
        i = re.sub('"$', '', i)
        i = i.replace('\\\\', '\\\\-')  # Go away
        i = i.replace('\\t', '\\\\\t')
        # i = i.replace('\n', '\\\\\n')  # Impossible
        i = i.replace(' ', '\\\\ ')
        i = i.replace("!", "\\\\!")
        # i = i.replace('"', '\\\\"')
        # i = i.replace('#', '\\\\#')
        i = i.replace('$', '\\\\$')
        # i = i.replace('%', '\\\\%')
        i = i.replace('&', '\\\\&')
        i = i.replace("'", "\\\\'")
        i = i.replace('(', '\\\\(')
        i = i.replace(')', '\\\\)')
        i = i.replace('*', '\\\\*')
        # i = i.replace(',', '\\\\,')
        # i = i.replace('-', '\\\\-')
        # i = i.replace('/', '\\\\/')
        # i = i.replace(':', '\\\\:')
        i = i.replace(';', '\\\\;')
        i = i.replace('<', '\\\\<')
        # i = i.replace('=', '\\\\=')
        i = i.replace('>', '\\\\>')
        i = i.replace("?", "\\\\?")
        # i = i.replace('@', '\\\\@')
        i = i.replace('[', '\\\\[')
        # i = i.replace('\\', '\\\\\\')  # Not here
        i = i.replace(']', '\\\\]')
        # i = i.replace('^', '\\\\^')
        # i = i.replace('_', '\\\\_')
        i = i.replace('`', '\\\\`')
        i = i.replace('{', '\\\\{')
        i = i.replace('|', '\\\\|')
        i = i.replace('}', '\\\\}')
        # i = i.replace('~', '\\\\~')
        i = i.replace('\\\\-', '\\\\\\\\')  # Return
        i = codecs.getdecoder('unicode_escape')(i)[0]
        i = i.encode('latin1').decode('utf-8')
        print(i)
    except EOFError:
        break

#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/sazae_check_candidates.py
# Version:      v09
# Time-stamp:   <2021.10.03-10:40:30-JST>
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
# 標準入力から補完候補を受け取り，形式をチェックして表示します。
#
# 例：> echo '/' | ./sazae_check_candidates.py -d '/home' 'dire' '' ''
#     '/'
#
# 例：> echo '/home' | ./sazae_check_candidates.py 'dire' '' ''
#     '/home/'
#
# 例：> echo 'a.exe\nb.txt\nc.pdf' | ./sazae_check_candidates.py '' '' ''
#     a.jpg
#     b.txt
#     c.pdf
#
# 例：> echo 'a.exe\nb.txt\nc.pdf' \
#         | ./sazae_check_candidates.py '' '^.*\.(t|T)(x|X)|(t|T)$' ''
#     b.txt
#
# 例：> ls -l a.exe b.txt c.pdf
#     -rwxr-xr-x 1 root root 0 Jan 01 01:01 a.exe
#     -rw-r--r-- 1 root root 0 Jan 01 01:01 b.txt
#     -r--r--r-- 1 root root 0 Jan 01 01:01 c.pdf
#     > echo 'a.exe\nb.txt\nc.pdf' \
#         | ./sazae_check_candidates.py '' '' '!000100100100'
#     a.jpg
#     b.txt


############################################################
# IMPORT
############################################################


import sys
import os
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v09'
if((len(sys.argv) >= 3) and (sys.argv[1] == '-d')):
    PWD = sys.argv[2]
    del sys.argv[1:3]
else:
    PWD = ''
if(PWD == ''):
    PWD = os.getcwd()
MODE = sys.argv[1]
REGEXP = sys.argv[2]
PERMISSION = sys.argv[3]


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: (stdout) | ' + sys.argv[0] + ' [mode]')
        print('Options:')
        print('  -h, --help            show this message and exit')
        print('  -v, --version         show version number and exit')
        print('  -d <path>             specify the current directory')
        exit(0)
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print(sys.argv[0] + ' ' + VERSION)
        exit(0)


############################################################
# GET CANDIDATES
############################################################


candidates = sys.stdin.read().splitlines()


############################################################
# CHECK CANDIDATES
############################################################


for i, c in enumerate(candidates):
    c_esc = c
    c_esc = c_esc.replace('\\', '\\\\')  # Convert first
    c_esc = c_esc.replace('\t', '\\\t')
    # c_esc = c_esc.replace('\n', '\\\n')  # Impossible
    c_esc = c_esc.replace(' ', '\\ ')
    c_esc = c_esc.replace("!", "\\!")
    c_esc = c_esc.replace('"', '\\"')
    c_esc = c_esc.replace('#', '\\#')
    c_esc = c_esc.replace('$', '\\$')
    # c_esc = c_esc.replace('%', '\\%')
    c_esc = c_esc.replace('&', '\\&')
    c_esc = c_esc.replace("'", "\\'")
    c_esc = c_esc.replace('(', '\\(')
    c_esc = c_esc.replace(')', '\\)')
    c_esc = c_esc.replace('*', '\\*')
    # c_esc = c_esc.replace(',', '\\,')
    # c_esc = c_esc.replace('-', '\\-')
    # c_esc = c_esc.replace('/', '\\/')
    # c_esc = c_esc.replace(':', '\\:')
    c_esc = c_esc.replace(';', '\\;')
    c_esc = c_esc.replace('<', '\\<')
    # c_esc = c_esc.replace('=', '\\=')
    c_esc = c_esc.replace('>', '\\>')
    c_esc = c_esc.replace("?", "\\?")
    # c_esc = c_esc.replace('@', '\\@')
    c_esc = c_esc.replace('[', '\\[')
    # c_esc = c_esc.replace('\\', '\\\\')  # Already
    c_esc = c_esc.replace(']', '\\]')
    # c_esc = c_esc.replace('^', '\\^')
    # c_esc = c_esc.replace('_', '\\_')
    c_esc = c_esc.replace('`', '\\`')
    c_esc = c_esc.replace('{', '\\{')
    c_esc = c_esc.replace('|', '\\|')
    c_esc = c_esc.replace('}', '\\}')
    # c_esc = c_esc.replace('~', '\\~')
    if(os.path.isdir(c)):
        if((MODE == 'Link') or (MODE == 'Dire') or (MODE == 'File')):
            if(re.match('^/', c)):
                path = PWD + '/NOT_CURRENT_DIRECTORY'
                # path = c
            else:
                path = PWD + '/' + c
            if(not re.match('^(.*)//[^/]*$', path)):
                path = re.sub('/+', '/', path)  # "..//a" -> "..//ab"
            # path = re.sub('/+$', '', path)  # Impossible
            while(re.match('^(.*)/[^/]+/\\.\\./', path)):
                path = re.sub('/[^/]+/\\.\\./', '/', path, 1)
        else:
            path = PWD + '/NOT_CURRENT_DIRECTORY'
        if(path != PWD):
            if(c == '/'):
                print(c_esc)
            else:
                print(c_esc + '/')
    elif(os.path.islink(c)):
        if((MODE != 'dire') and (MODE != 'Dire')):
            if(os.path.isdir(c)):
                print(c_esc + '/')
            else:
                if(re.match(REGEXP, c)):
                    print(c_esc)
    else:
        if((MODE != 'dire') and (MODE != 'Dire') and
           (MODE != 'link') and (MODE != 'Link')):
            if(re.match(REGEXP, c)):
                if(PERMISSION == ''):
                    print(c_esc)
                else:
                    mod_d = os.stat(c).st_mode
                    mod_o = \
                        str(int(mod_d / (8**3)) % 8) + \
                        str(int(mod_d / (8**2)) % 8) + \
                        str(int(mod_d / (8**1)) % 8) + \
                        str(int(mod_d / (8**0)) % 8)
                    per = ''
                    for i in mod_o:
                        per = per + \
                              str(int(int(i) / (2**2)) % 2) + \
                              str(int(int(i) / (2**1)) % 2) + \
                              str(int(int(i) / (2**0)) % 2)
                    if(re.match('^!', PERMISSION)):
                        if(not re.match(PERMISSION, '!' + per)):
                            print(c_esc)
                    else:
                        if(re.match(PERMISSION, per)):
                            print(c_esc)

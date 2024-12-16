#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/python/sazae_line_up.py
# Version:      v07
# Time-stamp:   <2021.10.03-18:08:39-JST>
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
# 標準入力から一覧を受け取り，きれいに並べて表示します
#
# 例：> echo '/bin\n/dev\n/home\n/lib\n/media\n/proc\n/sbin\n/usr\n/boot' \
#         | ./sazae_line_up.py -w 40
#     /bin   /home  /media /sbin  /boot
#     /dev   /lib   /proc  /usr


############################################################
# IMPORT
############################################################


import sys
import os
# import stat
import re
import unicodedata
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


############################################################
# CONSTANT
############################################################


VERSION = 'v07'
PYTHON_VERSION = sys.version_info[0]
TERMINAL_WIDTH = 80
LIST_COLORS = ''
for i in [1, 3]:
    if(len(sys.argv) >= (i + 2)):
        if(sys.argv[i] == '-w'):
            TERMINAL_WIDTH = int(sys.argv[i + 1])
        if(sys.argv[i] == '-c'):
            LIST_COLORS = sys.argv[i + 1]


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: (stdout) | ' + sys.argv[0] + ' [option]')
        print('Options:')
        print('  -h, --help            show this message and exit')
        print('  -v, --version         show version number and exit')
        print('  -w <width>            specify the width of the terminal')
        exit(0)
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print(sys.argv[0] + ' ' + VERSION)
        exit(0)


############################################################
# FUNCTIONS
############################################################


# REMOVE BACKSLASH
def remove_backslash(s):
    # s = s.replace('\\~', '~')
    s = s.replace('\\}', '}')
    s = s.replace('\\|', '|')
    s = s.replace('\\{', '{')
    s = s.replace('\\`', '`')
    # s = s.replace('\\_', '_')
    # s = s.replace('\\^', '^')
    s = s.replace('\\]', ']')
    # s = s.replace('\\\\', '\\')  # Already
    s = s.replace('\\[', '[')
    # s = s.replace('\\@', '@')
    s = s.replace("\\?", "?")
    s = s.replace('\\>', '>')
    # s = s.replace('\\=', '=')
    s = s.replace('\\<', '<')
    s = s.replace('\\;', ';')
    # s = s.replace('\\:', ':')
    # s = s.replace('\\/', '/')
    # s = s.replace('\\-', '-')
    # s = s.replace('\\,', ',')
    s = s.replace('\\*', '*')
    s = s.replace('\\)', ')')
    s = s.replace('\\(', '(')
    s = s.replace("\\'", "'")
    s = s.replace('\\&', '&')
    # s = s.replace('\\%', '%')
    s = s.replace('\\$', '$')
    s = s.replace('\\#', '#')
    s = s.replace('\\"', '"')
    s = s.replace("\\!", '!')
    s = s.replace('\\ ', ' ')
    # s = s.replace('\\\n', '\n')  # Impossible
    s = s.replace('\\\t', '\t')
    s = s.replace('\\\\', '\\')  # Convert first
    return s


# MEASURE WIDTH
def measure_width(s):
    wid = 0
    for c in remove_backslash(s):
        if (c == '\t'):
            wid = (wid + 8) // 8 * 8
            continue
        w = unicodedata.east_asian_width(c)
        if (w == 'F'):    # Full alphabet ...
            wid = wid + 2
        elif(w == 'H'):   # Half katakana ...
            wid = wid + 1
        elif(w == 'W'):   # Chinese character ...
            wid = wid + 2
        elif(w == 'Na'):  # Half alphabet ...
            wid = wid + 1
        elif(w == 'A'):   # Greek character ...
            wid = wid + 1
        elif(w == 'N'):   # Arabic character ...
            wid = wid + 1
    return wid


############################################################
# GET CANDIDATES
############################################################


candidates = sys.stdin.read().splitlines()


############################################################
# MEASURE LONGEST WIDTH
############################################################


longest_width = 0
for i, c in enumerate(candidates):
    if(PYTHON_VERSION == 2):
        w = measure_width(c.decode('utf-8'))
    else:
        w = measure_width(c)
    if(w > longest_width):
        longest_width = w
if(longest_width > TERMINAL_WIDTH - 1):
    longest_width = TERMINAL_WIDTH - 1

number_of_candidates = len(candidates)
number_of_columns = int(TERMINAL_WIDTH / (longest_width + 1))
if(number_of_columns == 0):
    number_of_columns = 1
number_of_lines = int(number_of_candidates / number_of_columns)
if((number_of_candidates % number_of_columns) > 0):
    number_of_lines += 1


############################################################
# MAKE A CANDIDATES ARRAY
############################################################


candidates_array = [['' for _ in range(number_of_columns)]
                    for _ in range(number_of_lines)]
for i, c in enumerate(candidates):
    line = i % number_of_lines
    column = int(i / number_of_lines)
    candidates_array[line][column] = c


############################################################
# PROPARE COLORS
############################################################


color = {'no': '', 'fi': '', 'rs': '', 'di': '', 'ln': '',
         'mh': '', 'pi': '', 'so': '', 'do': '', 'bd': '',
         'cd': '', 'or': '', 'mi': '', 'su': '', 'sg': '',
         'ca': '', 'tw': '', 'ow': '', 'st': '', 'ex': ''}
for i in LIST_COLORS.replace("'", ' ').replace('\t', ' ').split(' '):
    if(i != ''):
        j = i.split('=')
        if(len(j) == 2):
            color[j[0]] = '\033[' + j[1] + 'm'


############################################################
# OUTPUT
############################################################


for i, candidates_column in enumerate(candidates_array):
    for j, c_esc in enumerate(candidates_column):
        if((i > 0) and (j == 0)):
            sys.stdout.write("\n")
        if(c_esc == ''):
            continue
        if(PYTHON_VERSION == 2):
            w = measure_width(c_esc.decode('utf-8'))
        else:
            w = measure_width(c_esc)
        s = longest_width - w + 1
        c = remove_backslash(c_esc)
        c = re.sub('/$', '', c)  # for directory
        if(LIST_COLORS != ''):
            # COLOR
            if(os.path.exists(c)):
                m = os.stat(c).st_mode
            else:
                m = 0
            if(os.path.islink(c)):
                if(os.path.exists(c)):
                    # SYMLINK
                    sys.stdout.write(color['ln'])
                else:
                    # SYMLINK (TO NONEXISTENT FILE)
                    sys.stdout.write(color['or'])
            elif(os.path.isdir(c)):
                if((((m / 512) % 2) == 1) and (((m / 2) % 2) == 1)):
                    # DIRECTORY (STICKY AND OTHER WRITABLE)
                    sys.stdout.write(color['tw'])
                elif(((m / 512) % 2) == 1):
                    # DIRECTORY (STICKY)
                    sys.stdout.write(color['st'])
                elif(((m / 2) % 2) == 1):
                    # DIRECTORY (OTHER WRITABLE)
                    sys.stdout.write(color['ow'])
                elif(os.path.exists(c)):
                    # DIRECTORY
                    sys.stdout.write(color['di'])
                else:
                    # DIRECTORY (NONEXISTENT)
                    sys.stdout.write(color['mi'])
            elif(os.path.isfile(c)):
                if(((m / 2048) % 2) == 1):
                    # FILE (SETUID)
                    sys.stdout.write(color['su'])
                elif(((m / 1024) % 2) == 1):
                    # FILE (SETGID)
                    sys.stdout.write(color['sg'])
                elif((((m / 8**2) % 2) == 1) or
                     (((m / 8**1) % 2) == 1) or
                     (((m / 8**0) % 2) == 1)):
                    # FILE (EXECUTE PERMISSION)
                    sys.stdout.write(color['ex'])
                else:
                    # FILE
                    sys.stdout.write(color['fi'])
            elif((m/4096) == 1):  # stat.S_ISFIFO(m)
                # NAMED PIPE
                sys.stdout.write(color['pi'])
            elif((m/4096) == 2):  # stat.S_ISCHR(m)
                # CHARACTER DEVICE
                sys.stdout.write(color['cd'])
            elif((m/4096) == 6):  # stat.S_ISBLK(m)
                # BLOCK DEVICE
                sys.stdout.write(color['bd'])
            elif((m/4096) == 12):  # stat.S_ISSOCK(m)
                # SOCKET
                sys.stdout.write(color['so'])
            elif((m/4096) == 13):  # stat.S_ISDOOR(m):
                # DOOR
                sys.stdout.write(color['do'])
            elif((c_esc == 'http://') or (c_esc == 'https://')):
                # PLUS
                sys.stdout.write('\033[1;34;43m')
            else:
                # THE OTHERS
                sys.stdout.write('\033[1;30;47;5m')
            sys.stdout.write(c_esc)
            sys.stdout.write('\033[0m')
            sys.stdout.write(' ' * s)
        else:
            # MONOCHROME
            sys.stdout.write(c_esc)
            sys.stdout.write(' ' * s)
sys.stdout.write("\n")

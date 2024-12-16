#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/python/sazae_analyze_buffer.py
# Version:      v20
# Time-stamp:   <2023.01.06-09:31:30-JST>
#
# Copyright (C) 2017-2023  Seiichiro HATA
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
# コマンドライン（バッファ）の内容を受け取り，次を表示します。
#   1 前部分
#   2 補部分（基本 ; migemo ; 閉引用符）
#   3 後部分
#   4 補完のモード（コマンド，オプション，ファイル等）
#   5 補完するファイルの名前の正規表現
#   6 補完するファイルのパーミッション
#   7 追加する補完候補
#
# 例：> ./sazae_analyse_buffer.py 'mv abcd/ef' 'gh ijkl'
#     'mv '
#     'abcd/ ; efgh ; '
#     ' ijkl'
#     'file'
#     ''
#     ''
#     ''
#     'END'
#
# 例：> ./sazae_analyse_buffer.py 'mv "abcd efgh/ij' 'kl'
#     'mv '
#     '"abcd efgh/ ; ijkl ; "'
#     ''
#     'file'
#     ''
#     ''
#     ''
#     'END'
#
# 例：> ./sazae_analyse_buffer.py 'rmdir abcd/ef' 'gh ijkl'
#     'rmidr '
#     'abcd/ ; efgh ; '
#     ' ijkl'
#     'Dire'
#     ''
#     ''
#     ''
#     'END'
#
# 例：> ./sazae_analyse_buffer.py 'xpdf abcd/ef' 'gh ijkl'
#     'xpdf '
#     'abcd/ ; efgh ; '
#     ' ijkl'
#     'File'
#     '^.*\.(p|P)|(d|D)|(f|F)$'
#     ''
#     ''
#     'END'
#
# 例：> ./sazae_analyse_buffer.py 'chmod 750 abcd/ef' 'gh ijkl'
#     'chmod '
#     'abcd/ ; efgh ; '
#     'ijkl'
#     'File'
#     ''
#     '!000111101000'
#     ''
#     'END'
#
# 例：> ./sazae_analyse_buffer.py 'mpg123 abc/de' 'f ghi'
#     'mpg123 '
#     'abcd/ ; efgh ; '
#     'ijkl'
#     'File'
#     '^.*\.(m|M)|(p|P)|3$'
#     ''
#     'http://\\nhttps://'
#     'END'


############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v20'
PYTHON_VERSION = sys.version_info[0]
NOT_ESCAPED = '^((.*[^\\\\])?(\\\\\\\\)*)?'


############################################################
# HELP AND VERSION
############################################################


if(len(sys.argv) == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('Usage: ' + sys.argv[0] + ' [left part] [right part]')
        print('Options:')
        print('  -h, --help            show this message and exit')
        print('  -v, --version         show version number and exit')
        exit(0)
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print(sys.argv[0] + ' ' + VERSION)
        exit(0)


############################################################
# CLASS
############################################################


class Buffer:
    """A class handling a buffer"""

    ########################################
    # CONSTRUCTOR
    ########################################

    def __init__(self, buf_array_in):
        self.buf_array_in = [buf_array_in[1], buf_array_in[2]]
        # [front, command, base, migemo, rear]
        self.buf_array_out = ['', '', '', '', '']
        # [`'"(]
        self.unclosed_signs = ''
        # File, file, Dire, dire, Link, moun,
        # igno, comm, opti, envi, user, lang, arch, norm,
        # _gi1, _gi2
        self.mode = ''
        # *.pdf, *.txt, *.mp3, ...
        self.regexp = ''
        # !sugo(0000-7777)
        self.permission = ''
        # http://, https://, ...
        self.plus = ''

    ########################################
    # ANALYSE
    ########################################

    def analyse_buffer(self):
        _buf_array_in = self._decode_utf8(self.buf_array_in)
        _buf_string = self._add_cursor_marker_and_join(_buf_array_in)
        _buf_array, _unclosed_signs = self._split(_buf_string)
        while(self._is_command_part_unclosed(_unclosed_signs)):
            _buf_array[0] = _buf_array[0] + _buf_array[1]
            _buf_array[1] = ''
            _buf_array \
                = self._extract_command_part(_buf_array, _unclosed_signs)
            _tmp_array, _unclosed_signs = self._split(_buf_array[2])
            _buf_array[0] = _buf_array[0] + _tmp_array[0]
            _buf_array[1] = _tmp_array[1]
            _buf_array[2] = _tmp_array[2]
            # _buf_array[3] = _tmp_array[3]  # This must empty.
            _buf_array[4] = _tmp_array[4]
        _buf_array = self._remove_cursor_marker(_buf_array)
        _buf_array = self._adjust(_buf_array)
        _buf_array = self._get_migemo_key(_buf_array)
        _buf_array = self._encode_utf8(_buf_array)
        self.buf_array_out = _buf_array
        self.unclosed_signs = _unclosed_signs

    def _decode_utf8(self, _array):
        if(PYTHON_VERSION == 2):
            for _i, _ in enumerate(_array):
                _array[_i] = _array[_i].decode('utf-8')
        return _array

    # ['a_b', 'c_d'] -> 'aA_bZ_cA_d'
    def _add_cursor_marker_and_join(self, _buf_array):
        return (_buf_array[0].replace('_', 'A_') +
                'Z_' +
                _buf_array[1].replace('_', 'A_'))

    # 'a ;  b 'c d'Z_e f' -> ['a ;  ', 'b ', ''c d'Z_e', '', ' f']
    # 'a |  b "c d"Z_e<f' -> ['a |  ', 'b ', '"c d"Z_e', '', '<f']
    # 'a || b `c d`Z_e>f' -> ['a || ', 'b ', '`c d`Z_e', '', '>f']
    # 'a && b (c d)Z_e f' -> ['a && ', 'b ', '(c d)Z_e', '', ' f']
    def _split(self, _buf_string):
        # [front, command, base+migemo, , rear]
        _buf_array = ['', '', '', '', '']
        _substring = ''
        _is_in_word = False
        _unclosed_signs = ''
        for _char in _buf_string:
            if(re.match(NOT_ESCAPED + '$', _substring)):
                if(_unclosed_signs == ''):
                    if(re.match('^[\\s\\|&;<>]$', _char) and (_char != '\u3000')):
                        if(_is_in_word):
                            # END OF WORD
                            _buf_array \
                                = self._record_buffer(_buf_array, _substring)
                            _substring = ''
                            _is_in_word = False
                    else:
                        if(not _is_in_word):
                            # BEGGINING OF WORD
                            _buf_array \
                                = self._record_buffer(_buf_array, _substring)
                            _substring = ''
                            _is_in_word = True
                if((_buf_array[2] == '') and re.match('^[\'"`\\(\\)]$', _char)):
                    # BEGGINING OR END OF CHUNK
                    _unclosed_signs \
                        = self._remake_unclosed_signs(_unclosed_signs, _char)
            _substring = _substring + _char
        _buf_array = self._record_buffer(_buf_array, _substring)
        return _buf_array, _unclosed_signs

    def _record_buffer(self, _buf_array, _substring):
        if('Z_' in _substring):
            _buf_array[2] = _substring
        elif(_buf_array[2] == ''):
            _buf_array[1] = _buf_array[1] + _substring
            if(re.match('^\\s*((;)|(\\|\\|?)|(&&))\\s*$', _substring)):
                _buf_array[0] = _buf_array[0] + _buf_array[1]
                _buf_array[1] = ''
        else:
            _buf_array[4] = _buf_array[4] + _substring
        return _buf_array

    #   ' " ` ( )
    # ' \ - - - -
    # " - \ Q - -
    # ` E E \ E E
    # ( Q Q Q \ E
    # ) E E E E \
    def _remake_unclosed_signs(self, _signs, _char):
        _signs = _signs + _char  # _char = ['"`()]
        for _c in _signs:
            if(_c == '\''):
                _signs = re.sub('\'.*\'', '', _signs, 1)
            elif(_c == '"'):
                _signs = re.sub('"[^`]?"', '', _signs, 1)
            elif(_c == '`'):
                _signs = re.sub('``', '', _signs, 1)
            elif(_c == '('):
                _signs = re.sub('\\(\\)', '', _signs, 1)
        return _signs

    def _is_command_part_unclosed(self, _unclosed_signs):
        if(re.match('.*[`(]', _unclosed_signs)):
            return True
        else:
            return False

    # ['a; ', 'b ', 'c`d e', , ' f'] -> ['a; b c`', 'd ', 'e', , ' f']
    # ['a; ', 'b ', 'c(d e', , ' f'] -> ['a; b c(', 'd ', 'e', , ' f']
    def _extract_command_part(self, _buf_array, _unclosed_signs):
        _unclosed_signs_comm_a = re.sub('[\'"]', '', _unclosed_signs)
        _substring = ''
        _unclosed_signs = ''
        for _char in _buf_array[2]:
            _unclosed_signs_comm_b = re.sub('[\'"]', '', _unclosed_signs)
            if(re.match('^[\'"`\\(\\)]$', _char)):
                if(re.match(NOT_ESCAPED + '$', _substring)):
                    _unclosed_signs \
                        = self._remake_unclosed_signs(_unclosed_signs, _char)
            _substring = _substring + _char
            if(_unclosed_signs_comm_b != _unclosed_signs_comm_a):
                _buf_array[0] = _buf_array[0] + _substring
                _substring = ''
        _buf_array[2] = _substring
        return _buf_array

    # ['aA_b', 'cA_d', 'eA_Z_f', '', 'gA_h'] -> ['a_b', 'c_d', 'e_f', , 'g_h']
    def _remove_cursor_marker(self, _buf_array):
        _buf_array[2] = _buf_array[2].replace('Z_', '')
        _buf_array[0] = _buf_array[0].replace('A_', '_')
        _buf_array[1] = _buf_array[1].replace('A_', '_')
        _buf_array[2] = _buf_array[2].replace('A_', '_')
        # _buf_array[3] = _buf_array[3].replace('A_', '_')  # This must empty.
        _buf_array[4] = _buf_array[4].replace('A_', '_')
        return _buf_array

    # [aa,  bb, cc, , dd] -> [aa , bb, cc, , dd]
    # [aa; , then bb, cc, , dd] -> [aa; then , bb, cc, , dd]
    # [aa;, env bb=cc dd, ee, , ff] -> [aa; env bb=cc , dd, ee, , ff]
    # [aa,  bb, cc~, , dd] -> [aa , bb, cc\~, , dd]
    def _adjust(self, _buf_array):
        # SPACE
        _m = re.match('^\\s+', _buf_array[1])
        if(_m):
            _buf_array[0] = _buf_array[0] + _m.group()
            _buf_array[1] = re.sub(_m.group(), '', _buf_array[1], 1)
        # KEY WORDS
        for _w in ['then', 'else', 'do', 'sudo', 'time']:
            _m = re.match('^' + _w + '\\s+', _buf_array[1])
            if(_m):
                _buf_array[0] = _buf_array[0] + _m.group()
                _buf_array[1] = re.sub(_m.group(), '', _buf_array[1], 1)
        # ENV
        _m = re.match('^(env\\s+)?(\\S+=\\S*\\s+)', _buf_array[1])
        if(_m):
            _buf_array[0] = _buf_array[0] + _m.group()
            _buf_array[1] = _buf_array[1].replace(_m.group(), '', 1)
        # TILDE
        _buf_array[2] = re.sub('^((.*[^\\\\])(\\\\\\\\)*)~',
                               '\\1\\~',
                               _buf_array[2])
        return _buf_array

    # [, ~aaa${bbb}$ccc\d-eF0-, , , ] -> [, ~aaa${bbb}$ccc\d-, eF0-, , ]
    def _get_migemo_key(self, _buf_array):
        _buf_array[3] = _buf_array[2]
        # DROP HOME DIRECTORY
        _buf_array[3] = re.sub('^~[a-z][_a-z0-9]*', '', _buf_array[3])
        # DROP BACKSLASHED ALPHABET
        _buf_array[3] = re.sub('^.*\\\\[a-z]', '', _buf_array[3])
        # DROP SHELL VARIABLES AND ENVIRONMENT VARIABLES
        _buf_array[3] = re.sub(NOT_ESCAPED + '\\${?[_a-zA-Z][_a-zA-Z0-9]*',
                               '', _buf_array[3])
        # GET MIGEMO KEY
        _buf_array[3] = re.search('[a-zA-Z0-9\\-]*$', _buf_array[3]).group()
        _buf_array[3] = re.sub('^-*', '', _buf_array[3])
        # DROP MIGEMO KEY
        _buf_array[2] = re.sub(_buf_array[3] + '$', '', _buf_array[2])
        return _buf_array

    def _encode_utf8(self, _array):
        if(PYTHON_VERSION == 2):
            for _i, _ in enumerate(_array):
                _array[_i] = _array[_i].encode('utf-8')
        return _array

    ########################################
    # GET MODE
    ########################################

    def get_mode(self, ):
        _last = self.buf_array_out[1]
        if(re.match('^\\s*$', _last)):
            if(re.match('^[_a-zA-Z][_a-zA-Z0-9]*=', self.buf_array_out[2])):
                # Shell variables and environment variables
                _temp = re.match('^[_a-zA-Z][_a-zA-Z0-9]*=',
                                 self.buf_array_out[2]).group(0)
                self.buf_array_out[1] = self.buf_array_out[1] + _temp
                self.buf_array_out[2] = re.sub(_temp, '',
                                               self.buf_array_out[2])
                if(self.buf_array_out[1] == 'HOME='):
                    # HOME
                    self.mode = 'dire'
                elif(self.buf_array_out[1] == 'PATH='):
                    # PATH
                    self.mode = 'dire'
                elif(self.buf_array_out[1] == 'LANG='):
                    # LANG
                    self.mode = 'lang'
                else:
                    # OTHERS
                    self.mode = 'file'
                if(re.match('^.*:', self.buf_array_out[2])):
                    _temp = re.match('^.*:',
                                     self.buf_array_out[2]).group(0)
                    self.buf_array_out[1] = self.buf_array_out[1] + _temp
                    self.buf_array_out[2] \
                        = self.buf_array_out[2].replace(_temp, '', 1)
            else:
                self.mode = 'comm'
        elif(not re.match('^.*\\s+--\\s+', _last) and
             re.match('^-', self.buf_array_out[2])):
            self.mode = 'opti'
        elif(re.match(NOT_ESCAPED + '\\${?([_a-zA-Z][_a-zA-Z0-9]*)?$',
                      self.buf_array_out[2]) and
             self.buf_array_out[3] == ''):
            self.mode = 'envi'
        elif(re.match('^[^\\(]*\\)\\s*$', _last)):
            # For "case XXX in; X) ..."
            self.mode = 'comm'
        elif(re.match('^.*[<>]\\s*\\S*$', _last)):
            self.mode = 'File'
        elif(re.match('^acroread\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
        elif(re.match('^apt\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^apt-cache\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^apt-get\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^brew\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^bundle\\s+', _last)):
            # RUBY
            if(re.match('^bundle\\s+$', _last)):
                self.mode = 'File'
                self.plus = 'install' \
                    + '\\n'+ 'update' \
                    + '\\n'+ 'cache' \
                    + '\\n'+ 'exec' \
                    + '\\n'+ 'config' \
                    + '\\n'+ 'help' \
                    + '\\n'+ 'add' \
                    + '\\n'+ 'binstubs' \
                    + '\\n'+ 'check' \
                    + '\\n'+ 'clean' \
                    + '\\n'+ 'console' \
                    + '\\n'+ 'doctor' \
                    + '\\n'+ 'gem' \
                    + '\\n'+ 'info' \
                    + '\\n'+ 'init' \
                    + '\\n'+ 'inject' \
                    + '\\n'+ 'list' \
                    + '\\n'+ 'lock' \
                    + '\\n'+ 'open' \
                    + '\\n'+ 'outdated' \
                    + '\\n'+ 'platform' \
                    + '\\n'+ 'plugin' \
                    + '\\n'+ 'pristine' \
                    + '\\n'+ 'remove' \
                    + '\\n'+ 'show' \
                    + '\\n'+ 'version' \
                    + '\\n'+ 'viz'
            else:
                self.mode = 'norm'
        elif(re.match('^bzip2\\s+', _last)):
            self.mode = 'file'
            _opt = '^.*\\s+-(([a-zA-Z0-9]*d[a-zA-Z0-9]*)|(-decompress))\\s+'
            if(re.match(_opt, _last)):
                self.mode = 'File'
                self.regexp = '^.*\\.(b|B)(z|Z)2$'
        elif(re.match('^cd\\s+', _last)):
            self.mode = 'Dire'
        elif(re.match('^chmod\\s+', _last)):
            # GET PERMISSION PART
            _perm = _last
            _perm = re.sub('([\\s,])([-+][rwxXt][\\s,])', '\\1a\\2', _perm)
            _perm = re.sub('^chmod(\\s+-\\S+)*\\s+', '', _perm)
            _perm = re.sub('\\s+.*$', '', _perm)
            if(_perm == ''):
                # NONE
                self.mode = 'igno'
            elif(re.match('^[0-9]*$', _perm)):
                # BY NUMBER
                self.mode = 'File'
                _bin = '000'
                for _char in _perm:
                    _bin = _bin + \
                           str(int(int(_char) / (2**2)) % 2) + \
                           str(int(int(_char) / (2**1)) % 2) + \
                           str(int(int(_char) / (2**0)) % 2)
                _bin = re.sub('^.*(............)$', '\\1', _bin)
                self.permission = '!' + _bin
            else:
                # BY ALPHABET
                self.mode = 'File'
                _perm = re.sub('([^,]*)=', '\\1-rwxst,\\1+', _perm)
                _perm = re.sub('a', '012', _perm)
                _perm = re.sub('u', '0', _perm)
                _perm = re.sub('g', '1', _perm)
                _perm = re.sub('o', '2', _perm)
                _perm = re.sub('r', '0', _perm)
                _perm = re.sub('w', '1', _perm)
                _perm = re.sub('[xX]', '2', _perm)
                _perm = re.sub('s', '3', _perm)
                _perm = re.sub('t', '4', _perm)
                #       r    w    x    s    t
                _p = [['.', '.', '.', '.', '.'],  # u
                      ['.', '.', '.', '.', '.'],  # g
                      ['.', '.', '.', '.', '.']]  # o
                for _str in _perm.split(','):
                    if(re.search('\\+', _str)):
                        _mode = '1'
                    else:
                        _mode = '0'
                    _ugo = re.sub('[-+].*$', '', _str)
                    _rwxst = re.sub('^.*[-+]', '', _str)
                    for _i in _ugo:
                        for _j in _rwxst:
                            _p[int(_i)][int(_j)] = _mode
                        self.permission = '!' + \
                            _p[0][3] + _p[1][3] + _p[2][4] + \
                            _p[0][0] + _p[0][1] + _p[0][2] + \
                            _p[1][0] + _p[1][1] + _p[1][2] + \
                            _p[2][0] + _p[2][1] + _p[2][2]
        elif(re.match('^chown\\s+', _last)):
            _owner = re.sub('^chown', '', _last)
            _owner = re.sub('\\s+-\\S+', '', _owner)
            _owner = re.sub('^\\s+', '', _owner)
            _owner = re.sub('\\s+$', '', _owner)
            if(_owner == ''):
                self.mode = 'user'
            else:
                self.mode = 'File'
        elif(re.match('^dd\\s+', _last)):
            if(re.match('^if=', self.buf_array_out[2])):
                self.mode = 'File'
                self.buf_array_out[1] = self.buf_array_out[1] + 'if='
                self.buf_array_out[2] = re.sub('^if=', '',
                                               self.buf_array_out[2])
            elif(re.match('^of=', self.buf_array_out[2])):
                self.mode = 'file'
                self.buf_array_out[1] = self.buf_array_out[1] + 'of='
                self.buf_array_out[2] = re.sub('^of=', '',
                                               self.buf_array_out[2])
        elif(re.match('^dnf\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^docx2md\\s+', _last)):
            self.mode = 'Flie'
            if(not re.match('^.*\\.docx\\s+$', _last, re.I)):
                self.regexp = '^.*\\.(d|D)(o|O)(c|C)(x|X)$'
        elif(re.match('^docx2pdf\\s+', _last)):
            self.mode = 'Flie'
            if(not re.match('^.*\\.docx\\s+$', _last, re.I)):
                self.regexp = '^.*\\.(d|D)(o|O)(c|C)(x|X)$'
        elif(re.match('^dvipdfmx?\\s+', _last)):
            if(re.match('^.*\\s+-[dgmprsxyzCDIKOPV]\\s+$', _last)):
                self.mode = 'norm'
            elif(re.match('^.*\\s+-o\\s+$', _last)):
                self.mode = 'File'
            elif(re.match('^.*\\s+-f\\s+$', _last)):
                self.mode = 'File'
                self.regexp = '^.*\\.(m|M)(a|A)(p|P)$'
            else:
                self.mode = 'File'
                self.regexp = '^.*\\.(d|D)(v|V)(i|I)$'
        elif(re.match('^dvips\\s+', _last)):
            self.mode = 'File'
            if(not re.match('^.*\\s+-o\\s+$', _last)):
                self.regexp = '^.*\\.(d|D)(v|V)(i|I)$'
        elif(re.match('^env\\s+', _last)):
            if(re.match('^[_a-zA-Z][_a-zA-Z0-9]*=', self.buf_array_out[2])):
                # Shell variables and environment variables
                _temp = re.match('^[_a-zA-Z][_a-zA-Z0-9]*=',
                                 self.buf_array_out[2]).group(0)
                self.buf_array_out[1] = self.buf_array_out[1] + _temp
                self.buf_array_out[2] = re.sub(_temp, '',
                                               self.buf_array_out[2])
                if(_temp == 'HOME='):
                    # HOME
                    self.mode = 'dire'
                elif(_temp == 'PATH='):
                    # PATH
                    self.mode = 'dire'
                elif(_temp == 'LANG='):
                    # LANG
                    self.mode = 'lang'
                else:
                    # OTHERS
                    self.mode = 'file'
                if(re.match('^.*:', self.buf_array_out[2])):
                    _temp = re.match('^.*:',
                                     self.buf_array_out[2]).group(0)
                    self.buf_array_out[1] = self.buf_array_out[1] + _temp
                    self.buf_array_out[2] \
                        = self.buf_array_out[2].replace(_temp, '', 1)
            else:
                self.mode = 'envi'
        elif(re.match('^evince\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(' \
                          + '((p|P)(d|D)(f|F))|' \
                          + '((p|P)(s|S))|' \
                          + '((t|T)(i|I)(f|F)(f|F))|' \
                          + '((d|D)(v|V)(i|I)))$'
        elif(re.match('^export?\\s+', _last)):
            if(re.match('^[_a-zA-Z][_a-zA-Z0-9]*=', self.buf_array_out[2])):
                # Shell variables and environment variables
                _temp = re.match('^[_a-zA-Z][_a-zA-Z0-9]*=',
                                 self.buf_array_out[2]).group(0)
                self.buf_array_out[1] = self.buf_array_out[1] + _temp
                self.buf_array_out[2] = re.sub(_temp, '',
                                               self.buf_array_out[2])
                if(_temp == 'HOME='):
                    # HOME
                    self.mode = 'dire'
                elif(_temp == 'PATH='):
                    # PATH
                    self.mode = 'dire'
                elif(_temp == 'LANG='):
                    # LANG
                    self.mode = 'lang'
                else:
                    # OTHERS
                    self.mode = 'file'
                if(re.match('^.*:', self.buf_array_out[2])):
                    _temp = re.match('^.*:',
                                     self.buf_array_out[2]).group(0)
                    self.buf_array_out[1] = self.buf_array_out[1] + _temp
                    self.buf_array_out[2] \
                        = self.buf_array_out[2].replace(_temp, '', 1)
            else:
                self.mode = 'envi'
        elif(re.match('^gem\\s+', _last)):
            # RUBY
            if(re.match('^gem\\s+$', _last)):
                self.mode = 'File'
                self.plus = 'env' \
                    + '\\n'+ 'help' \
                    + '\\n'+ 'build' \
                    + '\\n'+ 'cert' \
                    + '\\n'+ 'check' \
                    + '\\n'+ 'cleanup' \
                    + '\\n'+ 'contents' \
                    + '\\n'+ 'dependency' \
                    + '\\n'+ 'environment' \
                    + '\\n'+ 'fetch' \
                    + '\\n'+ 'generate_index' \
                    + '\\n'+ 'help' \
                    + '\\n'+ 'install' \
                    + '\\n'+ 'list' \
                    + '\\n'+ 'lock' \
                    + '\\n'+ 'mirror' \
                    + '\\n'+ 'outdated' \
                    + '\\n'+ 'pristine' \
                    + '\\n'+ 'query' \
                    + '\\n'+ 'rdoc' \
                    + '\\n'+ 'search' \
                    + '\\n'+ 'server' \
                    + '\\n'+ 'sources' \
                    + '\\n'+ 'specification' \
                    + '\\n'+ 'uninstall' \
                    + '\\n'+ 'unpack' \
                    + '\\n'+ 'update' \
                    + '\\n'+ 'which'
            else:
                self.mode = 'norm'
        elif(re.match('^git\\s+', _last)):
            if(re.match('^git\\s+add\\s+', _last)):
                self.mode = 'File'
            elif(re.match('^git\\s+((mv)|(rm))\\s+', _last)):
                self.mode = '_gi1'
            elif(re.match('^git\\s+((checkout))\\s+', _last)):
                self.mode = '_gi2'
            else:
                self.mode = 'norm'
        elif(re.match('^growisofs\\s+', _last)):
            self.mode = 'File'
            if (re.match('^/dev/[a-zA-Z0-9]*=', self.buf_array_out[2])):
                _temp = re.match('^/dev/[a-zA-Z0-9]*=',
                                 self.buf_array_out[2]).group(0)
                self.buf_array_out[1] = self.buf_array_out[1] + _temp
                self.buf_array_out[2] \
                    = self.buf_array_out[2].replace(_temp, '', 1)
        elif(re.match('^gzip\\s+', _last)):
            self.mode = 'File'
            _opt = '^.*\\s+-(([a-zA-Z0-9]*d[a-zA-Z0-9]*)|(-decompress))\\s+'
            if(re.match(_opt, _last)):
                self.mode = 'File'
                self.regexp = '^.*\\.(g|G)(z|Z)$'
        elif(re.match('^java\\s+', _last)):
            if(re.match('^.*\\s+-classpath\\s+$', _last)):
                self.mode = 'Dire'
            else:
                self.mode = 'norm'
        elif(re.match('^javac\\s+', _last)):
            self.mode = 'File'
            if(not re.match('^.*\\s+-(d|classpath)\\s+$', _last)):
                self.mode = 'Dire'
                self.regexp = '^.*\\.(j|J)(a|A)(v|V)(a|A)$'
        elif(re.match('^kill\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^killall\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^latex\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(t|T)(e|E)(x|X)$'
        elif(re.match('^(libreoffice)|(soffice)\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(' \
                          + 'odt|Odt|ODT|' \
                          + 'ott|Ott|OTT|' \
                          + 'fodt|Fodt|FODT|' \
                          + 'uot|Uot|UOT|' \
                          + 'docx|Docx|DOCX|' \
                          + 'xml|Xml|XML|' \
                          + 'doc|Doc|DOC|' \
                          + 'dot|Dot|DOT|' \
                          + 'html|Html|HTML|' \
                          + 'rtf|Rtf|RTF|' \
                          + 'txt|Txt|TXT|' \
                          + 'ods|Ods|ODS|' \
                          + 'ots|Ots|OTS|' \
                          + 'fods|Fods|FODS|' \
                          + 'uos|Uos|UOS|' \
                          + 'xlsx|Xlsx|XLSX|' \
                          + 'xls|Xls|XLS|' \
                          + 'xlt|Xlt|XLT|' \
                          + 'dif|Dif|DIF|' \
                          + 'dbf|Dbf|DBF|' \
                          + 'slk|Slk|SLK|' \
                          + 'csv|Csv|CSV|' \
                          + 'xlsm|Xlsm|XLSM|' \
                          + 'odp|Odp|ODP|' \
                          + 'otp|Otp|OTP|' \
                          + 'odg|Odg|ODG|' \
                          + 'fodp|Fodp|FODP|' \
                          + 'uop|Uop|UOP|' \
                          + 'pptx|Pptx|PPTX|' \
                          + 'ppsx|Ppsx|PPSX|' \
                          + 'potm|Potm|POTM|' \
                          + 'ppt|Ppt|PPT|' \
                          + 'pps|Pps|PPS|' \
                          + 'pot|Pot|POT|' \
                          + 'odg|Odg|ODG|' \
                          + 'otg|Otg|OTG|' \
                          + 'fodg|Fodg|FODG|' \
                          + 'odf|Odf|ODF|' \
                          + 'mml|Mml|MML|' \
                          + 'odb|Odb|ODB|' \
                          + ')$'
        elif(re.match('^md2docx\\s+', _last)):
            self.mode = 'Flie'
            if(not re.match('^.*\\.md\\s+$', _last, re.I)):
                self.regexp = '^.*\\.(m|M)(d|D)$'
        elif(re.match('^md2pdf\\s+', _last)):
            self.mode = 'Flie'
            if(not re.match('^.*\\.md\\s+$', _last, re.I)):
                self.regexp = '^.*\\.(m|M)(d|D)$'
        elif(re.match('^mount\\s+', _last)):
            if(re.match('^.*\\s+-o\\s+$', _last)):
                self.mode = 'opti'
            else:
                self.mode = 'File'
        elif(re.match('^mpg123\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(m|M)(p|P)3$'
        elif(re.match('^man\\s+', _last)):
            self.mode = 'comm'
        elif(re.match('^pdffonts\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
        elif(re.match('^pdfinfo\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
        elif(re.match('^pdf2ps\\s+', _last)):
            self.mode = 'Flie'
            if(not re.match('^.*\\.pdf\\s+$', _last, re.I)):
                self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
        elif(re.match('^pdftk\\s+', _last)):
            if (re.match('^[A-Z]+=', self.buf_array_out[2])):
                self.mode = 'File'
                _temp = re.match('^[A-Z]+=',
                                 self.buf_array_out[2]).group(0)
                self.buf_array_out[1] = self.buf_array_out[1] + _temp
                self.buf_array_out[2] \
                    = self.buf_array_out[2].replace(_temp, '', 1)
                self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
            else:
                self.mode = 'File'
                self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
                self.plus = 'input_pw' \
                            + '\\n'+ 'output' \
                            + '\\n'+ 'encrypt_40bit\\nencrypt_128bit' \
                            + '\\n'+ 'allow' \
                            + '\\n'+ 'owner_pw' \
                            + '\\n'+ 'user_pw' \
                            + '\\n'+ 'flatten' \
                            + '\\n'+ 'need_appearances' \
                            + '\\n'+ 'compress\\nuncompress' \
                            + '\\n'+ 'keep_first_id\\nkeep_final_id' \
                            + '\\n'+ 'drop_xfa' \
                            + '\\n'+ 'drop_xmp' \
                            + '\\n'+ 'verbose' \
                            + '\\n'+ 'dont_ask\\ndo_ask' \
                            + '\\n'+ 'cat' \
                            + '\\n'+ 'shuffle' \
                            + '\\n'+ 'burst' \
                            + '\\n'+ 'rotate' \
                            + '\\n'+ 'generate_fdf' \
                            + '\\n'+ 'fill_form' \
                            + '\\n'+ 'background\\nmultibackground' \
                            + '\\n'+ 'stamp\\nmultistamp' \
                            + '\\n'+ 'dump_data\\ndump_data_utf8' \
                            + '\\n'+ 'dump_data_fields\\ndump_data_fields_utf8' \
                            + '\\n'+ 'dump_data_annots' \
                            + '\\n'+ 'update_info\\nupdate_info_utf8' \
                            + '\\n'+ 'attach_files' \
                            + '\\n'+ 'unpack_files' \
                            + '\\n'+ '1-endeast\\n1-endsouth\\n1-endwest' \
                            + '\\n'+ '1-endnorth\\n1-endodd\\n1-endeven'
        elif(re.match('^ping\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^platex\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(t|T)(e|E)(x|X)$'
        elif(re.match('^readlink\\s+', _last)):
            self.mode = 'Link'
        elif(re.match('^rfkill\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^rmdir\\s+', _last)):
            self.mode = 'Dire'
        elif(re.match('^service\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^snap\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^su\\s+', _last)):
            if(re.match('^.*\\s+-c\\s+$', _last)):
                self.mode = 'comm'
            else:
                self.mode = 'user'
        elif(re.match('^tar\\s+', _last)):
            _last = re.sub('^tar', '', _last)
            if(re.match('^\\s+[^-]', _last)):
                _last = re.sub('^\\s+', ' -', _last)
            while(re.match('^.*\\s+-([a-zA-Z0-9])([a-zA-Z0-9]+)\\s+', _last)):
                _last = re.sub('\\s+-([a-zA-Z0-9])([a-zA-Z0-9]+)\\s+',
                               ' -\\1 -\\2 ', _last)
            _last = re.sub('\\s+-(-catenate|-concatenate)\\s+',  ' -A ', _last)
            _last = re.sub('\\s+-(-create)\\s+',                 ' -c ', _last)
            _last = re.sub('\\s+-(-diff|-compare)\\s+',          ' -d ', _last)
            _last = re.sub('\\s+-(-append)\\s+',                 ' -r ', _last)
            _last = re.sub('\\s+-(-list|-test-label)\\s+',       ' -t ', _last)
            _last = re.sub('\\s+-(-update)\\s+',                 ' -u ', _last)
            _last = re.sub('\\s+-(-extract|-get)\\s+',           ' -x ', _last)
            _last = re.sub('\\s+-(-file)\\s+',                   ' -f ', _last)
            _last = re.sub('\\s+-(-compress|-uncompress)\\s+',   ' -Z ', _last)
            _last = re.sub('\\s+-(-gzip|-gunzip|-ungzip)\\s+',   ' -z ', _last)
            _last = re.sub('\\s+-(-bzip2)\\s+',                  ' -j ', _last)
            _last = re.sub('\\s+-(-xz)\\s+',                     ' -J ', _last)
            _last = re.sub('\\s+-(b|-block-size)\\s+\\S+\\s+',        ' ', _last)
            _last = re.sub('\\s+-(C|-directory)\\s+\\S+\\s+',         ' ', _last)
            _last = re.sub('\\s+-(N|-after-date|-newer)\\s+\\S+\\s+', ' ', _last)
            _last = re.sub('\\s+-(V|-label)\\s+\\S+\\s+',             ' ', _last)
            _last = re.sub('\\s+-(X|-exclude-from)\\s+\\S+\\s+',      ' ', _last)
            _temp = _last
            while(re.match('^.*\\s+-\\S+\\s+', _temp)):
                _temp = re.sub('\\s+-\\S+\\s+', ' ', _temp)
            if(re.match('^\\s+$', _last)):
                self.mode = 'opti'
            elif(re.match('^.*\\s+-(A|r|u)\\s+', _last)):
                if(re.match('^\\s+$', _temp) and
                   re.match('^.*\\s+-f\\s+', _last)):
                    self.mode = 'File'
                    self.regexp = '^.*\\.(t|T)(a|A)(r|R)$'
                else:
                    self.mode = 'File'
            elif(re.match('^.*\\s+--delete\\s+', _last)):
                if(re.match('^\\s+$', _temp) and
                   re.match('^.*\\s+-f\\s+', _last)):
                    self.mode = 'File'
                    self.regexp = '^.*\\.(t|T)(a|A)(r|R)$'
                else:
                    self.mode = 'arch'
            elif(re.match('^.*\\s+-(t|x)\\s+', _last)):
                if(re.match('^\\s+$', _temp) and
                   re.match('^.*\\s+-f\\s+', _last)):
                    self.mode = 'File'
                    if(re.match('^.*\\s+-Z\\s+', _last)):
                        self.regexp = '^.*\\.(t|T)(a|A)\\.?(z|Z)$'
                    elif(re.match('^.*\\s+-z\\s+', _last)):
                        self.regexp = '^.*\\.(t|T)((a|A)(r|R)\\.)?(g|G)(z|Z)$'
                    elif(re.match('^.*\\s+-j\\s+', _last)):
                        self.regexp = '^.*\\.(t|T)((a|A)(r|R)\\.)?(b|B)(z|Z)2?$'
                    elif(re.match('^.*\\s+-J\\s+', _last)):
                        self.regexp = '^.*\\.(t|T)((a|A)(r|R)\\.)?(x|X)(z|Z)$'
                    else:
                        self.regexp = '^.*\\.(t|T)(a|A)(r|R)$'
                else:
                    self.mode = 'arch'
            else:
                self.mode = 'file'
        elif(re.match('^umount\\s+', _last)):
            self.mode = 'moun'
        elif(re.match('^unzip\\s+', _last)):
            _last = re.sub('^unzip', '', _last)
            while(re.match('^.*\\s+-([a-zA-Z0-9])([a-zA-Z0-9]+)\\s+', _last)):
                _last = re.sub('\\s+-([a-zA-Z0-9])([a-zA-Z0-9]+)\\s+',
                               ' -\\1 -\\2 ', _last)
            _last = re.sub('\\s+-(I|O|P|d)\\s+\\S+\\s+', ' ', _last)
            _temp = re.sub('^.*\\s+-\\S+\\s+', ' ', _last)
            if(re.match('^\\s+$', _temp)):
                self.mode = 'File'
                if(not re.match('^.*\\s+-d\\s+$', _last)):
                    self.regexp = '^.*\\.(z|Z)(i|I)(p|P)$'
            else:
                self.mode = 'arch'
        elif(re.match('^uplatex\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(t|T)(e|E)(x|X)$'
        elif(re.match('^vmplayer\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(v|V)(m|M)(x|X)$'
        elif(re.match('^where\\s+', _last)):
            self.mode = 'comm'
        elif(re.match('^which\\s+', _last)):
            self.mode = 'comm'
        elif(re.match('^xpdf\\s+', _last)):
            self.mode = 'File'
            self.regexp = '^.*\\.(p|P)(d|D)(f|F)$'
        elif(re.match('^xz\\s+', _last)):
            self.mode = 'File'
            _opt = '^.*\\s+-(([a-zA-Z0-9]*d[a-zA-Z0-9]*)|(-decompress))\\s+'
            if(re.match(_opt, _last)):
                self.mode = 'file'
                self.regexp = '^.*\\.(x|X)(z|Z)$'
        elif(re.match('^yum\\s+', _last)):
            self.mode = 'norm'
        elif(re.match('^zypper\\s+', _last)):
            self.mode = 'norm'
        else:
            self.mode = 'file'

    ########################################
    # OUTPUT
    ########################################

    def output(self):
        # 1. front part + command part
        print(self.buf_array_out[0] +
              self.buf_array_out[1])
        # print(self.buf_array_out[0])
        # print(self.buf_array_out[1])
        # 2. complementation part (base + migemo + quotation)
        print(self.buf_array_out[2] + ' ; ' +
              self.buf_array_out[3] + ' ; ' +
              str(self.unclosed_signs[::-1].encode('utf-8').decode()))
        # 3. rear part
        print(self.buf_array_out[4])
        # 4. mode
        print(self.mode)
        # 5. regexp
        print(self.regexp)
        # 6. permission
        print(self.permission)
        # 7. plus
        print(self.plus)
        # 8. end mark (Without this, blank lines will disappear.)
        print('END')


############################################################
# MAIN


if __name__ == '__main__':
    buf = Buffer(sys.argv)
    buf.analyse_buffer()
    buf.get_mode()
    buf.output()

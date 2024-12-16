# Name:         ~/.zshrc-sazae/zshrc
# Version:      v26
# Time-stamp:   <2023.04.29-09:02:16-JST>
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
# zshのコマンドラインについて，migemoを用いて，
#   ファイル名の補完候補を表示し又は実際に補完します。
#
# migemoを用いるのは，最後のアルファベットと数字の部分です。
#
# 例：'yama'
#     -> '山形県.txt'
#        '山口県.txt'
#        '山梨県.txt'
#
# 例：'*yama'
#     -> '岡山県.txt'
#        '山形県.txt'
#        '山口県.txt'
#        '山梨県.txt'
#        '富山県.txt'
#        '和歌山県.txt'

#==============================================================================#
# 設定（必要があれば修正のこと）

if [ -z "$sazae_migemo_command" ]; then
    if   [ -x /usr/bin/cmigemo ]; then
	if   [ -r /usr/share/cmigemo/utf-8/migemo-dict ]; then
	    sazae_migemo_command='/usr/bin/cmigemo -q -d /usr/share/cmigemo/utf-8/migemo-dict'
	elif [ -r /usr/share/migemo/utf-8/migemo-dict ]; then
	    sazae_migemo_command='/usr/bin/cmigemo -q -d /usr/share/migemo/utf-8/migemo-dict'
	fi
    elif [ -x /usr/local/bin/cmigemo ]; then
	if   [ -r /usr/local/share/cmigemo/utf-8/migemo-dict ]; then
	    sazae_migemo_command='/usr/local/bin/cmigemo -q -d /usr/local/share/cmigemo/utf-8/migemo-dict'
	elif [ -r /usr/local/share/migemo/utf-8/migemo-dict ]; then
	    sazae_migemo_command='/usr/local/bin/cmigemo -q -d /usr/local/share/migemo/utf-8/migemo-dict'
	fi
    elif [ -x /usr/bin/migemo ]; then
	if [ /usr/share/migemo/migemo-dict ]; then
	    sazae_migemo_command='/usr/bin/migemo -t egrep -d /usr/share/migemo/migemo-dict | \nkf -w'
	fi
    elif [ -x /usr/local/bin/migemo ]; then
	if [ /usr/local/share/migemo/migemo-dict ]; then
	    sazae_migemo_command='/usr/local/bin/migemo -t egrep -d /usr/local/share/migemo/migemo-dict | \nkf -w'
	fi
    fi
fi

if [ -z "$sazae_python_command" ]; then
    if   [ -x /usr/bin/python ]; then
	sazae_python_command='/usr/bin/python'
    elif [ -x /usr/local/bin/python ]; then
	sazae_python_command='/usr/local/bin/python'
    elif [ -x /usr/local/bin/python ]; then
	sazae_python_command='/usr/local/bin/python'
    elif [ -x /usr/bin/python3 ]; then
	sazae_python_command='/usr/bin/python3'
    elif [ -x /usr/local/bin/python3 ]; then
	sazae_python_command='/usr/local/bin/python3'
    elif [ -x /usr/bin/python2 ]; then
	sazae_python_command='/usr/bin/python2'
    elif [ -x /usr/local/bin/python2 ]; then
	sazae_python_command='/usr/local/bin/python2'
    fi
fi

sazae (){
    if   [ "$*" = '-h' -o "$*" = '--help' ]; then
	\printf %b 'Usage: sazae [option]\n'
	\printf %b 'Options:\n'
	\printf %b '  -h, --help  show this message and exit\n'
	\printf %b '  -v, --version  show version number and exit\n'
	\printf %b '  -y, --yes   set to use sazae\n'
	\printf %b '  -n, --no    set not to use sazae\n'
    elif [ "$*" = '-v' -o "$*" = '--version' ]; then
	version=`cat ~/.zshrc-sazae/version | cut -d ' ' -f 1`
	\printf %b "sazae $version\n"
    elif [ "$*" = '-y' -o "$*" = '--yes' ]; then
	bindkey '^i'  expand-or-complete-with-migemo
	bindkey '^[i' reverse-menu-complete-with-migemo
	bindkey '^d'  exit-or-list-choices-with-migemo
	bindkey '^[m' sazae_toggle_use_sazae
    elif [ "$*" = '-n' -o "$*" = '--no' ]; then
	bindkey '^i'  "$sazae_original_keybind_ctrl_i"
	bindkey '^[i' "$sazae_original_keybind_esc_i"
	bindkey '^d'  "$sazae_original_keybind_ctrl_d"
	bindkey '^[m' "$sazae_original_keybind_esc_m"
    fi
}

if   [ -z "$sazae_migemo_command" ]; then
    \printf %b 'warning: migemo not found, sazae will not work.\n' > /dev/stderr
    \printf %b '  set the shell variable "sazae_migemo_command" in "~/.zshrc".\n' > /dev/stderr
    \printf %b '  example: sazae_migemo_command="~/bin/cmigemo -q -d ~/cmigemo/migemo-dict"\n' > /dev/stderr
elif [ -z "$sazae_python_command" ]; then
    \printf %b 'warning: python not found, sazae will not work.\n' > /dev/stderr
    \printf %b '  set the shell variable "sazae_python_command" in "~/.zshrc".\n' > /dev/stderr
    \printf %b '  example: sazae_python_command="~/bin/python"\n' > /dev/stderr
elif ( ! eval "printf %s 'a' | $sazae_migemo_command | grep 'あ'" > /dev/null ); then
    \printf %b 'warning: migemo does not work, sazae will not work.\n' > /dev/stderr
    \printf %b "  check \"$sazae_migemo_command\".\n" > /dev/stderr
elif ( ! eval "$sazae_python_command -c 'print(1+2)' | grep '3'" > /dev/null ); then
    \printf %b 'warning: python does not work, sazae will not work.\n' > /dev/stderr
    \printf %b "  check \"$sazae_python_command\".\n" > /dev/stderr
else
    sazae_original_keybind_ctrl_i=`\bindkey | \grep '"\^I"' | \cut -d ' ' -f 2`
    sazae_original_keybind_esc_i=`\bindkey | \grep '"\^\[i"' | \cut -d ' ' -f 2`
    sazae_original_keybind_ctrl_d=`\bindkey | \grep '"\^D"' | \cut -d ' ' -f 2`
    sazae_original_keybind_esc_m=`\bindkey | \grep '"\^\[m"' | \cut -d ' ' -f 2`
    sazae --yes
fi

#==============================================================================#
# 準備

sazae_get_variant_character="$HOME/.zshrc-sazae/python/sazae_get_variant_character.py"
sazae_analyse_buffer="$HOME/.zshrc-sazae/python/sazae_analyse_buffer.py"
sazae_separate_partial_variable="$HOME/.zshrc-sazae/python/sazae_separate_partial_variable.py"
sazae_separate_partial_command="$HOME/.zshrc-sazae/python/sazae_separate_partial_command.py"
sazae_get_grep_style_regexp="$HOME/.zshrc-sazae/python/sazae_get_grep_style_regexp.py"
sazae_check_candidates="$HOME/.zshrc-sazae/python/sazae_check_candidates.py"
sazae_extract_common_part="$HOME/.zshrc-sazae/python/sazae_extract_common_part.py"
sazae_line_up="$HOME/.zshrc-sazae/python/sazae_line_up.py"
sazae__git_decode_utf8="$HOME/.zshrc-sazae/python/sazae__git_decode_utf8.py"

sazae_old_buffer=''
sazae_candidates=''
sazae_number_of_candidates=-1

#==============================================================================#
# メイン

# 使用と不使用
sazae_use_sazae=Y
sazae_toggle_use_sazae (){
    if [ "x$sazae_use_sazae" = 'xY' ]; then
	sazae_use_sazae=N
    else
	sazae_use_sazae=Y
    fi
}
zle -N sazae_toggle_use_sazae

sazae_last_time=0

# 候補表示
list-choices-with-migemo (){
    if [ "x$sazae_use_sazae" = 'xY' ]; then
	sazae_curr_time=`\date +%s`
	if [ "$LASTWIDGET" = 'list-choices-with-migemo' ]; then
	    if [ `\expr $sazae_curr_time - $sazae_last_time` -le 0 ]; then
		return
	    fi
	fi
	sazae_last_time=$sazae_curr_time
	_sazae-main -l
    else
	zle list-choices
    fi
}
zle -N list-choices-with-migemo

# 終了又は候補表示
exit-or-list-choices-with-migemo (){
    \test -z "$BUFFER" && exit
    if [ "x$sazae_use_sazae" = 'xY' ]; then
	sazae_curr_time=`\date +%s`
	if [ "$LASTWIDGET" = 'exit-or-list-choices-with-migemo' ]; then
	    if [ `\expr $sazae_curr_time - $sazae_last_time` -le 0 ]; then
		return
	    fi
	fi
	sazae_last_time=$sazae_curr_time
	_sazae-main -l
    else
	zle list-choices
    fi
}
zle -N exit-or-list-choices-with-migemo

# 順方向補完
expand-or-complete-with-migemo (){
    if [ "x$sazae_use_sazae" = 'xY' ]; then
	if [ "$LASTWIDGET" = 'expand-or-complete-with-migemo' ]; then
	    if [ $sazae_number_of_candidates -eq 0 ]; then
		_sazae-get-variant-character
		return
	    fi
	elif [ "$LASTWIDGET" = 'reverse-menu-complete-with-migemo' ]; then
	    if [ $sazae_number_of_candidates -eq 0 ]; then
		_sazae-get-variant-character
		return
	    fi
	fi
	_sazae-main -c
    else
	zle expand-or-complete
    fi
}
zle -N expand-or-complete-with-migemo

# 逆方向補完
reverse-menu-complete-with-migemo (){
    if [ "x$sazae_use_sazae" = 'xY' ]; then
	if [ "$LASTWIDGET" = 'expand-or-complete-with-migemo' ]; then
	    if [ $sazae_number_of_candidates -eq 0 ]; then
		_sazae-get-variant-character -r
		return
	    fi
	elif [ "$LASTWIDGET" = 'reverse-menu-complete-with-migemo' ]; then
	    if [ $sazae_number_of_candidates -eq 0 ]; then
		_sazae-get-variant-character -r
		return
	    fi
	fi
	_sazae-main -r
    else
	zle reverse-menu-complete
    fi
}
zle -N reverse-menu-complete-with-migemo

_sazae-get-variant-character (){
    sazae_old_lbuffer=`\printf %s "$LBUFFER" | \sed 's/%/-%/g' | \sed 's/@/+%/g' | \tr '\n' '@'`
    sazae_new_lbuffer=`$sazae_python_command $sazae_get_variant_character $@ "$sazae_old_lbuffer"`
    LBUFFER=`\printf %s "$sazae_new_lbuffer" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'`
    _sazae-set-buffer "$LBUFFER" "$RBUFFER"
}

_sazae-main (){
    # ビープ音の設定を保存
    if ( setopt | \grep nobeep > /dev/null ); then
	sazae_nobeep='Y'
    else
	sazae_nobeep='N'
    fi
    setopt nobeep
    # コア
    _sazae-main-core $@
    # ビープ音の設定を戻す
    if [ "$sazae_nobeep" = 'Y' ]; then
	setopt nobeep
    else
	unsetopt nobeep
    fi
}

_sazae-main-core (){
    # 旧コマンドラインの分解
    if   [ "x$*" != 'x-l' \
	-a "$LASTWIDGET" = 'expand-or-complete-with-migemo' \
	-a $sazae_number_of_candidates -gt 1 ]; then
	:
    elif [ "x$*" != 'x-l' \
	-a "$LASTWIDGET" = 'reverse-menu-complete-with-migemo' \
	-a $sazae_number_of_candidates -gt 1 ]; then
	:
    else
	sazae_old_lbuffer=`\printf %s "$LBUFFER" | \sed 's/%/-%/g' | \sed 's/@/+%/g' | \tr '\n' '@'`
	sazae_old_rbuffer=`\printf %s "$RBUFFER" | \sed 's/%/-%/g' | \sed 's/@/+%/g' | \tr '\n' '@'`
	sazae_old_buffer=`$sazae_python_command $sazae_analyse_buffer "$sazae_old_lbuffer" "$sazae_old_rbuffer"`
	unset sazae_old_lbuffer sazae_old_rbuffer
	#sazae_old_buffer=`$sazae_python_command $sazae_analyse_buffer "$LBUFFER" "$RBUFFER"`
	sazae_old_buffer_A=`\printf %s "$sazae_old_buffer" | \head -n 1 | \tail -n 1` # 前部分
	sazae_old_buffer_Q=`\printf %s "$sazae_old_buffer" | \head -n 2 | \tail -n 1`
	sazae_old_buffer_B=`\printf %s "$sazae_old_buffer_Q" | sed 's/\(.*\) ; \(.*\) ; \(.*\)/\1/'` # 補完基本部分
	sazae_old_buffer_M=`\printf %s "$sazae_old_buffer_Q" | sed 's/\(.*\) ; \(.*\) ; \(.*\)/\2/'` # 補完migemo部分
	sazae_old_buffer_Q=`\printf %s "$sazae_old_buffer_Q" | sed 's/\(.*\) ; \(.*\) ; \(.*\)/\3/'` # 補完閉引用符部分
	sazae_old_buffer_C=`\printf %s "$sazae_old_buffer" | \head -n 3 | \tail -n 1` # 後部分
	sazae_mode=`\printf %s "$sazae_old_buffer" | \head -n 4 | \tail -n 1`
	sazae_regexp=`\printf %s "$sazae_old_buffer" | \head -n 5 | \tail -n 1`
	sazae_permission=`\printf %s "$sazae_old_buffer" | \head -n 6 | \tail -n 1`
	sazae_plus=`\printf %s "$sazae_old_buffer" | \head -n 7 | \tail -n 1`
	sazae_new_buffer_A=`\printf %s "$sazae_old_buffer_A" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'` # 前部分
	sazae_new_buffer_B=`\printf %s "$sazae_old_buffer_B" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'` # 補完基本部分
	sazae_new_buffer_M=`\printf %s "$sazae_old_buffer_M" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'` # 補完migemo部分
	sazae_new_buffer_Q=`\printf %s "$sazae_old_buffer_Q" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'` # 補完閉引用符部分
	sazae_new_buffer_C=`\printf %s "$sazae_old_buffer_C" | \tr '@' '\n' | \sed 's/+%/@/g' | \sed 's/-%/%/g'` # 後部分
	#sazae_new_buffer_A=$sazae_old_buffer_A # 前部分
	#sazae_new_buffer_B=$sazae_old_buffer_B # 補完基本部分
	#sazae_new_buffer_M=$sazae_old_buffer_M # 補完migemo部分
	#sazae_new_buffer_Q=$sazae_old_buffer_Q # 補完閉引用符部分
	#sazae_new_buffer_C=$sazae_old_buffer_C # 後部分
	sazae_number_of_candidates=-1
	unset sazae_old_buffer   sazae_old_buffer_A sazae_old_buffer_C # おかしなPROMPT防止
	unset sazae_old_buffer_B sazae_old_buffer_M sazae_old_buffer_Q # おかしなPROMPT防止
    fi
    # 補完しない
    if [ "$sazae_mode" = 'igno' ]; then
	return
    fi
    # コマンドの補完
    if [ "$sazae_mode" = 'comm' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # オプションの補完
    if [ "$sazae_mode" = 'opti' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # シェル変数と環境変数の補完
    if [ "$sazae_mode" = 'envi' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # ユーザーの補完
    if [ "$sazae_mode" = 'user' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # 言語の補完
    if [ "$sazae_mode" = 'lang' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # アーカイブの補完
    if [ "$sazae_mode" = 'arch' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # その他の標準の補完
    if [ "$sazae_mode" = 'norm' ]; then
	if   [ "x$*" = 'x-l' ]; then
	    zle list-choices
	elif [ "x$*" = 'x-c' ]; then
	    zle expand-or-complete
	else
	    zle reverse-menu-complete
	fi
	return
    fi
    # 末尾が「\」ならば何もしない
    \printf %s "$sazae_new_buffer_B" | \grep -E '^((.*[^\\])?(\\\\)*)?\\$' > /dev/null && return
    # ファイルの補完
    if [ $sazae_number_of_candidates -eq -1 ]; then
	\cd . 2> /dev/null
	# ホームディレクトリの展開
	if ( \printf %s "$sazae_new_buffer_B" | \grep -E '^~' > /dev/null ); then
	    sazae_new_buffer_B=`_sazae-expand-tilde "$sazae_new_buffer_B"`
	fi
	# シェル変数・環境変数の展開
	if   ( \printf %s "$sazae_new_buffer_B" | \grep -E '\$[_a-zA-Z][_a-zA-Z0-9]*' > /dev/null ); then
	    sazae_new_buffer_B=`_sazae-expand-partial-variable "$sazae_new_buffer_B"`
	elif ( \printf %s "$sazae_new_buffer_B" | \grep -E '\${[_a-zA-Z][_a-zA-Z0-9]*}' > /dev/null ); then
	    sazae_new_buffer_B=`_sazae-expand-partial-variable "$sazae_new_buffer_B"`
	fi
	# 部分コマンドの実行
	if ( \printf %s "$sazae_new_buffer_B" | \grep -E '((`)|(\$\())' > /dev/null ); then
	    sazae_new_buffer_B=`_sazae-execute-partial-command "$sazae_new_buffer_B"`
	fi
	# 展開と補完
	sazae_new_buffer_I=''
	sazae_new_buffer_J=''
	# bug?
	if ( \printf %s "=$sazae_new_buffer_B=" | \grep -E '^=(.*)\s(.*)=$' > /dev/null ); then
	    sazae_new_buffer_I=`printf %s "=$sazae_new_buffer_B=" | sed 's;^=\(.*\s\)\(.*\)=$;\1;'`
	    sazae_new_buffer_J=`printf %s "=$sazae_new_buffer_B=" | sed 's;^=\(.*\s\)\(.*\)=$;\2;'`
	fi
	#if ( \printf %s "$sazae_new_buffer_B" | \grep -E '^(.*)\s(.*)$' > /dev/null ); then
	#    sazae_new_buffer_I=`printf %s "$sazae_new_buffer_B" | sed 's;^\(.*\s\)\(.*\)$;\1;'`
	#    sazae_new_buffer_J=`printf %s "$sazae_new_buffer_B" | sed 's;^\(.*\s\)\(.*\)$;\2;'`
	#fi
	if [ ! -z "$sazae_new_buffer_B$sazae_new_buffer_Q$sazae_new_buffer_M" ]; then
	    # 全体の展開
	    sazae_candidates=`_sazae-expand "$sazae_new_buffer_B$sazae_new_buffer_Q$sazae_new_buffer_M"`
	    sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	    if [ "$sazae_number_of_candidates" -ge 2 ]; then
		if [ "x$*" = 'x-l' ]; then
		    _sazae-print-candidates "$sazae_candidates"
		    return
		else
		    sazae_candidate=`\printf %s%b "$sazae_candidates" '\n' | tr '\n' ' '`
		    sazae_new_buffer_L="$sazae_new_buffer_A$sazae_candidate"
		    sazae_new_buffer_R="$sazae_new_buffer_C"
		    unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		    unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		    unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		    unset sazae_candidates                                         # おかしなPROMPT防止
		    unset sazae_candidate                                          # おかしなPROMPT防止
		    _sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		    unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		    sazae_number_of_candidates=1
		fi
		return
	    fi
	    # 空白後の展開
	    if [ ! -z "$sazae_new_buffer_I$sazae_new_buffer_J" ]; then
		sazae_candidates=`_sazae-expand "$sazae_new_buffer_J$sazae_new_buffer_M"`
		sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	    fi
	    if [ "$sazae_number_of_candidates" -ge 2 ]; then
		sazae_new_buffer_A="$sazae_new_buffer_A$sazae_new_buffer_I"
		if [ "x$*" = 'x-l' ]; then
		    _sazae-print-candidates "$sazae_candidates"
		    return
		else
		    sazae_candidate=`\printf %s%b "$sazae_candidates" '\n' | tr '\n' ' '`
		    sazae_new_buffer_L="$sazae_new_buffer_A$sazae_candidate"
		    sazae_new_buffer_R="$sazae_new_buffer_C"
		    unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		    unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		    unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		    unset sazae_candidates                                         # おかしなPROMPT防止
		    unset sazae_candidate                                          # おかしなPROMPT防止
		    _sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		    unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		    sazae_number_of_candidates=1
		fi
		return
	    fi
	fi
	# 全体の補完候補の作成
	sazae_candidates=`_sazae-get-candidates "$sazae_new_buffer_B$sazae_new_buffer_Q" "$sazae_new_buffer_M"`
	sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	if [ -z "$sazae_candidates" ]; then
	    # "/u/s/e"で"/usr/share/emacs"の補完を試みる
	    sazae_tmp_buffer_BQ=`printf %s "$sazae_new_buffer_B$sazae_new_buffer_Q" | sed "s;\([^/]\)/;\1\*/;g"`
	    sazae_candidates=`_sazae-get-candidates "$sazae_tmp_buffer_BQ" "$sazae_new_buffer_M"`
	    sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	    unset sazae_tmp_buffer_BQ
	fi
	if [ ! -z "$sazae_candidates" ]; then
	    if [ "x$*" = 'x-l' ]; then
		_sazae-print-candidates "$sazae_candidates"
		return
	    elif [ $sazae_number_of_candidates -eq 1 ]; then
		# 補完候補が単数の場合
		sazae_new_buffer_L="$sazae_new_buffer_A$sazae_candidates"
		sazae_new_buffer_R="$sazae_new_buffer_C"
		if ( \printf %s "$sazae_candidates" | \grep -v -E '/$' > /dev/null ); then
		    # ディレクトリでない場合
		    sazae_new_buffer_L="$sazae_new_buffer_L "
		fi
		unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		unset sazae_candidates                                         # おかしなPROMPT防止
		#unset sazae_candidate                                          # おかしなPROMPT防止
		_sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		return
	    else
		# 補完候補が複数の場合
		sazae_common_parts=`\printf %b "$sazae_candidates" \
		    | $sazae_python_command $sazae_extract_common_part 2> /dev/null`
		test -z "$sazae_common_parts" && sazae_common_parts='---' # 補完候補の共通部分が空の場合
		sazae_new_buffer_L="$sazae_new_buffer_A$sazae_common_parts"
		sazae_new_buffer_R="$sazae_new_buffer_C"
		#unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		#unset sazae_candidates                                         # おかしなPROMPT防止
		#unset sazae_candidate                                          # おかしなPROMPT防止
		unset sazae_common_parts                                       # おかしなPROMPT防止
		_sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		sazae_candidate_number=0
		return
	    fi
	fi
	# 空白後の補完候補の作成
	if [ ! -z "$sazae_new_buffer_I$sazae_new_buffer_J" ]; then
	    sazae_candidates=`_sazae-get-candidates "$sazae_new_buffer_J" "$sazae_new_buffer_M"`
	    sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	    if [ -z "$sazae_candidates" ]; then
	    # "/u/s/e"で"/usr/share/emacs"の補完を試みる
	    sazae_tmp_buffer_J=`\printf %s "$sazae_new_buffer_J" | sed "s;\([^/]\)/;\1\*/;g"`
	    sazae_candidates=`_sazae-get-candidates "$sazae_tmp_buffer_J" "$sazae_new_buffer_M"`
	    sazae_number_of_candidates=`\printf %s%b "$sazae_candidates" '\n' | wc -l`
	    unset sazae_tmp_buffer_J
	    fi
	fi
	if [ ! -z "$sazae_candidates" ]; then
	    sazae_new_buffer_A="$sazae_new_buffer_A$sazae_new_buffer_I"
	    if [ "x$*" = 'x-l' ]; then
		_sazae-print-candidates "$sazae_candidates"
		return
	    elif [ $sazae_number_of_candidates -eq 1 ]; then
		# 補完候補が単数の場合
		sazae_new_buffer_L="$sazae_new_buffer_A$sazae_candidates"
		sazae_new_buffer_R="$sazae_new_buffer_C"
		if ( \printf %s "$sazae_candidates" | \grep -v -E '/$' > /dev/null ); then
		    # ディレクトリでない場合
		    sazae_new_buffer_L="$sazae_new_buffer_L "
		fi
		unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		unset sazae_candidates                                         # おかしなPROMPT防止
		#unset sazae_candidate                                          # おかしなPROMPT防止
		_sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		return
	    else
		# 補完候補が複数の場合
		sazae_common_parts=`\printf %b "$sazae_candidates" \
		    | $sazae_python_command $sazae_extract_common_part 2> /dev/null`
		test -z "$sazae_common_parts" && sazae_common_parts='---' # 補完候補の共通部分が空の場合
		sazae_new_buffer_L="$sazae_new_buffer_A$sazae_common_parts"
		sazae_new_buffer_R="$sazae_new_buffer_C"
		#unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
		unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
		unset sazae_new_buffer_I sazae_new_buffer_J                    # おかしなPROMPT防止
		#unset sazae_candidates                                         # おかしなPROMPT防止
		#unset sazae_candidate                                          # おかしなPROMPT防止
		unset sazae_common_parts                                       # おかしなPROMPT防止
		_sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_R"
		unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
		sazae_candidate_number=0
		return
	    fi
	fi
	# 展開も補完も失敗
	sazae_number_of_candidates=0
	\test "$sazae_nobeep" = 'N' && \printf %b '\a'
	return
    else
	# 補完候補の表示
	if [ "x$*" = 'x-c' ]; then
	    # 順方向補完
	    sazae_candidate_number=`\expr $sazae_candidate_number + 1`
	    \test $sazae_candidate_number -gt $sazae_number_of_candidates && sazae_candidate_number=1
	else
	    # 逆方向補完
	    sazae_candidate_number=`\expr $sazae_candidate_number - 1`
	    \test $sazae_candidate_number -lt 1 && sazae_candidate_number=$sazae_number_of_candidates
	fi
	sazae_candidate=`\printf %s%b "$sazae_candidates" '\n' | \head -n $sazae_candidate_number | \tail -n 1`
	sazae_new_buffer_L="$sazae_new_buffer_A$sazae_candidate"
	sazae_new_buffer_R="$sazae_new_buffer_C"
	#unset sazae_new_buffer_A sazae_new_buffer_C                    # おかしなPROMPT防止
	#unset sazae_new_buffer_B sazae_new_buffer_M sazae_new_buffer_Q # おかしなPROMPT防止
	#unset sazae_candidates                                         # おかしなPROMPT防止
	unset sazae_candidate                                          # おかしなPROMPT防止
	_sazae-set-buffer "$sazae_new_buffer_L" "$sazae_new_buffer_C"
	unset sazae_new_buffer_L sazae_new_buffer_R                    # おかしなPROMPT防止
	return
    fi
}

#==============================================================================#
# 関数

# ホームディレクトリの展開
_sazae-expand-tilde (){
    local user
    local home
    local left
    user=`\printf %s "$*" | \sed 's;^~;;' | \sed 's;^\([_a-z][_0-9a-z]*\)\?.*$;\1;'`
    if [ -z "$user" -a ! -z "$HOME" ]; then
	home=$HOME
    else
	\test -z "$user" && user=`whoami`
	home=`\cat /etc/passwd | \grep -E "^$user:" | \cut -d ':' -f 6`
    fi
    if [ -z "$home" ]; then
	\printf %s "$*"
    else
	left=`\printf %s "$*" | \sed 's;^~;;' | \sed "s;^$user;;"`
	\printf %s "$home$left" | \sed 's;/\+$;/;'
    fi
}

# 部分変数の展開
_sazae-expand-partial-variable (){
    local base
    local i
    local j
    base=''
    j=0
    $sazae_python_command $sazae_separate_partial_variable "$*" \
	| while read i; do
	\test `\expr $j % 2` -eq 1 && i=`eval "\printf %s \"$i\" 2> /dev/null" 2> /dev/null`
	base="$base$i"
	j=`\expr $j + 1`
    done
    \printf %s "$base"
}

# 部分コマンドの実行
_sazae-execute-partial-command (){
    local base
    local i
    local j
    base=''
    j=0
    $sazae_python_command $sazae_separate_partial_command "$*" \
	| while read i; do
	\test `\expr $j % 2` -eq 1 && i=`eval "\printf %s \"$i\" 2> /dev/null" 2> /dev/null`
	base="$base$i"
	j=`\expr $j + 1`
    done
    \printf %s "$base"
}

# 展開
_sazae-expand (){
    local n; setopt | \grep '^nonomatch$' > /dev/null && n='Y' || n='N'; setopt nonomatch
    eval "/bin/ls -d -- $* 2> /dev/null" 2> /dev/null \
	| $sazae_python_command $sazae_check_candidates -d "$PWD" \
				"$sazae_mode" "$sazae_regexp" "$sazae_permission" 2> /dev/null
    \test "$n" = 'N' && unsetopt nonomatch
}

# 候補を作成
_sazae-get-candidates (){
    local b; b=$1
    b=`\printf %s "$b" | \sed 's;/\+;/;g'`
    local g; g=`$sazae_python_command $sazae_get_grep_style_regexp "$b"`
    local m; m=$2
    local r; r=`eval "\printf %s \"$2\" 2> /dev/null | $sazae_migemo_command"`
    r="$m|$r"
    if [ ! -z "$sazae_plus" ]; then
	if [ ! -z "$g$m" ]; then
	    \printf %s "$sazae_plus" | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null
	fi
    fi
    if [ "$sazae_mode" = 'moun' -a -r /etc/mtab ]; then
	# 漢字名のディレクトリにマウントされている可能性があるので，migemo補完にする必要性がある
	if ( \printf %s "$g" | \grep '^/' > /dev/null ); then
	    # 絶対パス
	    \cat /etc/mtab | \cut -d ' ' -f 2 | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null \
		| $sazae_python_command $sazae_check_candidates -d "$PWD" \
					"$sazae_mode" "$sazae_regexp" "$sazae_permission" 2> /dev/null
	else
	    # 相対パス
	    local p; p="`\pwd`"
	    \cat /etc/mtab | \cut -d ' ' -f 2 | eval "\grep -a -E \"^$p/$g($r)\"" 2> /dev/null \
		| $sazae_python_command $sazae_check_candidates -d "$PWD" \
					"$sazae_mode" "$sazae_regexp" "$sazae_permission" 2> /dev/null \
		| \grep -a -E "^$p/.+" | sed "s;^$p/;;"
	fi
    elif [ "$sazae_mode" = '_gi1' -a "`\git --version 2> /dev/null`" != '' ]; then
	# GIT (files)
	local n; n=`\printf %s $g | \sed 's;[^/];;g' | wc -c`
	\git ls-files 2> /dev/null | $sazae_python_command $sazae__git_decode_utf8 \
	    | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null \
	    | \sed "s;^\([^/]*\(/\+[^/]\+\)\{$n\}/*\).*;\1;" \
	    | \uniq
    elif [ "$sazae_mode" = '_gi2' -a "`\git --version 2> /dev/null`" != '' ]; then
	# GIT (branches and files)
	\printf %s%b 'HEAD' '\n' \
	    | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null
	\git branch --list | sed 's;\*\? *;;' \
	    | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null
	local n; n=`\printf %s $g | \sed 's;[^/];;g' | wc -c`
	\git ls-files 2> /dev/null | $sazae_python_command $sazae__git_decode_utf8 \
	    | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null \
	    | \sed "s;^\([^/]*\(/\+[^/]\+\)\{$n\}/*\).*;\1;" \
	    | \uniq
    else
	local n; setopt | \grep '^nonomatch$' > /dev/null && n='Y' || n='N'; setopt nonomatch
	eval "/bin/ls -d -- $b* 2> /dev/null" 2> /dev/null | eval "\grep -a -E \"^$g($r)\"" 2> /dev/null \
	    | $sazae_python_command $sazae_check_candidates  -d "$PWD" \
				    "$sazae_mode" "$sazae_regexp" "$sazae_permission" 2> /dev/null
	\test "$n" = 'N' && unsetopt nonomatch
    fi
}

# 補完候補を表示
_sazae-print-candidates (){
    \printf %b '\n'
    local i
    local c; c=''
    if ( zstyle | \grep 'list-colors' > /dev/null ); then
	zstyle | while read i; do
	    if [ "$c" = 'list-colors' ]; then
		c=`\printf %s "$i" | \sed 's;^\s*\S\+\s\+;;'`
		break
	    fi
	    c="$i"
	done
    fi
    #c=`zstyle | \grep -A 1 'list-colors' | \tail -n 1| sed 's;^\s*\S\+\s\+;;'`
    local h; h=`expr $LINES - 1`
    \test $h -eq 0 && return
    trap "print -Pn \"$prompt\"; zle redisplay; return" INT TERM
    local j; j=0
    \printf %s%b "$sazae_candidates" '\n' \
	| $sazae_python_command $sazae_line_up -w $COLUMNS -c "$c" 2> /dev/null \
	| while read i; do
	\printf %s%b "$i" '\n'
	j=`expr $j + 1`; j=`expr $j % $h`
	if [ $j -eq 0 ]; then \printf %s ':'; read -s -k 1; fi
	\printf %b '\r'
    done
    print -Pn "$prompt"
    zle redisplay
}

# コマンドラインを表示
_sazae-set-buffer (){
    BUFFER="$1$2"
    CURSOR=$#1
}

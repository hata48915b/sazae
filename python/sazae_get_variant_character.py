#!/usr/bin/python
# coding: utf-8
#
# Name:         ~/.zshrc-sazae/python/sazae_get_variant_character.py
# Version:      v01
# Time-stamp:   <2023.04.22-09:54:44-JST>
#
# Copyright (C) 2023  Seiichiro HATA
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
# 最終の文字を異字体に変えます。
#
# 例：> ./sazae_get_variant_character.py 'echo 1'
#     echo ⑴

############################################################
# IMPORT
############################################################


import sys
import re


############################################################
# CONSTANT
############################################################


VERSION = 'v01'

CHAR_LISTS = [
    # NUMBER
    ['10', '⑽', '⑩', '⒑', 'Ⅹ', 'ⅹ'],
    ['11', '⑾', '⑪', '⒒', 'Ⅺ', 'ⅺ'],
    ['12', '⑿', '⑫', '⒓', 'Ⅻ', 'ⅻ'],
    ['13', '⒀', '⑬', '⒔'],
    ['14', '⒁', '⑭', '⒕'],
    ['15', '⒂', '⑮', '⒖'],
    ['16', '⒃', '⑯', '⒗'],
    ['17', '⒄', '⑰', '⒘'],
    ['18', '⒅', '⑱', '⒙'],
    ['19', '⒆', '⑲', '⒚'],
    ['20', '⒇', '⑳', '⒛'],
    ['21', '㉑'],
    ['22', '㉒'],
    ['23', '㉓'],
    ['24', '㉔'],
    ['25', '㉕'],
    ['26', '㉖'],
    ['27', '㉗'],
    ['28', '㉘'],
    ['29', '㉙'],
    ['30', '㉚'],
    ['31', '㉛'],
    ['32', '㉜'],
    ['33', '㉝'],
    ['34', '㉞'],
    ['35', '㉟'],
    ['36', '㊱'],
    ['37', '㊲'],
    ['38', '㊳'],
    ['39', '㊴'],
    ['40', '㊵'],
    ['41', '㊶'],
    ['42', '㊷'],
    ['43', '㊸'],
    ['44', '㊹'],
    ['45', '㊺'],
    ['46', '㊻'],
    ['47', '㊼'],
    ['48', '㊽'],
    ['49', '㊾'],
    ['50', '㊿'],
    ['0', '⓪', '⁰'],
    ['1', '⑴', '①', '⒈', 'Ⅰ', 'ⅰ'],
    ['2', '⑵', '②', '⒉', 'Ⅱ', 'ⅱ', '²'],
    ['3', '⑶', '③', '⒊', 'Ⅲ', 'ⅲ', '³'],
    ['4', '⑷', '④', '⒋', 'Ⅳ', 'ⅳ', '⁴'],
    ['5', '⑸', '⑤', '⒌', 'Ⅴ', 'ⅴ', '⁵'],
    ['6', '⑹', '⑥', '⒍', 'Ⅵ', 'ⅵ', '⁶'],
    ['7', '⑺', '⑦', '⒎', 'Ⅶ', 'ⅶ', '⁷'],
    ['8', '⑻', '⑧', '⒏', 'Ⅷ', 'ⅷ', '⁸'],
    ['9', '⑼', '⑨', '⒐', 'Ⅸ', 'ⅸ', '⁹'],
    # ALPHABET
    ['A', '🄐', 'Ⓐ'],
    ['B', '🄑', 'Ⓑ'],
    ['C', '🄒', 'Ⓒ'],
    ['D', '🄓', 'Ⓓ'],
    ['E', '🄔', 'Ⓔ'],
    ['F', '🄕', 'Ⓕ'],
    ['G', '🄖', 'Ⓖ'],
    ['H', '🄗', 'Ⓗ'],
    ['I', '🄘', 'Ⓘ'],
    ['J', '🄙', 'Ⓙ'],
    ['K', '🄚', 'Ⓚ'],
    ['L', '🄛', 'Ⓛ'],
    ['M', '🄜', 'Ⓜ'],
    ['N', '🄝', 'Ⓝ'],
    ['O', '🄞', 'Ⓞ'],
    ['P', '🄟', 'Ⓟ'],
    ['Q', '🄠', 'Ⓠ'],
    ['R', '🄡', 'Ⓡ'],
    ['S', '🄢', 'Ⓢ'],
    ['T', '🄣', 'Ⓣ'],
    ['U', '🄤', 'Ⓤ'],
    ['V', '🄥', 'Ⓥ'],
    ['W', '🄦', 'Ⓦ'],
    ['X', '🄧', 'Ⓧ'],
    ['Y', '🄨', 'Ⓨ'],
    ['Z', '🄩', 'Ⓩ'],
    ['a', '⒜', 'ⓐ'],
    ['b', '⒝', 'ⓑ'],
    ['c', '⒞', 'ⓒ'],
    ['d', '⒟', 'ⓓ'],
    ['e', '⒠', 'ⓔ'],
    ['f', '⒡', 'ⓕ'],
    ['g', '⒢', 'ⓖ'],
    ['h', '⒣', 'ⓗ'],
    ['i', '⒤', 'ⓘ'],
    ['j', '⒥', 'ⓙ'],
    ['k', '⒦', 'ⓚ'],
    ['l', '⒧', 'ⓛ'],
    ['m', '⒨', 'ⓜ'],
    ['n', '⒩', 'ⓝ', 'ⁿ'],
    ['o', '⒪', 'ⓞ'],
    ['p', '⒫', 'ⓟ'],
    ['q', '⒬', 'ⓠ'],
    ['r', '⒭', 'ⓡ'],
    ['s', '⒮', 'ⓢ'],
    ['t', '⒯', 'ⓣ'],
    ['u', '⒰', 'ⓤ'],
    ['v', '⒱', 'ⓥ'],
    ['w', '⒲', 'ⓦ'],
    ['x', '⒳', 'ⓧ'],
    ['y', '⒴', 'ⓨ'],
    ['z', '⒵', 'ⓩ'],
    # KATAKANA
    ['ア', 'ｱ', '㋐'],
    ['イ', 'ｲ', '㋑'],
    ['ウ', 'ｳ', '㋒'],
    ['エ', 'ｴ', '㋓'],
    ['オ', 'ｵ', '㋔'],
    ['カ', 'ｶ', '㋕'],
    ['キ', 'ｷ', '㋖'],
    ['ク', 'ｸ', '㋗'],
    ['ケ', 'ｹ', '㋘'],
    ['コ', 'ｺ', '㋙'],
    ['サ', 'ｻ', '㋚'],
    ['シ', 'ｼ', '㋛'],
    ['ス', 'ｽ', '㋜'],
    ['セ', 'ｾ', '㋝'],
    ['ソ', 'ｿ', '㋞'],
    ['タ', 'ﾀ', '㋟'],
    ['チ', 'ﾁ', '㋠'],
    ['ツ', 'ﾂ', '㋡'],
    ['テ', 'ﾃ', '㋢'],
    ['ト', 'ﾄ', '㋣'],
    ['ナ', 'ﾅ', '㋤'],
    ['ニ', 'ﾆ', '㋥'],
    ['ヌ', 'ﾇ', '㋦'],
    ['ネ', 'ﾈ', '㋧'],
    ['ノ', 'ﾉ', '㋨'],
    ['ハ', 'ﾊ', '㋩'],
    ['ヒ', 'ﾋ', '㋪'],
    ['フ', 'ﾌ', '㋫'],
    ['ヘ', 'ﾍ', '㋬'],
    ['ホ', 'ﾎ', '㋭'],
    ['マ', 'ﾏ', '㋮'],
    ['ミ', 'ﾐ', '㋯'],
    ['ム', 'ﾑ', '㋰'],
    ['メ', 'ﾒ', '㋱'],
    ['モ', 'ﾓ', '㋲'],
    ['ヤ', 'ﾔ', '㋳'],
    ['ユ', 'ﾕ', '㋴'],
    ['ヨ', 'ﾖ', '㋵'],
    ['ラ', 'ﾗ', '㋶'],
    ['リ', 'ﾘ', '㋷'],
    ['ル', 'ﾙ', '㋸'],
    ['レ', 'ﾚ', '㋹'],
    ['ロ', 'ﾛ', '㋺'],
    ['ワ', 'ﾜ', '㋻'],
    ['ヰ', '㋼'],
    ['ヱ', '㋽'],
    ['ヲ', 'ｦ', '㋾'],
    ['ン', 'ﾝ'],
    ['ァ', 'ｧ'],
    ['ィ', 'ｨ'],
    ['ゥ', 'ｩ'],
    ['ェ', 'ｪ'],
    ['ォ', 'ｫ'],
    ['ッ', 'ｯ'],
    ['ャ', 'ｬ'],
    ['ュ', 'ｭ'],
    ['ョ', 'ｮ'],
    # SYMBOL
    ['■', '☑'],
    ['□', '☐'],
    ['、', '､'],
    ['。', '｡'],
    ['「', '｢'],
    ['」', '｣'],
    ['・', '･'],
    ['ー', 'ｰ'],
    # JOYOKANJI
    ['亜', '亞'],
    ['悪', '惡'],
    ['圧', '壓'],
    ['囲', '圍'],
    ['医', '醫'],
    ['為', '爲'],
    ['壱', '壹'],
    ['逸', '逸'],
    ['隠', '隱'],
    ['栄', '榮'],
    ['営', '營'],
    ['衛', '衞'],
    ['駅', '驛'],
    ['謁', '謁'],
    ['円', '圓'],
    ['塩', '鹽'],
    ['縁', '緣'],
    ['艶', '艷'],
    ['応', '應'],
    ['欧', '歐'],
    ['殴', '毆'],
    ['桜', '櫻'],
    ['奥', '奧'],
    ['横', '橫'],
    ['温', '溫'],
    ['穏', '穩'],
    ['仮', '假'],
    ['価', '價'],
    ['禍', '禍'],
    ['画', '畫'],
    ['会', '會'],
    ['悔', '悔'],
    ['海', '海'],
    ['絵', '繪'],
    ['壊', '壞'],
    ['懐', '懷'],
    ['慨', '慨'],
    ['概', '槪'],
    ['拡', '擴'],
    ['殻', '殼'],
    ['覚', '覺'],
    ['学', '學'],
    ['岳', '嶽'],
    ['楽', '樂'],
    ['喝', '喝'],
    ['渇', '渴'],
    ['褐', '褐'],
    ['缶', '罐'],
    ['巻', '卷'],
    ['陥', '陷'],
    ['勧', '勸'],
    ['寛', '寬'],
    ['漢', '漢'],
    ['関', '關'],
    ['歓', '歡'],
    ['観', '觀'],
    ['気', '氣'],
    ['祈', '祈'],
    ['既', '既'],
    ['帰', '歸'],
    ['亀', '龜'],
    ['器', '器'],
    ['偽', '僞'],
    ['戯', '戲'],
    ['犠', '犧'],
    ['旧', '舊'],
    ['拠', '據'],
    ['挙', '擧'],
    ['虚', '虛'],
    ['峡', '峽'],
    ['挟', '挾'],
    ['狭', '狹'],
    ['郷', '鄕'],
    ['響', '響'],
    ['暁', '曉'],
    ['勤', '勤'],
    ['謹', '謹'],
    ['区', '區'],
    ['駆', '驅', '駈'],  # "駈"は追加
    ['勲', '勳'],
    ['薫', '薰'],
    ['径', '徑'],
    ['茎', '莖'],
    ['恵', '惠'],
    ['掲', '揭'],
    ['渓', '溪'],
    ['経', '經'],
    ['蛍', '螢'],
    ['軽', '輕'],
    ['継', '繼'],
    ['鶏', '鷄'],
    ['芸', '藝'],
    ['撃', '擊'],
    ['欠', '缺'],
    ['研', '硏'],
    ['県', '縣'],
    ['倹', '儉'],
    ['剣', '劍'],
    ['険', '險'],
    ['圏', '圈'],
    ['検', '檢'],
    ['献', '獻'],
    ['権', '權'],
    ['顕', '顯'],
    ['験', '驗'],
    ['厳', '嚴'],
    ['広', '廣'],
    ['効', '效'],
    ['恒', '恆'],
    ['黄', '黃'],
    ['鉱', '鑛'],
    ['号', '號'],
    ['国', '國'],
    ['黒', '黑'],
    ['穀', '穀'],
    ['砕', '碎'],
    ['済', '濟'],
    ['斎', '齋'],
    ['剤', '劑'],
    ['殺', '殺'],
    ['雑', '雜'],
    ['参', '參'],
    ['桟', '棧'],
    ['蚕', '蠶'],
    ['惨', '慘'],
    ['賛', '贊'],
    ['残', '殘'],
    ['糸', '絲'],
    ['祉', '祉'],
    ['視', '視'],
    ['歯', '齒'],
    ['児', '兒'],
    ['辞', '辭'],
    ['湿', '濕'],
    ['実', '實'],
    ['写', '寫'],
    ['社', '社'],
    ['者', '者'],
    ['煮', '煮'],
    ['釈', '釋'],
    ['寿', '壽'],
    ['収', '收'],
    ['臭', '臭'],
    ['従', '從'],
    ['渋', '澁'],
    ['獣', '獸'],
    ['縦', '縱'],
    ['祝', '祝'],
    ['粛', '肅'],
    ['処', '處'],
    ['暑', '暑'],
    ['署', '署'],
    ['緒', '緖'],
    ['諸', '諸'],
    ['叙', '敍', '敘'],  # "敘"が追加
    ['将', '將'],
    ['祥', '祥'],
    ['称', '稱'],
    ['渉', '涉'],
    ['焼', '燒'],
    ['証', '證'],
    ['奨', '奬'],
    ['条', '條'],
    ['状', '狀'],
    ['乗', '乘'],
    ['浄', '淨'],
    ['剰', '剩'],
    ['畳', '疊'],
    ['縄', '繩'],
    ['壌', '壤'],
    ['嬢', '孃'],
    ['譲', '讓'],
    ['醸', '釀'],
    ['触', '觸'],
    ['嘱', '囑'],
    ['神', '神'],
    ['真', '眞'],
    ['寝', '寢'],
    ['慎', '愼'],
    ['尽', '盡'],
    ['図', '圖'],
    ['粋', '粹'],
    ['酔', '醉'],
    ['穂', '穗'],
    ['随', '隨'],
    ['髄', '髓'],
    ['枢', '樞'],
    ['数', '數'],
    ['瀬', '瀨'],
    ['声', '聲'],
    ['斉', '齊'],
    ['静', '靜'],
    ['窃', '竊'],
    ['摂', '攝'],
    ['節', '節'],
    ['専', '專'],
    ['浅', '淺'],
    ['戦', '戰'],
    ['践', '踐'],
    ['銭', '錢'],
    ['潜', '潛'],
    ['繊', '纖'],
    ['禅', '禪'],
    ['祖', '祖'],
    ['双', '雙'],
    ['壮', '壯'],
    ['争', '爭'],
    ['荘', '莊'],
    ['捜', '搜'],
    ['挿', '插'],
    ['巣', '巢'],
    ['曽', '曾'],
    ['痩', '瘦'],
    ['装', '裝'],
    ['僧', '僧'],
    ['層', '層'],
    ['総', '總'],
    ['騒', '騷'],
    ['増', '增'],
    ['憎', '憎'],
    ['蔵', '藏'],
    ['贈', '贈'],
    ['臓', '臟'],
    ['即', '卽'],
    ['属', '屬'],
    ['続', '續'],
    ['堕', '墮'],
    ['対', '對'],
    ['体', '體'],
    ['帯', '帶'],
    ['滞', '滯'],
    ['台', '臺'],
    ['滝', '瀧'],
    ['択', '擇'],
    ['沢', '澤'],
    ['担', '擔'],
    ['単', '單'],
    ['胆', '膽'],
    ['嘆', '嘆'],
    ['団', '團'],
    ['断', '斷'],
    ['弾', '彈'],
    ['遅', '遲'],
    ['痴', '癡'],
    ['虫', '蟲'],
    ['昼', '晝'],
    ['鋳', '鑄'],
    ['著', '著'],
    ['庁', '廳'],
    ['徴', '徵'],
    ['聴', '聽'],
    ['懲', '懲'],
    ['勅', '敕'],
    ['鎮', '鎭'],
    ['塚', '塚'],
    ['逓', '遞'],
    ['鉄', '鐵'],
    ['点', '點'],
    ['転', '轉'],
    ['伝', '傳'],
    ['都', '都'],
    ['灯', '燈'],
    ['当', '當'],
    ['党', '黨'],
    ['盗', '盜'],
    ['稲', '稻'],
    ['闘', '鬭'],
    ['徳', '德'],
    ['独', '獨'],
    ['読', '讀'],
    ['突', '突'],
    ['届', '屆'],
    ['難', '難'],
    ['弐', '貳'],
    ['悩', '惱'],
    ['脳', '腦'],
    ['覇', '霸'],
    ['拝', '拜'],
    ['廃', '廢'],
    ['売', '賣'],
    ['梅', '梅'],
    ['麦', '麥'],
    ['発', '發'],
    ['髪', '髮'],
    ['抜', '拔'],
    ['繁', '繁'],
    ['晩', '晚'],
    ['蛮', '蠻'],
    ['卑', '卑'],
    ['秘', '祕'],
    ['碑', '碑'],
    ['浜', '濱', '濵'],  # "濵"は追加
    ['賓', '賓'],
    ['頻', '頻'],
    ['敏', '敏'],
    ['瓶', '甁'],
    ['侮', '侮'],
    ['福', '福'],
    ['払', '拂'],
    ['仏', '佛'],
    ['併', '倂'],
    ['並', '竝'],
    ['塀', '塀'],
    ['餅', '餠'],
    ['辺', '邊'],
    ['変', '變'],
    ['弁', '辨', '瓣', '辯'],
    ['勉', '勉'],
    ['歩', '步'],
    ['宝', '寶'],
    ['豊', '豐'],
    ['褒', '襃'],
    ['墨', '墨'],
    ['翻', '飜'],
    ['毎', '每'],
    ['万', '萬'],
    ['満', '滿'],
    ['免', '免'],
    ['麺', '麵'],
    ['黙', '默'],
    ['弥', '彌'],
    ['訳', '譯'],
    ['薬', '藥'],
    ['与', '與'],
    ['予', '豫'],
    ['余', '餘'],
    ['誉', '譽'],
    ['揺', '搖'],
    ['様', '樣'],
    ['謡', '謠'],
    ['来', '來'],
    ['頼', '賴'],
    ['乱', '亂'],
    ['覧', '覽'],
    ['欄', '欄'],
    ['竜', '龍'],
    ['隆', '隆'],
    ['虜', '虜'],
    ['両', '兩'],
    ['猟', '獵'],
    ['緑', '綠'],
    ['涙', '淚'],
    ['塁', '壘'],
    ['類', '類'],
    ['礼', '禮', '礼'],  # "礼"は追加
    ['励', '勵'],
    ['戻', '戾'],
    ['霊', '靈'],
    ['齢', '齡'],
    ['暦', '曆'],
    ['歴', '歷'],
    ['恋', '戀'],
    ['練', '練'],
    ['錬', '鍊'],
    ['炉', '爐'],
    ['労', '勞'],
    ['郎', '郞'],
    ['朗', '朗'],
    ['廊', '廊'],
    ['楼', '樓'],
    ['録', '錄'],
    ['湾', '灣'],
    # 基本
    ['吉', '𠮷'],
    ['崎', '﨑'],
    ['高', '髙'],
    # 特殊
    ['印', '㊞'],
    ['有', '㈲'],
    ['株', '㈱'],
    ['社', '㈳'],
    ['財', '㈶'],
    # 追加
    ['侠', '俠'],
    ['巌', '巖'],
    ['桑', '桒'],
    ['桧', '檜'],
    ['槙', '槇'],
    ['祐', '祐'],
    ['祷', '禱'],
    ['禄', '祿'],
    ['秦', '䅈'],
    ['穣', '穰'],
    ['第', '㐧'],
    ['蝉', '蟬'],
    ['頬', '頰'],
    ['鴎', '鷗'],
    ['鴬', '鶯'],
]


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


if len(sys.argv) == 2:
    is_forward = True
    in_str = sys.argv[1]
elif len(sys.argv) == 3 and sys.argv[1] == '-r':
    is_forward = False
    in_str = sys.argv[2]
else:
    print(in_str)
    sys.exit(1)


for cl in CHAR_LISTS:
    if not is_forward:
        cl.reverse()
    cl.append(cl[0])
    for i in range(len(cl) - 1):
        if re.match('^.*' + cl[i] + '$', in_str):
            print(re.sub(cl[i] + '$', cl[i + 1], in_str))
            sys.exit(0)


print(in_str)
sys.exit(1)

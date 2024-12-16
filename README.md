# sazae(栄螺)

## 概要

UNIX系OS（macOS、Linux、WSL（Windows Subsystem for Linux）等）の
シェルzsh（Z shell）のコマンドラインで、migemo（cmigemo）を使い、
ローマ字の文字列から、日本語のファイル名（ディレクトリ名を含む。）も含めて、
補完候補を表示し、実際に補完するソフトウェアです。

日本で生活し仕事をする以上、一部の特殊な状況（理工系の研究職等）を除き、
日本語のファイル名は避けて通れません。

zshは非常に優れた補完機能を有していますが、日本語のファイル名の場合は、
簡単に補完できない状況もあります。

そこで、migemo（cmigemo）を使って、
ローマ字の文字列から、候補となる日本語のファイル名を選び出し、
補完候補を表示し、実際に補完させることができるようにしました。

「list-choices」及び「expand-or-complete」とほとんど同じ動作をしますが、
日本語のファイル名も含めて、補完候補を表示し、実際に補完します。

例えば、「北海道.txt」から「沖縄県.txt」までのファイルが存在する状態で、
「cat yama」まで入力し、Ctrl-dを押すと、
「山形県.txt 山口県.txt 山梨県.txt」と補完候補を表示し、Ctrl-i又はTabを押すと、
「山形県.txt」と「山口県.txt」「山梨県.txt」を実際に補完します。

実行例

``` zsh
zsh> cd todo (Ctrl-i or Tab)
zsh> cd 都道府県/
zsh> ls
愛知県.txt   宮城県.txt   埼玉県.txt   新潟県.txt   長崎県.txt   富山県.txt
愛媛県.txt   京都府.txt   三重県.txt   神奈川県.txt 長野県.txt   福井県.txt
茨城県.txt   熊本県.txt   山形県.txt   青森県.txt   鳥取県.txt   福岡県.txt
岡山県.txt   群馬県.txt   山口県.txt   静岡県.txt   島根県.txt   福島県.txt
沖縄県.txt   広島県.txt   山梨県.txt   石川県.txt   東京都.txt   兵庫県.txt
岩手県.txt   香川県.txt   滋賀県.txt   千葉県.txt   徳島県.txt   北海道.txt
岐阜県.txt   高知県.txt   鹿児島県.txt 大阪府.txt   栃木県.txt   和歌山県.txt
宮崎県.txt   佐賀県.txt   秋田県.txt   大分県.txt   奈良県.txt
zsh> cat yama (Ctrl-d)
山形県.txt 山口県.txt 山梨県.txt                                             
zsh> cat yama (Ctrl-i or Tab)
zsh> cat 山 (Ctrl-i or Tab)
zsh> cat 山形県 (Ctrl-i or Tab)
zsh> cat 山口県 (Ctrl-i or Tab)
zsh> cat 山梨県
甲府市
zsh> cat *yama (Ctrl-d)
岡山県.txt   山形県.txt   山口県.txt   山梨県.txt   富山県.txt   和歌山県.txt 
zsh> cat *yama (Ctrl-i or Tab)
zsh> cat  (Ctrl-i or Tab)
zsh> cat 岡山県 (Ctrl-i or Tab)
zsh> cat 山形県 (Ctrl-i or Tab)
zsh> cat 山口県 (Ctrl-i or Tab)
zsh> cat 山梨県 (Ctrl-i or Tab)
zsh> cat 富山県 (Ctrl-i or Tab)
zsh> cat 和歌山県
和歌山市
zsh> cat yamaguchi (Ctrl-i or Tab)
zsh> cat 山口県
山口市
```

![SAZAEの再現動画](https://github.com/hata48915b/sazae/blob/main/depot/sazae-example.gif "SAZAEの再現動画")

分かりやすいように、速度を落としてあります。

## 動作環境

zsh、python、migemo（cmigemo）等がインストールしてあれば、動くと思います。

## インストール方法

### zsh、python、migemo（cmigemo）等のインストール

zsh、python、migemo（cmigemo）を使いますので、インストールしてください
（すでにインストールされている可能性もありますので、よくご確認ください。）。
また、cmigemoではないmigemoの場合は、nkfを使いますので、
インストールしてください。

アプリケーションのインストールは、OSのパッケージ管理システムに依ります。
ご自身のOSのパッケージ管理システムをよく確認してください。

macOSの場合、「brew install foo」等でインストールできます。

debian、ubuntu等の場合、「apt-get install foo」等でインストールできます。

fedora、centOS等の場合、「yum install foo」等でインストールできるようです
（使ったことがないので、よく分かりません。）。

FreeBSDの場合、packagesかportsを使ってインストールできます。

### ファイルのインストール

このディレクトリを、「.zshrc-sazae」の名前で、
ホームディレクトリに移動させてください。

ホームディレクトリは、通常「/home/ユーザー名」です。

### 設定ファイルへの書込み

zshの設定ファイル（.zshrc）に、最終行付近（キーバインドの設定後）に、
「source ~/.zshrc-sazae/zshrc」と書き込んでください。

### インストーラの利用

これらのインストール作業が難しければ、
インストーラー（install）を用意しましたので、使ってください。

「ファイルのインストール」と「設定ファイルへの書込み」を自動で行います。

## アンインストール方法

### 設定ファイルへの書込みを消去

zshの設定ファイル（.zshrc）から、
「source ~/.zshrc-sazae/zshrc」を含む行を消してください。

通常は、これだけで十分です。

### ファイルのアンインストール

必要があれば、このディレクトリ（.zshrc-sazae）を、削除してください。

### zsh、python、migemo（cmigemo）等のアンインストール

必要があれば、zsh、python、migemo（cmigemo）等をアンインストールしてください。

ただし、これらのアンインストールは、注意が必要です。

zshをアンインストールした場合、
ログインシェルがなくなり、パソコンにログインできなくなる可能性があります。

pythonをアンインストールした場合、
pythonで書かれた他のソフトウェアが動かなくなり、トラブルになるかもしれません。

migemo（cmigemo）をアンインストールした場合、
emacsやw3mの検索に支障が出る可能性があります。

nkfをアンインストールした場合、日本語環境に支障が出る可能性があります。

## 使用方法

### 補完候補の表示

コマンド入力中に、Ctrl-d（Ctrlキーを押しながら、dキーを押す。）を押すと、
ファイル名の補完候補を表示します。

### 補完

コマンド入力中に、Ctrl-i（Ctrlキーを押しながら、iキーを押す。）又はTabで、
ファイル名を補完します。

### 補足説明

入力中の文字列の中の最後のアルファベットと数字の部分について、
migemoを用いて、日本語を候補に入れます。

例えば、「/home/kawa」と入力して補完すると、
「yama」にmigemoが適用され、「/home/河田」や「/home/川本」は補完候補ですが、
「home」にmigemoは適用されないため、「/ホーム/kawai」等は補完候補になりません。

なお、migemoの規則に従って、大文字を使う必要があります。

「name河田」と補完するためには、「nameKawa」と入力する必要があり、
「名前河田」と補完するためには、「namaeKawa」と入力する必要があります。

### 一時停止

本ソフトウェアは、環境によっては、補完に数秒かかる場合があり、
一時的に日本語のファイル名を使わない場合には、負担が大きすぎる場合があります。

そのような場合には、本ソフトウェアの使用を、
「sazae -n」で一時的に停止し、「sazae -y」で再開することが出来ます。

また、Esc-mでも一時的に使用を停止することが出来ます。

両者の違いは、前者がキーバインドを元に戻すのに対して、
後者はキーバインドはそのままでmigemoの使用のみを停止する点にあります。

### 文字コード

文字コードはUTF-8を前提としておりますので、Shift_JIS等では正常に作動しません。

### テストデータ

配布するzipファイルに、各都道府県名をファイル名にしたテストデータ集
（test-data.tgz）を入れてありますので、適当に展開してテストにお使いください。

## ライセンス

GNU General Public Licenseバージョン3 (GPLv3)又はその後継バージョン

GPLv3のライセンス条項は、LICENSE-GPLv3.txtをご覧ください。

## 免責条項

ライセンスに定められているとおり、本プログラムにより損害が発生したとしても、
著作権者は何らの損害賠償責任も負いませんので、ご注意ください。

## 問題点

### zshの本来的補完ができなくなる点

ファイルの補完に関して、独自の補完機能を用いることになるため、
zshの本来的補完ができなくなります。

そのため、自分で定義した補完関数による補完もできなくなり、原則として、
カレントディレクトリを基準にして、ファイル名を補完することになります。

このような補完方法は、一部のコマンドに関しては、正しくありません。

例えば、「which」の後であれば、コマンド名を補完すべきであって、
ファイル名を補完すべきではありません。

一部のコマンド（which, su, dd, cd等）については、コマンドの性質に合わせて、
補完方法を修正してありますが、十分とはいえません。

今後、補完関数をそのまま取り込むことも検討しております。

### 動作速度が遅い点

zshの本来的補完に比べて、動作速度が遅く、ワンテンポ遅れます。

migemoを用いている以上、ある程度はやむを得ないところと考えています。

### 入力文字の一部が消える点

1回目の補完で、候補が多数の場合に、入力が消えてしまうという問題があります。

例えば、「/home/河田」と「/home/川本」というファイルが存在する状態で、
「/home/kawa」まで入力して補完すると、両ファイルを補完候補としたうえで、
両者の先頭からの共通部分である「/home/」を表示するため、
「kawa」が一時的に消えてしまいます。

最初は驚きますが、慣れれば大丈夫だと思います。

### 予想外の補完をする点

文字数が少ないと、予想外の補完をする場合があります。

例えば、「i」で補完すると、「1」から始まるファイルもヒットするため、
驚く場合があります。

これは辞書の問題ですので、辞書を調整すれば、改善するかもしれません。

### ファイル名に改行コードを含むファイルは補完できない点

ファイル名に改行コードを含めることはあまりないと思いますが、
ファイル名に改行コードを含むファイルは補完できません。

### 文字コードがUTF-8でないファイルは補完の対象にならない点

文字コードがUTF-8でないファイルは、補完できないのはもちろんですが、
そもそも補完の対象になりません。

例えば、「東京都.txt」というファイルがShift_JISであった場合、
「tokyo」で補完できないのはもちろん、「*.txt」でも補完できません。
これは、UTF-8でない部分が文字とみなされないため、
正規表現でヒットしないためです。

また、「東京都.txt」というファイルがShift_JISであった場合、
「*.txt」で補完候補を表示させると、エラーになります。
これは、UTF-8でないファイル名は、文字幅を数えることができないため、
補完候補を並べて表示することができないためです。

この問題は、Windows上で作成したzipファイルを展開した場合などで、
発生する可能性があります。

## 開発動機

### 日本語のファイル名の問題

日本で生活し仕事をする以上、一部の特殊な状況（理工系の研究職等）を除き、
日本語のファイル名は避けて通れません。

日本語のファイル名は、
GUIの場合（マウスでクリックする場合）は、特に苦労しませんが、
CUIの場合（コマンドラインで指定する場合）は、漢字に変換しなければならず、
非常に苦労します。

zshの場合、補完候補を順番に補完してくれますので、
気長に補完候補を待っても良いのですが、うっかりボタンを押しすぎて、
通りすぎてしまうなど、悲劇は絶えません。

そこで、「ls $2* | grep -E `migemo $1`」のようなシェルスクリプトを作り、
これを使ってファイルを探した後、手作業でコマンドラインに写していたのですが、
いちいち、マウスに手を伸ばし、コピーアンドペーストしなければならず、
その度に作業が中断してしまいます。

そのまま補完できないかと思い、開発に着手しました。

### pythonのスクリプトを入れた経緯

当初は、zshのスクリプトのみで書いたのですが、
速度面で問題があったため（非力なパソコンでは補完に数秒かかります。）、
一部の作業にpythonのスクリプトを入れ、高速化を図りました。

それでも、「list-choices」や「expand-or-complete」に比べると、かなり遅いです。

今後、パソコンの性能が飛躍的に向上し、十分な処理速度が出たときには、
zshのスクリプトのみで実装したいと考えています。

## 著作権

Copyright © 2017-2024  Seiichiro HATA

## ライセンス

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## 連絡先

[弁護士 秦 誠一郎の公式ページ](https://hata-o.jp/hata48915b/)

[弁護士 秦 誠一郎の連絡先](<mailto:hata48915b@post.nifty.jp>)

## ウェブページ

[公式ページ（github）](https://github.com/hata48915b/sazae)

## ヒストリー

### 2023.04.29 v32 リリース

バグを修正しました。

### 2023.04.22 v31 リリース

補完に失敗後に最終文字を異字体に変換する機能を追加しました。

### 2022.12.08 v30 リリース

バグを修正しました。

ディレクトリ構造の変化に対応しました。

### 2022.08.11 v29 リリース

改行を含むコマンドラインに対応しました。

gitコマンドの補完を強化しました。

### 2021.10.03 v28 リリース

コマンドごと（git、brew、yum等）の補完関数を強化しました。

### 2021.07.04 v27 リリース

補完候補の共通部分が空の場合に"---"が表示されるように変更しました。

### 2020.07.13 v26 リリース

バグを修正しました。

### 2020.05.25 v25 リリース

コマンドごとの補完関数を強化しました。

### 2020.03.01 v24 リリース

一定の場合にカレントディレクトリを除外する仕様を修正しました。

### 2019.10.28 v23 リリース

起動時のシステム確認を強化しました。

### 2019.10.13 v22 リリース

バグを修正し、macOSに対応しました。

### 2019.07.30 v21 リリース

コマンドラインを解析する関数を改善しました。

バグを修正しました。

### 2019.04.27 v20 リリース

Esc-mで一時的にmigemoの使用を停止できるようにしました。

### 2019.03.25 v19 リリース

Pythonの仕様変更に対応しました。

### 2019.01.13 v18 リリース

「/u/s/e」で「/usr/share/emacs」を補完するようにしました。

コマンドごとの補完関数を強化しました。

バグを修正しました。

### 2019.01.05 v17 リリース

記号による表示幅のずれに対応しました。

バグを修正しました。

### 2018.11.15 v16 リリース

バグを修正しました。

### 2018.08.04 v15 リリース

コマンドごとの補完関数を強化しました。

バグを修正しました。

### 2018.05.30 v14 リリース

バグを修正しました。

### 2018.05.10 v13 リリース

バグを修正しました。

### 2018.05.04 v12 リリース

バグを修正しました。

### 2017.12.16 v11 リリース

リダイレクトに対応しました。

### 2017.11.22 v10 リリース

環境変数の設定に対応しました。

### 2017.10.09 v09 リリース

シンボリックリンクに対応しました。

補完候補のカラー表示に対応しました。

一時停止に対応しました。

### 2017.09.17 v08 リリース

バグを修正しました。

### 2017.08.17 v07 リリース

ビープ音の設定に対応しました。

### 2017.08.09 v06 リリース

カレントディレクトリが削除された場合に対応しました。

### 2017.08.04 v05 リリース

複雑なコマンドラインにも対応しました。

コマンドごとの補完関数を強化しました。

バグを修正しました。

### 2017.07.01 v04 リリース

バグを修正しました。

### 2017.06.24 v03 リリース

バグを修正しました。

echoをprintfに書き換えました。

### 2017.06.14 v02 リリース

バグを修正しました。

### 2017.06.12 v01 リリース

最初のリリースです。

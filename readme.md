# 環境
- Python 3.6.5
- Windows (& WSL), Linux, Mac (Tested on Windows 10)
- MeCab Neologd

# Python パッケージ
- MeCab
- neologch

# 使い方
```shell
mv /path/to/projectnextnlp-chat-dialogue-corpus /path/to/N-Corpus-parser/
python parser.py --type 1
python parser.py --type 2
python perser.py --type 3 --split_func [word, yomi, word-yomi]
                          --max_sentence_length [10, 200) 
                          --min_sentence_length [1, 10) 
                          --remove_english True
```
または、
```shell
mv /path/to/projectnextnlp-chat-dialogue-corpus /path/to/N-Corpus-parser/
python parser.py --type 4
```

最終的に得られるファイルは cleaned-corpus.csv です。
## 引数の説明
- --type (必須)     
    行うプロセスの指定    
    - 1   
        コーパスのテキストを一つのファイルにマージする
    - 2   
        マージしたファイルをアノテーションに基づいて対話コーパスに変換する
    - 3   
        対話コーパスをクリーニングし、指定された方式に基づいて分割する
        
- --split_func (省略可)
    テキストを分割する手法の設定
    - word 単語分割
    - yomi 文字分割
    - word-yomi 単語分割 & よみがなに変換
- --max_sentence_length (省略可)  
   許容するテキストの最大長
- --min_sentence_length (省略可)   
    許容するテキストの最小長
- --remove_english    (省略可)   
    英単語を含むテキストを許容するか

# MeCab Neologd のインストール for Windows
```shell
sudo apt install mecab libmecab-dev mecab-ipadic-utf-8
pip install mecab-python-windows
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git 
cd mecab-ipadic-neologd
sudo ./bin/instal-mecaab-ipadic-neologd
nano /etc/mecabrc
```

```text
;
; Configuration file of MeCab
;
; $Id: mecabrc.in,v 1.3 2006/05/29 15:36:08 taku-ku Exp $;
;
; dicdir = /var/lib/mecab/dic/debian
dicdir = /usr/lib/mecab/dic/mecab-ipadic-neologd

; userdic = /home/foo/bar/user.dic

; output-format-type = wakati
; input-buffer-size = 8192

; node-format = %m\n
; bos-format = %S\n
; eos-format = EOS\n
```
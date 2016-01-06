# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer
t = Tokenizer()
sentence = u"日本語構文解析器CaboChaをインストールするのはyumを使うと激しく簡単だった"
sentence = u"日本語の自然言語ライブラリの中には、ヘブライ語や韓国語をぶちこんだ瞬間にエラーで処理が止まるライブラリ多いです。そんなときに便利な呪文を紹介します。"
# Open a file
fo = open("ex2.dat", "r+")
str_ = fo.read();
sentence = str_.decode('utf-8')
fo.close()

tokens = t.tokenize(sentence)

# Open a file
fo = open("ex2.txt", "wb")
for token in tokens:
    print(token)
    fo.write(str(token) + "\n")
# Close opend file
fo.close()
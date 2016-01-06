# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer
t = Tokenizer()

tokens = t.tokenize(u'吾輩は猫である。と思います。')
for token in tokens:
    print(token)
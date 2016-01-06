# -*- coding: utf-8 -*-

import re
import nltk
from janome.tokenizer import Tokenizer

def filter(text):
   """
   :param text: str
   :rtype : str
   """
   # アルファベットと半角英数と記号と改行とタブを排除
   text = re.sub(r'[a-zA-Z0-9¥"¥.¥,¥@]+', '', text)
   text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', text)
   text = re.sub(r'[\n|\r|\t]', '', text)

   # 日本語以外の文字を排除(韓国語とか中国語とかヘブライ語とか)
   jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')
   text = "".join(jp_chartype_tokenizer.tokenize(text))
   return text


text = u'他言語版Italiano한국어PolskiSimple English'
text = filter(text)
t = Tokenizer()

# Open a file
fo = open("ex3.txt", "wb")
for token in t.tokenize(text):
   print token
   fo.write(str(token) + "\n")
# Close opend file
fo.close()


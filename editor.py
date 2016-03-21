"""
A simple TKinter GUI to enter data into a given table in a database.

This program will build a small sample table into a given database
and then build a simple TKinter window with label and entry widgets
for each column in the table.
"""

import nltk
from nltk.book import *
from time import gmtime, strftime
import sqlite3
import Tkinter as tk
from Tkinter import N, S, E, W
from Tkinter import TOP, BOTTOM, LEFT, RIGHT, END, ALL
import ScrolledText
from sqlite_vocabulary import SqliteVocabulary

class TextWindow():

    def __init__(self, master=None, *args):
        #tk.Frame.__init__(self, master)
        self.master = tk.Tk()
        self.init_window()
        #self.master.mainloop()

    def init_window(self):
        frame_text = tk.Frame(self.master)
        frame_text.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=2, expand=tk.Y)
        st  = ScrolledText.ScrolledText(frame_text)
        st.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=2, expand=tk.Y)

        def nature_language_processing(self):
            sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
            text = st.get(1.0, END) # open('document.txt').read() # nltk.corpus.gutenberg.raw('document.txt')
            sents = sent_tokenizer.tokenize(text)
            words = nltk.word_tokenize(text)
            fdist = FreqDist(words)

            sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
            #sqlVocab.delete_vocabulary()
            for sent in sents:
                tokens = nltk.word_tokenize(sent)
                #words = [w.lower() for w in tokens]
                #vocab = sorted(set(words))
                tagged = nltk.pos_tag(tokens)

                for v, t in tagged:
                    print(v,)
                    print(t)
                    print fdist.freq(v)
                    existed_word = sqlVocab.check_existed_word(v.lower())
                    if not existed_word:
                        sqlVocab.insert_vocabulary(v.lower(), t, "", "", sent, 1, strftime("%Y-%m-%d", gmtime()), fdist.freq(v), fdist.freq(v))

            for v in fdist.keys():
                existed_word = sqlVocab.check_existed_word(v.lower())
                if existed_word:
                    sqlVocab.update_word_freq(v.lower(), fdist.freq(v))

            sqlVocab.commit()
            sqlVocab.close()

            self.master.destroy()

        frame_button = tk.Frame(self.master)
        frame_button.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)
        
        submit_button = tk.Button(frame_button, text='Nature Language Processing', width=50, 
                    command=lambda: nature_language_processing(self))
        submit_button.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
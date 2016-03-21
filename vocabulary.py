
import nltk
from time import gmtime, strftime
from sqlite_vocabulary import SqliteVocabulary
import Tkinter as tk
import tkFont as tkfont
import ttk

class TreeViewVocabulary(ttk.Frame):
    def __init__(self, name='treetest'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master.title('Vocabulary Table')

        self._create_treeview(self)
        self._build_fake_data()
        self._populate_tree()

        self._showContextMenu(self)

        self.tree.bind("<Double-1>", self.OnDoubleClick)
        # attach popup to frame
        self.tree.bind("<Button-3>", self._popup)

    def _onDoubleClick(self, event):
        # item = self.tree.selection()[0]
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))
        values = self.tree.item(item,"values")
        print(values(0))

    def _vocabularyStudied(self):
        print("_vocabularyStudied", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        sqlVocab.update_word_status(values[0], 1)        
        """sqlVocabStudied = SqliteVocabulary("studyenglish.db", "vocabulary_studied")
                                # sqlVocabStudied.delete_vocabulary()
                                values = self.tree.item(self.item,"values")
                                existed_word = sqlVocabStudied.check_existed_word(values[(0)])
                                if not existed_word:
                                    sqlVocabStudied.insert_vocabulary(values[(0)], values[(1)], values[(2)], values[(3)], values[(4)], values[(5)])
                        
                                sqlVocabStudied.commit()
                                sqlVocabStudied.close()"""

    def _vocabularyStudying(self):
        print("_vocabularyStudying", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        sqlVocab.update_word_status(values[0], 0)
        """sqlVocabStudying = SqliteVocabulary("studyenglish.db", "vocabulary_studying")
                                # sqlVocabStudying.delete_vocabulary()
                                values = self.tree.item(self.item,"values")
                                existed_word = sqlVocabStudying.check_existed_word(values[(0)])
                                if not existed_word:
                                    sqlVocabStudying.insert_vocabulary(values[(0)], values[(1)], values[(2)], values[(3)], values[(4)], values[(5)])
                        
                                sqlVocabStudying.commit()
                                sqlVocabStudying.close()"""

    def _vocabularyIgnored(self):
        print("_vocabularyInorge", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        sqlVocab.update_word_status(values[0], -1)
        """sqlVocabIgnored = SqliteVocabulary("studyenglish.db", "vocabulary_ignored")
                                # sqlVocabIgnored.delete_vocabulary()
                                values = self.tree.item(self.item,"values")
                                existed_word = sqlVocabIgnored.check_existed_word(values[(0)])
                                if not existed_word:
                                    sqlVocabIgnored.insert_vocabulary(values[(0)], values[(1)], values[(2)], values[(3)], values[(4)], values[(5)])
                        
                                sqlVocabIgnored.commit()
                                sqlVocabIgnored.close()"""

    def _showContextMenu(self, parent):
        # create a popup menu
        self.menu = tk.Menu(parent, tearoff=0)
        self.menu.add_command(label="Studied", command=self._vocabularyStudied)
        self.menu.add_command(label="Studying", command=self._vocabularyStudying)
        self.menu.add_command(label="Ignore", command=self._vocabularyIgnored)

    def _popup(self, event):
        self.item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(self.item,"text"))
        self.tree.selection_set(self.item)
        self.menu.post(event.x_root, event.y_root)

    def OnDoubleClick(self, event):
        # item = self.tree.selection()[0]
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))
        values = self.tree.item(item,"values")
        print(values[0])

    def _create_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.Y)

        # (word, status, vietnamese, japanese, study_date, sentence)
        # create the tree and scrollbars
        self.dataCols = ('word', 'status', 'vietnamese', 'japanese', 'study_date', 'sentence')
        self.tree = ttk.Treeview(columns=self.dataCols)

        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0',         text='#',           anchor=tk.E)
        self.tree.heading('word',  text='word',  anchor=tk.W)
        self.tree.heading('status',   text='status',   anchor=tk.E)
        self.tree.heading('vietnamese',     text='vietnamese',      anchor=tk.W)
        self.tree.heading('japanese',     text='japanese', anchor=tk.W)
        self.tree.heading('study_date', text='study_date', anchor=tk.W)
        self.tree.heading('sentence', text='sentence', anchor=tk.W)

        self.tree.column('#0',         stretch=0, width=50 , anchor=tk.E)
        self.tree.column('word',  stretch=0, width=160)
        self.tree.column('status',   stretch=0, width=50, anchor=tk.E)
        self.tree.column('vietnamese',     stretch=0, width=160)
        self.tree.column('japanese',     stretch=0, width=160)
        self.tree.column('study_date', stretch=0, width=100)
        self.tree.column('sentence', stretch=0, width=300)

        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=tk.NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=tk.NS)
        xsb.grid(in_=f, row=1, column=0, sticky=tk.EW)

        # set frame resizing priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

        # create fonts and tags
        self.normal   = tkfont.Font(family='Consolas', size=10)
        self.boldfont = tkfont.Font(family='Consolas', size=10, weight='bold')
        self.whacky   = tkfont.Font(family='Jokerman', size=10)

        self.tree.tag_configure('normal',   font=self.normal)
        self.tree.tag_configure('timedout', background='pink',
            font=self.boldfont)
        self.tree.tag_configure('whacky',   background='lightgreen',
            font=self.whacky)

    def _build_fake_data(self):
        # create a dict with a number as key, and randomized contents matching
        # the column layout of the table

        self.data = {}

        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        words = sqlVocab.query_words_with_status(0)
        num = 0
        for w in words:
            num += 1
            self.data[num] = w

    def _populate_tree(self):
        for n in range(len(self.data)):
            num = n+1
            item = self.data[num]

            if item[2] == 'word': # use highlight if status is 'timedout'
                tags = ('timedout')
            else:
                tags = ('normal')

            if '5' in item[0]: # override styles if there's a 5 in the ipaddress
                tags = ['whacky']

            self.tree.insert('', tk.END, text='%3d'%num, values=item, tags=tags)

def main():
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    text = open('document.txt').read() # nltk.corpus.gutenberg.raw('document.txt')
    sents = sent_tokenizer.tokenize(text)

    sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
    #sqlVocab.delete_vocabulary()

    for sent in sents:
        tokens = nltk.word_tokenize(sent)
        words = [w.lower() for w in tokens]
        vocab = sorted(set(words))

        for v in vocab:
            existed_word = sqlVocab.check_existed_word(v)
            if not existed_word:
                sqlVocab.insert_vocabulary(v, 0, "", "", strftime("%Y-%m-%d", gmtime()), sent)

    sqlVocab.commit()
    sqlVocab.close()

if __name__ == '__main__':
    main()
    TreeViewVocabulary().mainloop()


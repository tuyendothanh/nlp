
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

from time import gmtime, strftime
from sqlite_vocabulary import SqliteVocabulary
import Tkinter as tk
import tkFont as tkfont
import ttk
from sqlite_table import EntryWindow
from editor import TextWindow
from ptb_poses import *
import requests
import lxml.html
import os

class TreeViewVocabulary(ttk.Frame):
    def __init__(self, name='treetest'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master.title('Vocabulary Table')

        self._create_button(self)
        
        self._create_treeview(self)
        self._build_vocabulary_data(None)
        self._populate_tree()

        self._showContextMenu(self)

        self.tree.bind("<Double-1>", self.OnDoubleClick)
        # attach popup to frame
        self.tree.bind("<Button-3>", self._popup)

    def _vocabularyStudied(self):
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        for item in self.items:
            print("_vocabularyStudied", self.tree.item(item,"text"))
            values = self.tree.item(item,"values")
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
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        for item in self.items:            
            print("_vocabularyStudying", self.tree.item(item,"text"))
            values = self.tree.item(item,"values")
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
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        for item in self.items:            
            print("_vocabularyInorge", self.tree.item(item,"text"))
            values = self.tree.item(item,"values")
            sqlVocab.update_word_status(values[0], -1)
        """sqlVocabIgnored = SqliteVocabulary("studyenglish.db", "vocabulary_ignored")
                                # sqlVocabIgnored.delete_vocabulary()
                                values = self.tree.item(self.item,"values")
                                existed_word = sqlVocabIgnored.check_existed_word(values[(0)])
                                if not existed_word:
                                    sqlVocabIgnored.insert_vocabulary(values[(0)], values[(1)], values[(2)], values[(3)], values[(4)], values[(5)])
                        
                                sqlVocabIgnored.commit()
                                sqlVocabIgnored.close()"""

    def _edit_vocabulary(self):
        # item = self.tree.selection()[0]
        #item = self.tree.identify('item',event.x,event.y)
        #print("you clicked on", self.tree.item(item,"text"))
        values = self.tree.item(self.item,"values")
        print(values[0])
        db = 'studyenglish.db'
        tbl = 'vocabulary'
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        words = sqlVocab.query_words_with_sql("word = '{}'".format(values[0]))
        for w in words:
            root = tk.Tk()
            entry_window = EntryWindow(root, *[db, tbl, w])
            #root.mainloop()
            break

    def _delete_vocabulary(self):
        # item = self.tree.selection()[0]
        #item = self.tree.identify('item',event.x,event.y)
        #print("you clicked on", self.tree.item(item,"text"))
        values = self.tree.item(self.item,"values")
        print(values[0])
        db = 'studyenglish.db'
        tbl = 'vocabulary'
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        words = sqlVocab.delete_word(values[0])

    def _get_uks_link_mp3_cambridge(self, org_word, word, item):
        BASE_URL = 'http://dictionary.cambridge.org/dictionary/english/'
        url = BASE_URL + word
        print(url)
        html = requests.get(url).content                                          
        tree = lxml.html.fromstring(html)
        uks = tree.xpath("//span[@class='sound audio_play_button pron-icon uk']/@data-src-mp3")

        #pos_header = tree.xpath("//div[@class='pos-header']")[0]
        # //*[@id="dataset-british"]/div[1]/div[2]/div/div/div[1]/span[2]
        # //*[@id="dataset-british"]/div[1]/div[2]/div/div/div[1]/span[2]/span
        # //*[@id="dataset-british"]/div[1]/div[2]/div/div/div[1]/span[@class='uk']/span[@class='pron']/span[@class='ipa']/text()
        # uks_pron = tree.xpath("//span[@class='uk']/span[@class='pron']/span[@class='ipa']/text()")
        uks_pron_html = tree.xpath("//*[@id='dataset-british']/div[1]/div[2]/div/div/div[1]/span[@class='uk']/span[@class='pron']/span[@class='ipa']")
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        #import xml.etree.ElementTree as ET
        uks_pron = [html.text_content() for html in uks_pron_html]
        prons = u'/' + u'/,/'.join(uks_pron) + u'/'
        #if uks_pron:
        #    prons = u'/' + uks_pron[0] + u'/'
        self.tree.set(item,'#2',prons)
        if len(uks_pron)>0:
            sqlVocab.update_uk_pron(org_word, prons)

        return uks

    def _get_uss_link_mp3_cambridge(self, org_word, word, item):
        BASE_URL = 'http://dictionary.cambridge.org/dictionary/english/'
        url = BASE_URL + word
        print(url)
        html = requests.get(url).content                                          
        tree = lxml.html.fromstring(html)
        uss = tree.xpath("//span[@class='sound audio_play_button pron-icon us']/@data-src-mp3")

        #pos_header = tree.xpath("//div[@class='pos-header']")[0]
        #uss_pron = tree.xpath("//span[@class='us']/span[@class='pron']/span[@class='ipa']/text()")
        #uss_pron = tree.xpath("//*[@id='dataset-british']/div[1]/div[2]/div/div/div[1]/span[@class='us']/span[@class='pron']/span[@class='ipa']/text()")
        uss_pron_html = tree.xpath("//*[@id='dataset-british']/div[1]/div[2]/div/div/div[1]/span[@class='us']/span[@class='pron']/span[@class='ipa']")
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        uss_pron = [html.text_content() for html in uss_pron_html]
        prons = u'/' + u'/,/'.join(uss_pron) + u'/'
        self.tree.set(item,'#3',prons)
        if len(uss_pron)>0:
            sqlVocab.update_us_pron(org_word, prons)

        return uss

    def _download_mp3_cambridge(self, region_link, region_pron_dir):
        sound_dir = region_pron_dir + "/" + region_link.split('/')[-1]
        if not os.path.exists(sound_dir):
            import urllib
            urllib.urlretrieve (region_link, sound_dir)
        return sound_dir

    def _dictionary_cambridge_org(self):
        print("_dictionary_cambridge_org", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        import webbrowser
        url = 'http://dictionary.cambridge.org/dictionary/english/' + values[0]
        webbrowser.open(url)
        #webbrowser.open(url, new=1, autoraise=True)

    def _tratu_soha_vn(self):
        print("_dictionary_cambridge_org", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        import webbrowser
        url = 'http://tratu.soha.vn/dict/en_vn/' + values[0]
        webbrowser.open(url)

    def _vdict_com(self):
        print("_dictionary_cambridge_org", self.tree.item(self.item,"text"))
        values = self.tree.item(self.item,"values")
        import webbrowser
        url = "http://vdict.com/{},1,0,0.html".format(values[0])
        webbrowser.open(url)

    def _us_pron(self):
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        for item in self.items:
            print("_us_pron", self.tree.item(item,"text"))
            values = self.tree.item(item,"values")
            
            sound_dir, = sqlVocab.get_us_sound(values[0])
            if not sound_dir:
                uss = self._get_uss_link_mp3_cambridge(values[0], values[0], item)
                if not uss:
                    words = sqlVocab.query_words_with_sql("word = '{}'".format(values[0]))
                    wn_tag = self.penn_to_wn(words[0][3])
                    uss = self._get_uss_link_mp3_cambridge(values[0], WordNetLemmatizer().lemmatize(values[0],wn_tag), item)
                if uss:
                    sound_dir = self._download_mp3_cambridge(uss[0], 'us_pron')
                    if os.path.exists(sound_dir):
                        sqlVocab.update_us_sound(values[0], sound_dir)

            if os.path.exists(sound_dir):
                from pygame import mixer
                mixer.init()
                mixer.music.load(sound_dir)
                mixer.music.play()
                if len(self.items)>1:
                    import time
                    time.sleep(2) # delays for 2 seconds

    def _uk_pron(self):
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        for item in self.items:
            print("_uk_pron", self.tree.item(item,"text"))
            values = self.tree.item(item,"values")
            
            sound_dir, = sqlVocab.get_uk_sound(values[0])
            if not sound_dir:
                uks = self._get_uks_link_mp3_cambridge(values[0], values[0], item)
                if not uks:
                    words = sqlVocab.query_words_with_sql("word = '{}'".format(values[0]))
                    wn_tag = self.penn_to_wn(words[0][3])
                    uks = self._get_uks_link_mp3_cambridge(values[0], WordNetLemmatizer().lemmatize(values[0],wn_tag), item)
                if uks:
                    sound_dir = self._download_mp3_cambridge(uks[0], 'uk_pron')
                    if os.path.exists(sound_dir):
                        sqlVocab.update_uk_sound(values[0], sound_dir)

            if os.path.exists(sound_dir):
                from pygame import mixer
                mixer.init()
                mixer.music.load(sound_dir)
                mixer.music.play()
                if len(self.items)>1:
                    import time
                    time.sleep(2) # delays for 2 seconds
                

    def is_noun(self, tag):
        return tag in ['NN', 'NNS', 'NNP', 'NNPS']

    def is_verb(self, tag):
        return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

    def is_adverb(self, tag):
        return tag in ['RB', 'RBR', 'RBS']

    def is_adjective(self, tag):
        return tag in ['JJ', 'JJR', 'JJS']

    def penn_to_wn(self, tag):
        if self.is_adjective(tag):
            return wn.ADJ
        elif self.is_noun(tag):
            return wn.NOUN
        elif self.is_adverb(tag):
            return wn.ADV
        elif self.is_verb(tag):
            return wn.VERB
        else:
            if tag.startswith('J'):
                return wn.ADJ
            elif tag.startswith('V'):
                return wn.VERB
            elif tag.startswith('N'):
                return wn.NOUN
            elif tag.startswith('R'):
                return wn.ADV

        return wn.NOUN

    def _showContextMenu(self, parent):
        # create a popup menu
        self.menu = tk.Menu(parent, tearoff=0)
        self.menu.add_command(label="New word", command=self._vocabularyStudying)
        self.menu.add_command(label="Studied", command=self._vocabularyStudied)        
        self.menu.add_command(label="Ignore", command=self._vocabularyIgnored)
        self.menu.add_command(label="dictionary.cambridge.org", command=self._dictionary_cambridge_org)
        self.menu.add_command(label="tratu.soha.vn", command=self._tratu_soha_vn)
        self.menu.add_command(label="vdict.com", command=self._vdict_com)
        self.menu.add_command(label="uk pron", command=self._uk_pron)
        self.menu.add_command(label="us pron", command=self._us_pron)
        self.menu.add_command(label="Edit word", command=self._edit_vocabulary)
        self.menu.add_command(label="Delete word", command=self._delete_vocabulary)

    def _popup(self, event):
        self.item = self.tree.identify('item',event.x,event.y)
        self.items = self.tree.selection()
        print("you clicked on", self.tree.item(self.item,"text"))
        if len(self.items) == 1:
            self.tree.selection_set(self.item)
        self.menu.post(event.x_root, event.y_root)

    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        identify_column = self.tree.identify_column(event.x)
        self.item = item
        self.items = [item]
        if identify_column == '#2':
            self._uk_pron()
        else:
            self._us_pron()
        '''
        values = self.tree.item(item,"values")
        uss = self._get_uss_link_mp3_cambridge(values[0])
        if uss:
            sound_dir = self._download_mp3_cambridge(uss[0], 'us_pron')
            if os.path.exists(sound_dir):
                from pygame import mixer
                mixer.init()
                mixer.music.load(sound_dir)
                mixer.music.play()
        '''

    def show_new_words(self):
        self._build_vocabulary_data(0)
        self._populate_tree()

    def show_today_new_words(self):
        self._build_vocabulary_data(0, strftime("%Y-%m-%d", gmtime()))
        self._populate_tree()

    def show_studied_words(self):
        self._build_vocabulary_data(1)
        self._populate_tree()

    def show_ignored_words(self):
        self._build_vocabulary_data(-1)
        self._populate_tree()

    def show_all_words(self):
        self._build_vocabulary_data(None)
        self._populate_tree()

    def show_input_words(self):
        #root = tk.Tk()
        text_wnd = TextWindow(None, self.show_all_words)

    def fetch(self, entry):
        sql = entry.get()
        self._query_vocabulary_data(sql)
        self._populate_tree()

    def show_option_words(self):
        sql = self.query_entry.get()
        self._query_vocabulary_data(sql)
        self._populate_tree()

    def _create_button(self, parent):
        frame_button = tk.Frame(parent)
        frame_button.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        # Add button to show new vocabularys from database.
        new_words_button = tk.Button(frame_button, text='Show new words', width=20, command=lambda: self.show_new_words())
        new_words_button.grid(row=0, column=0, sticky=tk.E, pady=10, padx=1)
        # Add button to show new vocabularys from database.
        today_new_words_button = tk.Button(frame_button, text='Show today new words', width=20, command=lambda: self.show_today_new_words())
        today_new_words_button.grid(row=0, column=1, sticky=tk.E, pady=10, padx=1)
        # Add button to show studied vocabularys from database.
        studied_words_button = tk.Button(frame_button, text='Show studied words', width=20, command=lambda: self.show_studied_words())
        studied_words_button.grid(row=0, column=2, sticky=tk.E, pady=10, padx=1)
        # Add button to show ignored vocabularys from database.
        ignored_words_button = tk.Button(frame_button, text='Show ignored words', width=20, command=lambda: self.show_ignored_words())
        ignored_words_button.grid(row=0, column=3, sticky=tk.E, pady=10, padx=1)
        # Add button to user input into database.
        input_words_button = tk.Button(frame_button, text='Input sentences', width=20, command=lambda: self.show_input_words())
        input_words_button.grid(row=0, column=4, sticky=tk.E, pady=10, padx=1)
        # Add button to user input into database.
        all_words_button = tk.Button(frame_button, text='Show all words', width=20, command=lambda: self.show_all_words())
        all_words_button.grid(row=0, column=5, sticky=tk.E, pady=10, padx=1)
        # Add a cancel button which closes window.
        quit_button = tk.Button(frame_button, text='Close', width=8, command=self.quit)
        quit_button.grid(row=0, column=6, sticky=tk.W, pady=10, padx=1)

        self.query_entry = tk.Entry(frame_button, width=30)
        self.query_entry.insert(0, "")
        self.query_entry.grid(row=0, column=7, sticky=tk.W, pady=10, padx=1)
        #parent.bind('<Return>', (lambda event, e=query_entry: self.fetch(e)))
        # Add button to query database.
        query_button = tk.Button(frame_button, text='Query', width=10, command=lambda: self.show_option_words())
        query_button.grid(row=0, column=8, sticky=tk.E, pady=10, padx=1)

    def _create_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.Y)

        # self.dataCols = ('word', 'status', 'vietnamese', 'japanese', 'study_date', 'sentence')
        # (word, status, vietnamese, japanese, study_date, sentence)
        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        col_names = sqlVocab.get_col_names()
        self.dataCols = tuple(col_names)
        # create the tree and scrollbars
        self.tree = ttk.Treeview(columns=self.dataCols)

        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0',         text='#',           anchor=tk.E)
        """self.tree.heading('word',  text='word',  anchor=tk.W)
                                self.tree.heading('vietnamese',     text='vietnamese',      anchor=tk.W)
                                self.tree.heading('japanese',     text='japanese', anchor=tk.W)
                                self.tree.heading('sentence', text='sentence', anchor=tk.W)
                                self.tree.heading('status',   text='status',   anchor=tk.E)
                                self.tree.heading('study_date', text='study_date', anchor=tk.W)"""

        self.tree.column('#0',         stretch=0, width=50 , anchor=tk.E)
        """self.tree.column('word',  stretch=0, width=160)
                                self.tree.column('status',   stretch=0, width=50, anchor=tk.E)
                                self.tree.column('vietnamese',     stretch=0, width=160)
                                self.tree.column('japanese',     stretch=0, width=160)
                                self.tree.column('study_date', stretch=0, width=100)
                                self.tree.column('sentence', stretch=0, width=300)"""

        for col in self.dataCols:
            self.tree.heading(col,  text=col,  anchor=tk.W)
            self.tree.column(col,  stretch=0, width=160)

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

    def _build_vocabulary_data(self, status, study_date=None):
        # create a dict with a number as key, and randomized contents matching
        # the column layout of the table

        self.tree.delete(*self.tree.get_children())
        self.data = {}

        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        words = None
        if study_date == None:
            words = sqlVocab.query_words_with_status(status)
        else:
            words = sqlVocab.query_words_with_status_and_date(status, strftime("%Y-%m-%d", gmtime()))
        num = 0
        for w in words:
            num += 1
            self.data[num] = w

    def _query_vocabulary_data(self, sql):
        self.tree.delete(*self.tree.get_children())
        self.data = {}

        sqlVocab = SqliteVocabulary("studyenglish.db", "vocabulary")
        words = sqlVocab.query_words_with_sql(sql)
        num = 0
        for w in words:
            num += 1
            self.data[num] = w

    def _populate_tree(self):
        for n in range(len(self.data)):
            num = n+1
            item = self.data[num]
            tags = ('normal')
            '''
            if item[2] == 'word': # use highlight if status is 'timedout'
                tags = ('timedout')
            else:
                tags = ('normal')
            
            if item[0].lower() == item[0].upper(): # override styles if there's a 5 in the ipaddress
                tags = ['whacky']
            '''
            
            lst = list(item)
            lst[3] = posAttributes(item[3])['description']
            item = tuple(lst)
            #print posAttributes(item[1])['description']

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
                sqlVocab.insert_vocabulary(v, 1, "", "", strftime("%Y-%m-%d", gmtime()), sent)

    sqlVocab.commit()
    sqlVocab.close()

if __name__ == '__main__':
    #main()
    TreeViewVocabulary().mainloop()


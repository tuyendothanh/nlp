
import sqlite3

class SqliteVocabulary():
    """docstring for SqliteVocabulary"""
    def __init__(self, dbname, tbname):
        self.dbname = "studyenglish.db"
        self.tbname = tbname
        self.conn = sqlite3.connect(self.dbname) # or use :memory: to put it in RAM 
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # create a table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS """ + self.tbname + """ 
                  (word text, status integer, 
                  vietnamese text, japanese text, study_date text, sentence text)""")

    def insert_vocabulary(self, word, status, vietnamese, japanese, study_date, sentence):
        # insert some data
        self.cursor.execute('''INSERT INTO ''' + self.tbname + ''' (word, status, vietnamese, japanese, study_date, sentence) 
                VALUES (?,?,?,?,?,?)''',(word.lower(), status, vietnamese, japanese, study_date, sentence))
        
    def commit(self):
        # save data to database
        self.conn.commit()

    def close(self):
        # save data to database
        self.conn.close()

    def check_existed_word(self, word):
        sql = "SELECT * FROM " + self.tbname + " WHERE word=?"
        self.cursor.execute(sql, [(word)])
        # print(self.cursor.fetchone())
        return (self.cursor.fetchone())
        
    def query_words_with_status(self, status):
        sql = "SELECT * FROM " + self.tbname + " WHERE status=?"
        self.cursor.execute(sql, [(status)])
        return self.cursor.fetchall()  # or use fetchone()

    def delete_vocabulary(self):
        sql = """DELETE FROM """ +  self.tbname
        self.cursor.execute(sql)
        self.conn.commit()

    def update_word_status(self, word, status):
        sql = "UPDATE " + self.tbname + " SET status = "+str(status)+" WHERE word = ?"
        print(sql)
        self.cursor.execute(sql,[(word)])
        self.conn.commit()




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
                    (word text primary key, syntactic text,
                    vietnamese text, japanese text, sentence text, 
                    status integer, study_date text,
                    local_count integer default 0, global_count integer default 0)""")

    def insert_vocabulary(self, word, syntactic, vietnamese, japanese, sentence, status, study_date, local_count, global_count):
        # insert some data
        self.cursor.execute('''INSERT INTO ''' + self.tbname + 
                ''' (word, syntactic, vietnamese, japanese, sentence, status, study_date, local_count, global_count) 
                VALUES (?,?,?,?,?,?,?,?,?)''',(word, syntactic, vietnamese, japanese, sentence, status, study_date, local_count, global_count))
        
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
        if status != None:
            sql = "SELECT * FROM " + self.tbname + " WHERE status=?"
            self.cursor.execute(sql, [(status)])
        else:
            sql = "SELECT * FROM " + self.tbname
            self.cursor.execute(sql)
        return self.cursor.fetchall()  # or use fetchone()

    def query_words_with_status_and_date(self, status, study_date):
        if status != None:
            sql = "SELECT * FROM " + self.tbname + " WHERE status=? AND study_date=?"
            self.cursor.execute(sql, [(status),(study_date)])
        else:
            sql = "SELECT * FROM " + self.tbname
            self.cursor.execute(sql)
        return self.cursor.fetchall()  # or use fetchone()

    def query_words_with_sql(self, sql):
        sql = "SELECT * FROM " + self.tbname + " WHERE " + sql
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def delete_vocabulary(self):
        sql = """DELETE FROM """ +  self.tbname
        self.cursor.execute(sql)
        self.conn.commit()

    def update_word_status(self, word, status):
        sql = "UPDATE " + self.tbname + " SET status = "+str(status)+" WHERE word = ?"
        print(sql)
        self.cursor.execute(sql,[(word)])
        self.conn.commit()

    def get_col_names(self):
        self.cursor.execute("PRAGMA table_info('{}')".format(self.tbname))
        col_names = [x[1] for x in self.cursor.fetchall()]
        return col_names

    def update_word_count(self, word, lcnt, gcnt):
        # UPDATE Products SET Price = Price + 50 WHERE ProductID = 1
        sql = "UPDATE " + self.tbname + " SET local_count = local_count+" + str(lcnt) + ", global_count = global_count+" + str(gcnt) + " WHERE word = ?"
        # print(sql)
        self.cursor.execute(sql,[(word)])
        #self.conn.commit()

    def clear_local_count(self):
        # UPDATE Products SET Price = Price + 50 WHERE ProductID = 1
        sql = "UPDATE " + self.tbname + " SET local_count = 0"
        self.cursor.execute(sql)




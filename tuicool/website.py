# -*- coding:UTF-8 -*-

class WebsiteHelper:
    def __init__(self,conn):
        self.conn=conn

    def db_update_website(self,article_id,item):
        self.db_insert_website(item)
        website_id = self.db_select_website(item['web_name'])
        sql = 'INSERT INTO article_website(article_id,website_id) VALUES(%d,%d)' % (article_id,website_id)
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            rowcount=cur.execute(sql)
            print 'rowcount=',rowcount
            if rowcount==1:
                self.db_update_article_count(item['web_name'])
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        cur.close()

    def db_insert_website(self,item):
        sql = 'INSERT INTO website(name,logo) VALUES(\"%s\",\"%s\")' % (item['web_name'],item['web_logo'])
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        cur.close()

    def db_select_website(self,name):
        sql = 'SELECT id FROM website WHERE name = \"%s\"' % (name)
        print "sql:::", sql
        cur = self.conn.cursor()
        id = -1
        try:
            cur.execute(sql)
            row = cur.fetchone()
            id = row[0]
        except Exception,e:
            print e
            id = -1
        cur.close()
        return id

    def db_update_article_count(self,name):
        sql = 'UPDATE website SET article_count = article_count+1 WHERE name = \"%s\"' % (name)
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()

        cur.close()
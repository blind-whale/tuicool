# -*- coding:UTF-8 -*-

class TagHelper:
    def __init__(self,conn):
        self.conn=conn

    def db_update_tag(self,article_id,tags):
        taglist=tags.split(',')
        print 'taglist:',taglist
        for tag in taglist:
            if len(tag)!=0:
                self.db_insert_tag(tag)
                tag_id = self.db_select_tag(tag)
                sql = 'INSERT INTO article_tag(article_id,tag_id) VALUES(%d,%d)' % (article_id, tag_id)
                cur = self.conn.cursor()
                rowcount=0
                try:
                    rowcount = cur.execute(sql)
                    self.conn.commit()
                except Exception, e:
                    print e
                    self.conn.rollback()
                cur.close()

                if rowcount == 1:
                    self.update_tag_count(tag)



    def db_insert_tag(self,tag):
        sql = 'INSERT INTO tag(name) VALUES(\"%s\")' % (tag)
        cur = self.conn.cursor();
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        cur.close()

    def db_select_tag(self,tag):
        sql = 'SELECT id FROM tag WHERE name = \"%s\"' % (tag)
        id = -1
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            row= cur.fetchone()
            id = row[0]
        except Exception,e:
            print e
        cur.close()
        return id

    def update_tag_count(self,tag):
        sql = 'UPDATE tag SET article_count = article_count+1 WHERE name = \"%s\"' % (tag)
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit
        except Exception,e:
            print e
            self.conn.rollback()
        cur.close()

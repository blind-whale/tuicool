# -*- coding:UTF-8 -*-


class CategoryHelper:

    def __init__(self,conn):
        self.conn=conn

    # 更新category 分类表
    def db_update_category(self, id, category):
        self.db_insert_category(category)
        categroy_id = self.db_select_category(category)
        sql = 'INSERT INTO article_category(article_id,category_id) VALUES(%d,%d)' % (id, categroy_id)
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            rowcount=cur.execute(sql)
            print 'rowcount=',rowcount
            if rowcount==1:
                self.db_update_category_count(categroy_id)
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()
        cur.close()

    # 根据分类名称，获取分类id
    def db_select_category(self, category):
        sql = 'SELECT id FROM category WHERE name=\"%s\"' % (category)
        print "sql:::",sql
        cur = self.conn.cursor()
        id = -1
        try:
            cur.execute(sql)
            row = cur.fetchone();
            if row is not None:
                id = row[0]
        except Exception, e:
            print e
        cur.close()
        return id;

    # 插入一条新的分类
    def db_insert_category(self, category):
        sql = 'INSERT INTO category(name) VALUES(\"%s\")' % (category)
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()
        cur.close()

    # 根据分类id，更新分类文章数目
    def db_update_category_count(self, id):
        sql = 'UPDATE category SET article_count = article_count+1 WHERE id=%d' % (id)
        print "sql:::", sql
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()
        cur.close()
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import MySQLdb
import urllib
import os

class TuicoolPipeline(object):
    def process_item(self, item, spider):
        return item
		
class DbStorePipeline(object):
	
	@classmethod
	def from_crawler(cls,crawler):
		host = crawler.settings.get('MYSQL_HOST',None)
		dbname = crawler.settings.get('MYSQL_DBNAME',None)
		user = crawler.settings.get('MYSQL_USER',None)
		passwd = crawler.settings.get('MYSQL_PASSWD',None)
		return cls(host,dbname,user,passwd)
	
	def __init__(self,hostAddress,dbname,username,password):
		conn = MySQLdb.connect(host=hostAddress,port=3306,user=username,passwd=password,db=dbname,charset='utf8')
		self.conn = conn
	
	def process_item(self,item,spider):
		if item is None:
			return item
		query = self.db_select_by_title(item['title'])
		if query is None:
			self.db_insert(item)
		else:
			self.db_update(item,query)
		return item
	
	def close_spider(self,spider):
		self.conn.close()
	
	def db_select_by_title(self,title):
		sql = 'SELECT article_id,category,is_hot FROM tuicool WHERE title=\'%s\'' % title
		print 'sql:::',sql
		cur = self.conn.cursor()
		cur.execute(sql)
		result = cur.fetchone()
		item = None
		if result is not None:
			item = {
				'article_id':result[0],
				'category':result[1],
				'is_hot':result[2],
			}
		cur.close()
		return item
	
	def db_insert(self,item):
		sql = None
		if item.has_key('body'):
			sql = 'INSERT INTO tuicool(title,created_at,tag,body,web_name,origin_url,images)' + \
				' VALUES(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");'
			sql = sql % (item['title'],item['created_at'],item['tag'],item['body'],item['web_name'],item['origin_url'],str(item['images']))
		elif item.has_key('category') and item['category'] is not None:
			sql = 'INSERT INTO tuicool(title,thumb_image,category)' + \
				' VALUES(\"%s\",\"%s\",\"%s\");'
			sql = sql % (item['title'],item['thumb_image'],item['category'])
		else:
			sql = 'INSERT INTO tuicool(title,thumb_image,is_hot)' + \
				' VALUES(\"%s\",\"%s\",%d);'
			sql = sql % (item['title'],item['thumb_image'],item['is_hot'])
		
		print "sql:::",sql
		cur = self.conn.cursor()
		try:
			cur.execute(sql)
			self.conn.commit()
		except Exception,e:
			print e
			self.conn.rollback()
		cur.close()
	
	def db_update(self,item,query):
		sql = None
		if item.has_key('body'):
			sql = 'UPDATE tuicool SET created_at=\"%s\",tag=\"%s\",body=\"%s\",web_name=\"%s\",origin_url=\"%s\",images=\"%s\" WHERE article_id=%d;' % \
				(item['created_at'],item['tag'],item['body'],item['web_name'],item['origin_url'],str(item['images']),query['article_id'])
		elif item.has_key('category') and item['category'] is not None:
			sql = 'UPDATE tuicool SET title=\"%s\",thumb_image=\"%s\",category=\"%s\", WHERE article_id=%d;' % (item['title'],item['thumb_image'],item['category'],query['article_id'])
		else:
			sql = 'UPDATE tuicool SET title=\"%s\",thumb_image=\"%s\",is_hot=%d WHERE article_id=%d;' % (item['title'],item['thumb_image'],item['is_hot'],query['article_id'])
		print "sql:::", sql
		cur = self.conn.cursor()
		try:
			cur.execute(sql)
			self.conn.commit()
		except Exception,e:
			print e
			self.conn.rollback()


class ImageDownload(object):
	def process_item(self,item,spider):
		if item and item.has_key('images'):
			images = item['images']
			for index in range(len(images)):
				url = images[index]
				temp = url.split('/')
				name = temp[-1]
				filaname = os.path.join('/data/wwwroot/tuicool/articles/img/',name)
				if not os.path.exists(filaname):
					self.download(url,filaname)
				item['images'][index] = 'http://101.200.34.13:8080/articles/img/'+filaname
		return item

	def download(self,url,name):
		urllib.urlretrieve(url,filename=name)


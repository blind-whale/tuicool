#!/usr/python/bin
# -*- coding:UTF-8 -*-

from tuicool.items import TuicoolItem

import scrapy
import os


class TuicoolSpider(scrapy.spiders.Spider):
	name = 'hotArticles'
	start_urls =[
		'http://www.tuicool.com/ah',
	]
	allowed_domain = ['tuicool.com']
	hot_url = 'http://www.tuicool.com/ah/0'
	categories = {
		'http://www.tuicool.com/ah/101000000':'科技',
		'http://www.tuicool.com/ah/101040000':'创投',
		'http://www.tuicool.com/ah/101050000':'数码',
		'http://www.tuicool.com/ah/20':'技术',
		'http://www.tuicool.com/ah/108000000':'设计',
		'http://www.tuicool.com/ah/114000000':'营销',
	}
	
	def parse(self,response):
		# 请求地址
		url = response.url
		
		# tuicool表中的is_hot字段值
		is_hot = 0
		if url.startswith(TuicoolSpider.hot_url):# http://www.tuicool.com/ah/0/1?lang=1 最开始爬取网页的下一页
			is_hot = 1
		elif TuicoolSpider.start_urls[0]==url:# http://www.tuicool.com/ah  此为最开始爬取的网页
			is_hot = 1
			# 将科技、创投、数码、技术、设计、营销对应的列表页面，加入到爬取请求队列。此操作之执行一次
			for sel in response.css('div.span9 li'):
				category = sel.css('a::text').extract_first()
				category_url = sel.css('a::attr(href)').extract_first()
				category_url = response.urljoin(category_url)
				print 'category_url: ',category_url
				strs = self.split_nav_url(category_url)
				if strs is not None and TuicoolSpider.categories.has_key(strs[0]):
					yield scrapy.Request(category_url,callback=self.parse,priority=1)
		
		# 文章对应的分类
		category = None
		if is_hot!=1:
			category = self.get_article_category(url)
		
		# 对文章列表进行解析
		for sel in response.css('div.list_article_item'):
			#文章标题
			title = sel.css('div.title a::text').extract_first()
			# 文章列表的缩略图
			thumb_image = sel.css('div.article_thumb_image img::attr(src)').extract_first()
			#文章页面的地址
			article_url = sel.css('div.title a::attr(href)').extract_first()
			if article_url is not None:
				article_url=response.urljoin(article_url)
			
			yield {
				'title':title,
				'thumb_image':thumb_image,
				'url':article_url,
				'is_hot':is_hot,
				'category':category,
			}
			'''tuicoolitem=TuicoolItem()
			tuicoolitem['title']=title
			tuicoolitem['thumb_image']=thumb_image
			tuicoolitem['is_hot']=is_hot
			tuicoolitem['category']=category
			yield tuicoolitem'''
			# 将文章地址加入到爬取队列
			yield scrapy.Request(article_url,callback=self.parse_article,priority=0)
		
		# 将文章列表的下一页加入到爬取队列
		next_page = response.css('div.pagination li.next a::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			print '************next_page*************' + next_page
			yield scrapy.Request(next_page,callback = self.parse,priority=2)
	
	def parse_article(self,response):
		title = response.css('div.span8 h1::text').extract_first()
		created_at = response.css('div.article_meta span.timestamp::text').extract_first()
		print u'*************created_at*************%s' % (created_at)
		if created_at is not None:
			created_at = created_at.replace(u'时间','').strip()
		else:
			return
		web_name = response.css('div.article_meta span.from a::text').extract_first()
		origin_url = response.css('div.article_meta div.source a::text').extract_first()
		tag = ''
		for s in response.css('a span.new-label::text').extract():
			tag = tag +s+','
		images = []
		body = response.css('div.article_body').extract_first()
		for sel in response.css('div.article_body p'):
			temp=sel.css('img')
			for img in temp:
				image_url = img.css('img::attr(src)').extract_first()
				if image_url is not None:
					images.append(image_url)
					imagename = image_url.split('/')[-1]
					imagename='http://101.200.34.13:8080/articles/img/'+imagename;
					body = body.replace(image_url,imagename)
				continue
			#p=sel.css('p::text').extract_first()
			#p='  '+p+'\r\n'
			#body=body+p
		print '******images******',images

		os.chdir('/data/wwwroot/tuicool/articles')
		origin_dir=os.getcwd()
		body = u'<html><head><title>%s</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><style type=\"text/css\">img{max-width:100%%}</style></head><body>%s</body></html>' % (title,body)
		file_name=''+response.url.rpartition('/')[2]+'.html'
		if not os.path.exists(file_name):
			fbody=open(file_name,'wb')
			fbody.write(body)
			fbody.close()
		
		yield {
			'title':title,
			'created_at':created_at,
			'tag':tag,
			'body':'http://101.200.34.13:8080/articles/'+file_name,
			'web_name':web_name,
			'origin_url':origin_url,
			'images':images,
		}
	
	def split_nav_url(self,url):
		return url.split('?')
	
	#文章分类
	def get_article_category(self,url):
		strs = url.split('?')
		temp = None
		if len(strs) >= 2:
			temp = strs[0].rpartition('/')
		if temp is not None and len(temp)==3:
			strs[0]=temp[0]
		category = None
		if TuicoolSpider.categories.has_key(strs[0]):
			category = TuicoolSpider.categories[strs[0]]
		return category
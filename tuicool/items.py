# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuicoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	article_id = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field()
	created_at = scrapy.Field()
	thumb_image = scrapy.Field()
	category = scrapy.Field()
	is_hot = scrapy.Field()
	tag = scrapy.Field()
	images = scrapy.Field()
	body = scrapy.Field()
	web_name = scrapy.Field()
	web_url = scrapy.Field()
	origin_url = scrapy.Field()
	pass
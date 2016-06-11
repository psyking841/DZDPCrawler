# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    merchandise_name = scrapy.Field()
    merchandise_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    user_contribution = scrapy.Field()
    user_review_summary = scrapy.Field()
    user_review_tags = scrapy.Field()
    user_comment = scrapy.Field()
    comment_timestamp = scrapy.Field()

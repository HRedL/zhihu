# -*- coding: utf-8 -*-


import scrapy


class Review(scrapy.Item):
    # 评论内容
    is_anonymous = scrapy.Field()
    questioner_id = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()
    fullname = scrapy.Field()
    is_automatic = scrapy.Field()
    update_time = scrapy.Field()
    create_time = scrapy.Field()
    aid = scrapy.Field()



# -*- coding: utf-8 -*-


import scrapy


class PangTing(scrapy.Item):
    # 评论内容
    id = scrapy.Field()
    price = scrapy.Field()
    pangting_count = scrapy.Field()
    zan_count = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    user = scrapy.Field()



# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoyuanItem(scrapy.Item):
    # define the fields for your item here like:
    position = scrapy.Field()
    city = scrapy.Field()
    num = scrapy.Field()
    corporation = scrapy.Field()
    industry = scrapy.Field()
    xq_url = scrapy.Field()



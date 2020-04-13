# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VmgirlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_category = scrapy.Field()  # 分类
    file_dir_name = scrapy.Field()  #文件目录名字
    file_dir_href = scrapy.Field()  #文件目录名字
    image_url = scrapy.Field()  #文件目录名字

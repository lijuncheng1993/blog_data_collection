# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 个人资料信息
    Nickname=scrapy.Field() # 名字
    Gender = scrapy.Field() # 性别
    Adress = scrapy.Field() # 地区
    birthday = scrapy.Field()   # 生日
    VIPlevel = scrapy.Field()  # 会员等级
    Authentication = scrapy.Field()  # 认证信息
    Tewwts_number = scrapy.Field()  # 微博数
    Follows_numner = scrapy.Field()  # 关注数
    Fans_number = scrapy.Field()  # 粉丝数

# 用户

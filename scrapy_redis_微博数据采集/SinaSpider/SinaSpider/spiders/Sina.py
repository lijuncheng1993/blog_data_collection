# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import SinaspiderItem
from scrapy_redis.spiders import RedisSpider


class SinaSpider(scrapy.Spider):
    name = 'Sina'
    # allowed_domains = ['dddd']

    # start_urls = ['https://weibo.cn/5187664653/info']

    redis_key='Sina:start_urls'

    def parse(self, response):
        # 解析用户个人资料界面
        user_id = re.findall(r'(\d+)/info', response.url)
        items=SinaspiderItem()

        # 解析用户个人界面
        # print(response.text,'----------------------------------')
        # print('******************************************')
        # 302报警，网页重定向，需要利用cookies的内容 在中间件设置
        # pass
        print(response.xpath('//div[@class="c"]//text()').extract())
        text = ';'.join(response.xpath('//div[@class="c"]//text()').extract())
        print(text)
        print('*******************************')
        Nickname = re.findall(r'昵称:(.*?);', text)  # 名字
        Gender = re.findall(r'性别:(.*?);', text)  # 性别
        Adress = re.findall(r'地区:(.*?);',text)  # 地区
        birthday = re.findall(r'生日:(.*?);',text)  # 生日
        VIPlevel = re.findall(r'会员等级:(.*?);',text)  # 会员等级
        Authentication = re.findall(r'认证信息:(.*?);',text)  # 认证信息
        # Tewwts_number = re.findall(r'微博数:(.*?);',text)  # 微博数
        # Follows_numner = re.findall(r'关注数:(.*?);',text)  # 关注数
        # Fans_number = re.findall(r'粉丝数:(.*?);',text)  # 粉丝数

        if Nickname:
            items['Nickname'] = Nickname[0]
        if Gender:
            items['Gender'] = Gender[0]
        if Adress:
            items['Adress'] = Adress[0]
        if birthday:
            items['birthday'] = birthday[0]
        if VIPlevel:
            items['VIPlevel'] = VIPlevel[0]
        if Authentication:
            items['Authentication'] = Authentication[0]


        if user_id:
            yield scrapy.Request(url='https://weibo.cn/{}'.format(user_id[0]), callback=self.parse_index,meta={'items':items})

        if user_id:
        # 对粉丝关注页面发起请求
            yield scrapy.Request(url='https://weibo.cn/{}/fans'.format(user_id[0]),callback=self.parse_user_id)



    def parse_index(self, response):
        # 匹配首页用户的微博数 关注数 粉丝数
        items = response.meta.get('items')
        Tewwts_number = re.findall(r'微博\[(\d+)\]', response.text)  # 微博数
        Follows_numner = re.findall(r'关注\[(\d+)\]', response.text)  # 关注数
        Fans_number = re.findall(r'粉丝\[(\d+)\]', response.text)  # 粉丝数
        if Tewwts_number:
            items['Tewwts_number']=int(Tewwts_number[0])
        if Follows_numner:
            items['Follows_numner'] = int(Follows_numner[0])
        if Fans_number:
            items['Fans_number'] = int(Fans_number[0])

        yield  items

    def parse_user_id(self,response):
        # 解释用户的id值
        user_id_list=re.findall(r'https://weibo.cn/u/(\d+)"',response.text,re.S)

        for user_id in user_id_list:
            yield scrapy.Request(url='https://weibo.cn/{}/info'.format(user_id))

        # 翻页
        next_url=response.xpath('//a[text()="下页"]/@href').extract()
        if next_url:
            yield scrapy.Request(url='https;//weibo.cn'+next_url[0],callback=self.parse_user_id)
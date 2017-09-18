#!python2
#coding:utf8

from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from pprint import pprint

from ..items import *


class SchoolSpider(CrawlSpider):
    name = "school"
    allowed_domains = ["esf.wuhan.fang.com"]
    start_urls = [
        'http://esf.wuhan.fang.com/school/',
    ]
    rules = [
        Rule(sle(allow=("/school/[^/]*.htm$")), callback='parse_school_page', follow=True), #e.g. http://esf.wuhan.fang.com/school/4421.htm
        Rule(sle(allow=("/school/[^/,-]*/$")), follow=True),
    ]

    def parse_school_page(self, response):
        url = response.url
        name = response.css('div.wrap > p.schoolname > span.title::text').extract_first()
        ps = response.css('div.wrap > p.schoolname > span.info::text').extract_first()
        info_list = []
        house_list = response.xpath('/html/body/div[2]/div[2]/ul/li/div[2]/h3/a[1]/text()').extract()
        items = []
        item = SchoolItem()

        for info_item in response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/ul/li'):
            info_value = info_item.xpath('string(.)').extract_first()
            info_list.append(info_value)

        item['url'] = url
        item['name'] = name
        item['ps'] = ps
        item['info_list'] = info_list
        item['house_list'] = house_list

        items.append(item)
        return items



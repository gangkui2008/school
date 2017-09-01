# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import json
import unicodecsv as csv
from pprint import pprint
import datetime


class SchoolPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class CsvWriterPipeline(object):
    def open_spider(self, spider):
        today = datetime.date.today()
        format_today = today.strftime('%Y%m%d')
        self.file = open('武汉学校' + format_today + '.csv', 'wb')
        self.spamwriter = csv.writer(self.file, encoding='utf-8-sig')
        header = [u'学校', u'来源网址', u'学校概要', u'小区均价', u'在售房源', u'学校地址', u'周边小区', u'学校特色', u'学校电话', u'升学情况']
        self.spamwriter.writerow(header)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        row = self.extract_row_from_item(item)
        row = [(d if d else '').replace(',', ' ').replace(u'，', ' ') for d in row] #Replace comma with space as comma is a delimiter in csv
        self.spamwriter.writerow(row)
        return item

    def extract_row_from_item(self, item):
        name = ''
        url = ''
        ps = ''
        xiaoqujunjia = ''
        zaishoufangyuan = ''
        xuexiaodizhi = ''
        zhoubianxiaoqu = ''
        xuexiaotese = ''
        xuexiaodianhua = ''
        shengxueqingkuang = ''

        col_xiaoqujunjia = u'小区均价'
        col_zaishoufangyuan = u'在售房源'
        col_xuexiaodizhi = u'学校地址'
        col_zhoubianxiaoqu = u'周边小区'
        col_xuexiaotese = u'学校特色'
        col_xuexiaodianhua = u'学校电话'
        col_shengxueqingkuang = u'升学情况'
        maohao = u'：'

        pattern_xiaoqujunjia = re.compile(col_xiaoqujunjia)
        pattern_zaishoufangyuan = re.compile(col_zaishoufangyuan)
        pattern_xuexiaodizhi = re.compile(col_xuexiaodizhi)
        pattern_zhoubianxiaoqu = re.compile(col_zhoubianxiaoqu)
        pattern_xuexiaotese = re.compile(col_xuexiaotese)
        pattern_xuexiaodianhua = re.compile(col_xuexiaodianhua)
        pattern_shengxueqingkuang = re.compile(col_shengxueqingkuang)

        name = item['name']
        url = item['url']
        ps = item['ps']
        info_list = item['info_list']

        for info_item in info_list:
            if pattern_xiaoqujunjia.search(info_item):
                details = info_item.split(maohao)
                if len(details) > 1:
                    xiaoqujunjia = details[1]
            elif pattern_zaishoufangyuan.search(info_item):
                details = re.findall(r'\d+', info_item)
                if len(details) > 0:
                    zaishoufangyuan = details[0]
            elif pattern_xuexiaodizhi.search(info_item):
                details = info_item.split(maohao)
                if len(details) > 1:
                    xuexiaodizhi = details[1]
            elif pattern_zhoubianxiaoqu.search(info_item):
                details = re.findall(r'\d+', info_item)
                if len(details) > 0:
                    zhoubianxiaoqu = details[0]
            elif pattern_xuexiaotese.search(info_item):
                details = info_item.split(maohao)
                if len(details) > 1:
                    xuexiaotese = " ".join(re.findall(r'\S+', details[1]))
            elif pattern_xuexiaodianhua.search(info_item):
                details = info_item.split(maohao)
                if len(details) > 1:
                    xuexiaodianhua = details[1]
            elif pattern_shengxueqingkuang.search(info_item):
                details = info_item.split(maohao)
                if len(details) > 1:
                    shengxueqingkuang = " ".join(re.findall(r'\S+', details[1]))
            else:
                pass

        row = [name, url, ps, xiaoqujunjia, zaishoufangyuan, xuexiaodizhi, zhoubianxiaoqu, xuexiaotese, xuexiaodianhua, shengxueqingkuang]

        return row


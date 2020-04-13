import scrapy
import requests
import time

from vmgirls.items import VmgirlsItem


class VmgirlsSpider(scrapy.Spider):
    name = "vmgirls_spider"
    allowed_domaims = ["www.plmm.com.cn"]
    start_urls = ['https://www.plmm.com.cn']

    def parse(self, response):
        dir_list = response.xpath("//ul[@class='nav-list J_navMainList clearfix']/li[@class='nav-item']")
        for i_item in dir_list:
            item = VmgirlsItem()
            item['file_category'] = i_item.xpath("./a/text()").extract_first()
            next_href = i_item.xpath("./a/@href").extract_first().replace('//','http://',1)
            yield scrapy.Request(next_href, callback=self.lists, meta={'file_category': item['file_category']})

    def lists(self, response):
        dir_list = response.xpath("//div[@class='goods-list-box']//div[@class='goods-item']")
        item = VmgirlsItem()
        item['file_category'] = response.meta['file_category']
        for i_item in dir_list:
            item['file_dir_name'] = i_item.xpath(".//span//h3/a/text()").extract_first()
            item['file_dir_href'] = i_item.xpath(".//span//h3/a/@href").extract_first().replace('//','http://',1)
            yield scrapy.Request(item['file_dir_href'], callback=self.detail, method='GET',
                                 meta={'file_dir_name':item['file_dir_name'],'file_category':item['file_category']})
        next_url = response.xpath("//div[@class='common-page-box mt10 align-center']//span/a/@href").extract_first()
        if next_url:
            return scrapy.Request('https://www.plmm.com.cn'+next_url, callback=self.parse)

    # 进入详情页开始下载
    def detail(self, response):
        img_list = response.xpath("//ul[@class='grid effect-1']/a")
        img_urls = []
        item = VmgirlsItem()
        item['file_dir_name'] = response.meta['file_dir_name']
        item['file_category'] = response.meta['file_category']
        if img_list:
            for i_item in img_list:
                url = i_item.xpath("./img/@src").extract_first().replace('//','http://',1)
                url = url.replace('210', '900', 1)
                img_urls.append(url)
            item['image_url'] = img_urls
        return item
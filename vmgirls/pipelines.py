# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
import shutil
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
# 导入项目设置
from scrapy.utils.project import get_project_settings


class VmgirlsPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        for image_url in item['image_url']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains 没有图片")
        file_category = self.img_store+item['file_category']
        file_path = file_category+'/'+item['file_dir_name']
        # 定义分类保存的路径
        if not os.path.exists(file_category):
            os.mkdir(file_category)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        pic_list = []
        for v in image_paths:
            pic_name = v.replace('full/', '')
            # 移动图片
            shutil.move(self.img_store + '/full/' + pic_name, file_path + "\\" + pic_name)

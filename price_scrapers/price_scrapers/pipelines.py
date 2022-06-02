# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline



class FileDownloadPipeline(FilesPipeline):
    @classmethod
    def from_settings(cls, settings):
        return cls(store_uri="/tmp/out1.json",settings=settings)


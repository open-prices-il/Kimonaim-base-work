# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from urllib.parse import urlparse

from scrapy.exceptions import IgnoreRequest
from scrapy.pipelines.files import FileException, FilesPipeline, logger
from scrapy.utils.request import referer_str

from price_scrapers.items import DownloadLinkItem


def get_filename_from_url(url:str) ->str:
    a = urlparse(url)
    return os.path.basename(a.path)

class FileDownloadPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        if isinstance(item,DownloadLinkItem):

            url = request.url
            filename =get_filename_from_url(url)

            store = item.store
            res = f"full/{store}_{filename}"

            return res


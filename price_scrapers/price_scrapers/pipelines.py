# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from pathlib import Path
from urllib.parse import urlparse

import scrapy
from price_scrapers.items import DownloadLinkItem
from scrapy.exceptions import IgnoreRequest
from scrapy.pipelines.files import FileException, FilesPipeline, logger
from scrapy.utils.request import referer_str


def get_filename_from_url(url: str) -> str:
    a = urlparse(url)
    return os.path.basename(a.path)


class FileDownloadPipeline(FilesPipeline):
    def make_dir_if_not_exists(self, filename: str):
        base_path = os.path.dirname(filename)
        Path(base_path).mkdir(parents=True, exist_ok=True)

    def file_path(self, request, response=None, info=None, *, item=None):
        if isinstance(item, DownloadLinkItem):

            url = request.url
            filename = get_filename_from_url(url)

            store = item.chain
            category = item.category
            res = f"full/{store}_{category}_{filename}"
            self.make_dir_if_not_exists(res)

            return res

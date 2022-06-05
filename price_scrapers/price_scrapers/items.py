# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DownloadLinkItem:
    file_urls: List[str]
    chain: str
    branch_string: Optional[str]
    category: str
    update_time_str: str

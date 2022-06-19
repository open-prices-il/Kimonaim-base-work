from typing import Iterator, Optional

import scrapy
from price_scrapers.items import DownloadLinkItem
from scrapy import Selector
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


def strip_if_not_none(string: Optional[str]) -> Optional[str]:
    if string is not None:
        return string.strip()


import re


class YaynotBitanParentSpider(scrapy.spiders.CrawlSpider):
    """
    Crawls Yaynot bitan's main page, and triggers a second spider to download files for ech day
    """

    name = "ybp"
    base_url = "http://publishprice.ybitan.co.il"
    start_urls = [f"{base_url}/"]
    rules = [
        Rule(LinkExtractor(allow=["/20\d+/$"], deny=["\.gz"]), callback="parse_page"),
    ]

    def parse_page(self, response):
        li = LinkExtractor(allow=["PriceFull.+\.gz"])
        filename_split_reg = re.compile(
            "(?P<category>[A-z]+)\d+-(?P<branch>\d+)-(?P<date>\d+)"
        )

        for link in li.extract_links(response):
            url: str = link.url
            match = filename_split_reg.search(url)
            match_gd = match.groupdict()

            yield DownloadLinkItem(
                chain=self.name,
                file_urls=[url],
                branch_string=strip_if_not_none(match_gd["branch"]),
                update_time_str=strip_if_not_none(match_gd["date"]),
                category=strip_if_not_none(match_gd["category"]),
            )


class MegaScrape(YaynotBitanParentSpider):
    name = "mega"
    base_url = "http://publishprice.mega.co.il"
    start_urls = [f"{base_url}/"]


class MegaMarketScrape(YaynotBitanParentSpider):
    name = "mega-market"
    base_url = "http://publishprice.mega-market.co.il"
    start_urls = [f"{base_url}/"]

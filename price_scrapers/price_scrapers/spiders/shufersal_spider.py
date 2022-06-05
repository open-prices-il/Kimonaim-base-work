from typing import Optional

import scrapy
from scrapy import Selector
from scrapy.http import Response

from price_scrapers.items import DownloadLinkItem

def strip_if_not_none(string:Optional[str]) -> Optional[str]:
    if string is not None:
        return string.strip()



class ShufersalSpider(scrapy.Spider):
    name = "shufersal"
    base_url = "http://prices.shufersal.co.il"
    start_urls = [f"{base_url}/?sort=Time&sortdir=ASC&page=1"]
    next_page_xpath = "//a[text()='>']/@href"

    @staticmethod
    def row_xpath_iterator(rows_per_page=20):
        for i in range(1, rows_per_page + 1):
            yield f"""/html/body/div[2]/div[5]/div/table/tbody/tr[{i}]"""

    def get_next_page_url(self, response: Response) -> Optional[str]:
        next_page_item: Optional[str] = response.xpath(self.next_page_xpath).get()
        if next_page_item:
            next_page_url = self.base_url + next_page_item
            return next_page_url

    def row_to_item(self, row_selector: Selector) -> DownloadLinkItem:
        link = row_selector.xpath("td[1]/a/@href").get()
        update_time_str = row_selector.xpath("td[2]/text()").get()
        category = row_selector.xpath("td[5]/text()").get()
        branch = row_selector.xpath("td[6]/text()").get()

        return DownloadLinkItem(
            chain=self.name,
            file_urls=[link],
            branch_string=strip_if_not_none(branch),
            update_time_str=strip_if_not_none(update_time_str),
            category=strip_if_not_none(category),
        )

    def parse(self, response: Response):
        for row_xpath in self.row_xpath_iterator():
            for row in response.xpath(row_xpath):
                item = self.row_to_item(row)
                yield item

        next_page_url = self.get_next_page_url(response)
        if next_page_url:
            request = scrapy.Request(url=next_page_url)
            yield request

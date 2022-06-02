import scrapy
from scrapy import Selector
from scrapy.http import Response

from price_scrapers.items import DownloadLinkItem


class ShufersalSpider(scrapy.Spider):
    name = "shufersal"
    start_urls  = ["http://prices.shufersal.co.il/"]
    @staticmethod
    def row_xpath_iterator(rows_per_page=20):
        for i in range(1,rows_per_page+1):
            yield f'''/html/body/div[2]/div[5]/div/table/tbody/tr[{i}]'''
    def parse(self, response:Response):
        for row_xpath in self.row_xpath_iterator():
            for row  in response.xpath(row_xpath):
                link =row.xpath("td[1]/a/@href").get()
                yield DownloadLinkItem(file_urls=link)


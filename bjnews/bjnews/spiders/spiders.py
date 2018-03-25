import datetime
import re
import uuid

from scrapy import Request
from scrapy import Selector
from scrapy import Spider

from bjnews.items import BjnewsItem

check_value = lambda x: x if x else ""


class BjNews(Spider):
    name = "bjnews"

    allowed_domains = ['bjnews.com.cn']

    start_urls = ['http://epaper.bjnews.com.cn/']
    # start_urls = ['http://epaper.bjnews.com.cn/html/2013-07/24/node_1.htm']

    def parse(self, response):
        # 解析
        for request in self.parse_page(response):
            yield request

        pre_url = self.parse_pre_day_url(response)
        yield Request(pre_url)

    # 获取上一天的链接
    def parse_pre_day_url(self, response):
        curl = response.url
        date_arr = re.findall("(\d{4})-(\d{2})/(\d{2})", curl)
        if date_arr and len(date_arr[0]) == 3:
            date = datetime.datetime(int(date_arr[0][0]), int(date_arr[0][1]), int(date_arr[0][2]))
            pre_date = date - datetime.timedelta(days=1)

            pre_url = "http://epaper.bjnews.com.cn/html/"
            tail_url = "/node_1.htm"
            return pre_url + pre_date.strftime('%Y-%m/%d') + tail_url
        return None

    # 获取所有的版面
    def parse_page(self, response):
        sel = Selector(response)
        a_div = sel.xpath("//*[@id='pageLink']")
        for a in a_div:
            url = a.xpath("./@href").extract_first()
            page_info = a.xpath("./text()").extract_first()
            if url:
                yield Request(url=response.urljoin(url),
                              callback=self.parse_all_article,
                              meta={
                                  "page_info": page_info
                              },
                              priority=2)

    # 获取版面的所有文章
    def parse_all_article(self, response):
        sel = Selector(response)
        page_info = response.meta["page_info"]
        page_urls = sel.xpath("//map/area/@href").extract()
        for url in page_urls:
            yield Request(url=response.urljoin(url),
                          callback=self.parse_content,
                          meta={
                              "page_info": page_info
                          },
                          priority=3)
        pass

    # 解析文章内容
    def parse_content(self, response):
        sel = Selector(response)
        page_info = response.meta["page_info"]
        item = BjnewsItem()
        item["id"] = uuid.uuid4()

        item["page_info"] = page_info

        url = response.url
        date_arr = re.findall("(\d{4})-(\d{2})/(\d{2})", url)
        date = datetime.datetime(int(date_arr[0][0]), int(date_arr[0][1]), int(date_arr[0][2]))
        item["date"] = date.strftime("%Y-%m-%d")

        first_title = sel.xpath('//div[@class="rit"]/h1/text()').extract_first()
        second_title = sel.xpath('//div[@class="rit"]/p/text()').extract_first()
        item["first_title"] = check_value(first_title)
        item["second_title"] = check_value(second_title)

        content = sel.xpath("//founder-content/p/text()").extract()
        if content:
            item["content"] = "".join(content)
        else:
            item["content"] = ""

        item["parse_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")

        return item

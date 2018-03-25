import datetime
import re
import uuid

from scrapy import Request
from scrapy import Selector
from scrapy import Spider

from peoplePaper.items import PeoplePaperItem

check_value = lambda x: x if x else ""


class PeoplePaperSpider(Spider):
    name = "peoplePaper"

    allowed_domains = ['people.com.cn']

    start_urls = ['http://paper.people.com.cn/']

    def parse(self, response):
        for url_or_request in self.parse_page_info(response):
            yield url_or_request

        next_url = self.parse_next_date_url(response)

        if next_url:
            yield Request(next_url)

    # 获取下一期的url
    def parse_next_date_url(self, response):
        curl = response.url
        date_arr = re.findall("(\d{4})-(\d{2})/(\d{2})", curl)
        if date_arr and len(date_arr[0]) == 3:
            date = datetime.datetime(int(date_arr[0][0]), int(date_arr[0][1]), int(date_arr[0][2]))
            pre_date = date - datetime.timedelta(days=1)

            pre_url = "http://paper.people.com.cn/rmrb/html/"
            tail_url = "/nbs.D110000renmrb_01.htm"
            return pre_url + pre_date.strftime('%Y-%m/%d') + tail_url
        return None

    # 解析第一版面，获取每一期的版面信息
    def parse_page_info(self, response):
        sel = Selector(response)

        page_urls = sel.xpath("//a[@id='pageLink']/@href").extract()
        page_titles = sel.xpath("//a[@id='pageLink']/text()").extract()

        # 获取第一版的文章URL
        yield self.get_article_request(response, page_titles[0])

        # 获取第二版之后的文章信息
        for (page_url, page_title) in zip(page_urls[1:], page_titles[1:]):
            yield Request(response.urljoin(page_url),
                          callback=self.get_article_request,
                          meta={
                              "page_title": page_title
                          },
                          priority=2)

    # 获取每版文章的URL
    def get_article_request(self, response, page_title=None):
        if not page_title:
            page_title = response.meta["page_title"]
        sel = Selector(response)
        article_urls = sel.xpath("//div[@id='titleList']/ul/li/a/@href").extract()

        for url in map(response.urljoin, article_urls):
            yield Request(url=url,
                          callback=self.parse_content,
                          meta={
                              "page_title": page_title
                          },
                          priority=3)

    # 获取每一版的文章信息
    def parse_content(self, response):
        sel = Selector(response)
        page_title = response.meta["page_title"]

        url = response.url
        date_arr = re.findall("(\d{4})-(\d{2})/(\d{2})", url)
        date = datetime.datetime(int(date_arr[0][0]), int(date_arr[0][1]), int(date_arr[0][2]))

        item = PeoplePaperItem()
        item["id"] = uuid.uuid4()
        item["page_info"] = page_title
        item["date"] = date.strftime("%Y-%m-%d")

        first_title = sel.xpath('//div[@class="text_c"]/h3/text()').extract_first()
        second_title = sel.xpath('//div[@class="text_c"]/h1/text()').extract_first()
        author = sel.xpath('//div[@class="text_c"]/h4/text()').extract_first()

        item["first_title"] = check_value(first_title)
        item["second_title"] = check_value(second_title)
        item["author"] = check_value(author)

        content = sel.xpath('//div[@id="ozoom"]/p/text()').extract()
        if content:
            item["content"] = "".join(content)
        else:
            item["content"] = ""

        item["parse_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")

        return item

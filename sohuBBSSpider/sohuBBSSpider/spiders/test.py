from scrapy import Selector
from scrapy import Spider

from sohuBBSSpider.spiders.author import get_author_item
from sohuBBSSpider.spiders.post import get_post_item
from sohuBBSSpider.spiders.post_list import get_post_list_div, get_post_author_list


class Test(Spider):
    name = 'test'

    allowed_domains = ['sohu.com']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://yule.club.sohu.com/zz2286/thread/41pptlzhawg']

    def parse(self, response):
        sel = Selector(response)
        # ss = get_post_list_div(response, '#bbs_postlist')
        # print(ss)

        author_item = get_post_item(response)

        yield author_item

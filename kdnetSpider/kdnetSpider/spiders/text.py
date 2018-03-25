from scrapy import Request
from scrapy import Spider

from kdnetSpider.items import PostItem
from kdnetSpider.spiders.author import get_author_info
from kdnetSpider.spiders.category import get_last_cate_num
from kdnetSpider.spiders.comment import get_comment_info
from kdnetSpider.spiders.post import get_post_info


class KDNetSpider(Spider):
    def __init__(self):
        self.cate_num_dict = get_last_cate_num()

    name = 'text'

    allowed_domains = [
        'kdnet.net'
    ]

    start_urls = ['http://club.kdnet.net/dispbbs.asp?s=share&id=12128155&boardid=1']

    def parse(self, response):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse_test
            )

    def parse_test(self, response):
        # post_item = PostItem()
        # get_post_info(response, post_item)
        # yield post_item
        # get_author_info(response, '101', '10')

        for comment_item in get_comment_info(response, '12345678'):
            yield comment_item

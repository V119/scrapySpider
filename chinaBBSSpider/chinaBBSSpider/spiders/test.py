from scrapy import Spider

from chinaBBSSpider.spiders.comment import get_comment_prise


class Test(Spider):
    name = 'test'

    # start_urls = ['http://weibo.com/p/1005056091206703/home?from=page_100505_profile&wvr=6&mod=data&is_all=1#place']
    start_urls = [
        'http://club.china.com/data/thread/1011/2789/93/01/2_1.html',
    ]

    def parse(self, response):
        jobj = get_comment_prise(response)


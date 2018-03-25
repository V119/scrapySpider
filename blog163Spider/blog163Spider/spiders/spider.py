from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from blog163Spider.spiders.author import get_author_item
from blog163Spider.spiders.comment import get_comment_item
from blog163Spider.spiders.post import get_post_item


class Blog163Spider(CrawlSpider):
    name = '163_blog'

    allowed_domains = ['blog.163.com']

    start_urls = ['http://blog.163.com/']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/blog/static/\d+',
        ),
        allow_domains=(
            'blog.163.com'
        ),
        deny=(
            '/\$%7BblogDetail',
            '/\$%7Bx\.',
            '/\$%7Bfurl',
        ),
        # deny_domains=(
        #
        # )
    )

    author_extract = LxmlLinkExtractor(
        allow=(
            '/profile/$',
            '/profile$',
        ),
        allow_domains=(
            'blog.163.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'blog.163.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        Rule(follow_extract, follow=True, callback='parse_follow'),
        # Rule(follow_extract, follow=True),
    )

    a_count = 0
    p_count = 0
    f_count = 0

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)

        yield author_item

    def parse_follow(self, response):
        self.f_count += 1
        print('follow: ', self.f_count, '  ', response.url)

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)
        yield post_item

        for comment_item in get_comment_item(response, post_item['id']):

            yield comment_item

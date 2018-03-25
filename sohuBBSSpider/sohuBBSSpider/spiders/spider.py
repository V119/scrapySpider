from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from sohuBBSSpider.items import FansItem
from sohuBBSSpider.spiders import fans
from sohuBBSSpider.spiders.author import get_author_item
from sohuBBSSpider.spiders.comment import get_comment_items, get_comment_next_page_url
from sohuBBSSpider.spiders.fans import get_user_list, get_user_next_page
from sohuBBSSpider.spiders.post import get_post_item
from sohuBBSSpider.spiders.post_list import get_post_author_list


class Blog163Spider(CrawlSpider):
    name = 'sohu_bbs'

    allowed_domains = ['sohu.com']

    start_urls = ['http://club.sohu.com/index.php']

    author_extract = LxmlLinkExtractor(
        allow=(
            '/u/info',
        )
    )

    post_extract = LxmlLinkExtractor(
        allow=(
            '/thread/[a-z0-9]+',
        ),
        allow_domains=(
            'sohu.com'
        ),
        # deny=(
        #
        # ),
        deny_domains=(
            'passport.sohu.com',
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow=(
            'club.*sohu\.com/.*',
        ),
        allow_domains=(
            'sohu.com',
        ),
        deny=(
            '/reply\?floor=-1$',
            'action=search',
            'action=help',
            '/threads\?',
            '/u/fan\?',
            '/u/follow\?',
        ),
        deny_domains=(
            'passport.sohu.com',
        )
    )

    list_extract = LxmlLinkExtractor(
        allow=(
            '/threads',
            '/threads/$',
        ),
        allow_domains=(
            'sohu.com'
        ),
        deny=(
            '/reply\?floor=-1$',
            'action=search',
            '/threads\?',
        ),
        deny_domains=(
            'passport.sohu.com',
        )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(list_extract, follow=True, callback='parse_list'),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )

    # a_count = 0
    # p_count = 0
    # f_count = 0
    # l_count = 0

    def parse_author(self, response):
        author_item = get_author_item(response)

        yield author_item

        if author_item['author_id']:
            fans_url = 'http://i.club.sohu.com/u/fan?sp=' + author_item['author_id']
            friends_url = 'http://i.club.sohu.com/u/follow?sp=' + author_item['author_id']

            yield Request(
                url=fans_url,
                callback=self.parse_fans,
                meta={
                    'author_id': author_item['author_id']
                }
            )

            yield Request(
                url=friends_url,
                callback=self.parse_friends,
                meta={
                    'author_id': author_item['author_id']
                }
            )


    # def parse_follow(self, response):
    #     if '/u/info' in response.url:
    #         print('xxxx  ' + response.url)
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)

        post_item = get_post_item(response)

        for comment_item in get_comment_items(response):
            post_item['comment_ids'].append(comment_item['comment_id'])
            yield comment_item

        next_page = get_comment_next_page_url(response)
        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_comment_info,
                meta={
                    'post_item': post_item
                }
            )
        else:
            yield post_item

    def parse_list(self, response):
        for post_href, author_list in get_post_author_list(response):
            yield Request(
                url=post_href,
                callback=self.parse_post
            )

            for author_href in author_list:
                yield Request(
                    url=author_href,
                    callback=self.parse_author
                )

    def parse_comment_info(self, response):
        post_item = response.meta['post_item']
        for comment_item in get_comment_items(response):
            post_item['comment_ids'].append(comment_item['comment_id'])
            yield comment_item

        next_page = get_comment_next_page_url(response)
        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_comment_info,
                meta={
                    'post_item': post_item
                }
            )
        else:
            yield post_item

    def parse_fans(self, response):
        tag_name = '#middle_fans_list_bp'
        author_id = response.meta['author_id']
        user_list = get_user_list(response, tag_name)

        for user_id, user_href in user_list:
            fans_item = FansItem()
            fans_item['fans'] = user_id
            fans_item['follow'] = author_id

            yield fans_item

            yield Request(
                url=user_href,
                callback=self.parse_author,
            )

        if user_list and len(user_list) > 19:
            next_page_url = get_user_next_page(response, tag_name)
            if next_page_url:
                yield Request(
                    url=next_page_url,
                    callback=self.parse_fans,
                    meta={
                        'author_id': author_id
                    }
                )

    def parse_friends(self, response):
        tag_name = '#middle_friends_list_bp'
        author_id = response.meta['author_id']
        user_list = get_user_list(response, tag_name)

        for user_id, user_href in user_list:
            fans_item = FansItem()
            fans_item['fans'] = author_id
            fans_item['follow'] = user_id

            yield fans_item

            yield Request(
                url=user_href,
                callback=self.parse_author,
            )

        if user_list and len(user_list) > 19:
            next_page_url = get_user_next_page(response, tag_name)
            if next_page_url:
                yield Request(
                    url=next_page_url,
                    callback=self.parse_friends,
                    meta={
                        'author_id': author_id
                    }
                )



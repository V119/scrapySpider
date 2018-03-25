from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from xinhuaNewsSpider.spiders.get_info import *


class PeopleSpider(CrawlSpider):
    name = 'xinhuaNews'

    allowed_domains = ['xinhuanet.com', 'news.cn']

    start_urls = ['http://www.news.cn/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/\d{4}-\d{2}/\d{2}/[a-zA-Z]+_\d+.htm',
            '/\d{6}/\d+_[a-zA-Z].htm',
        ),
        allow_domains=(
            'xinhuanet.com',
            'news.cn'
        ),
        deny_domains=(
            'home.news.cn',
            'forum.xinhuanet.com',          # 论坛
            'kr.xinhuanet.com',             # 韩国频道
            'mongolian.news.cn',            # 蒙古
            'xizang.news.cn',               # 西藏

        ),
        deny=(
            'news.xinhuanet.com/video/'
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'xinhuanet.com',
            'news.cn'
        ),
        deny_domains=(
            'home.news.cn',
            'forum.xinhuanet.com',           # 论坛
            'kr.xinhuanet.com',
            'mongolian.news.cn',             # 蒙古
            'xizang.news.cn',                # 西藏
        ),
        deny=(
            'news.xinhuanet.com/video/'
        )
    )

    rules = (
        Rule(article_extract, follow=True, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )
    #
    # a_count = 0
    # f_count = 0

    def parse_article(self, response):
        sel = Selector(response)
        # self.a_count += 1
        # print('article:  ' + str(self.a_count) + '   ' + response.url)

        news_1_div = sel.xpath('//div[@id="center"]/div[@id="article"] | //td/div[@id="Content"]//span[@id="content"]')
        science_div = sel.xpath('//div[@class="content"]/div[@class="c_left"]')
        news_old_div = sel.xpath('//div[@id="content"]/div[@id="article"]')
        daily_div = sel.xpath('//font[@id="Zoom"]')
        pic_div = sel.xpath('//div[@class="conW"]/div[@class="content"] | '
                            '//div[@class="detail_body"]/div[@class="content_main clearfix"] | '
                            '//*[@class="bai13"]')
        data_news_div = sel.xpath('//div[@class="main"]/div[@class="article"]')
        global_div = sel.xpath('//body[@bgcolor]/div[@align="center"]/table[@width]')
        bj_div = sel.xpath('//div[@id="page"]/div[@id="mains"]  | //div[@id="page"]/div[@id="main"]')
        mrdx_div = sel.xpath('//td[@class="fs16 bl lh30"]/div[@id="Content"]')
        politics_div = sel.xpath('//div[@class="main pagewidth"]/div[@id="content"] '
                                 '| //div[@class="c_left"]/div[@id="content"]')
        world_div = sel.xpath('//div[@id="contentblock"]/span[@id="content"]')
        asia_news_div = sel.xpath('//div[@class="ej_box"]')

        if news_1_div:
            page_urls, news_item = get_news_1_info(response)
            page_index = 0
            if page_urls:
                yield Request(
                    url=response.urljoin(page_urls[page_index]),
                    callback=self.parse_next_page_info,
                    meta={
                        'item': news_item,
                        'page_list': page_urls,
                        'page_index': page_index + 1,
                        'parse_func': {
                            'content': get_news_1_content,
                            'picture_urls': get_news_1_pic_urls
                        }
                    }
                )

            yield news_item
        elif science_div:
            news_item = get_science_info(response)

            yield news_item
        elif news_old_div:
            news_item = get_old_news_info(response)

            yield news_item
        elif daily_div:
            news_item = get_daily_news_info(response)

            yield news_item
        elif pic_div:
            next_pages, news_item = get_pic_news_info(response)
            page_index = 0
            if next_pages:
                yield Request(
                    url=response.urljoin(next_pages[page_index]),
                    callback=self.parse_next_page_info,
                    meta={
                        'item': news_item,
                        'page_list': next_pages,
                        'page_index': page_index + 1,
                        'parse_func': {
                            'content': get_pic_content,
                            'picture_urls': get_pic_pic_url
                        }
                    }
                )
            else:
                yield news_item
        elif data_news_div:
            news_item = get_data_news_info(response)

            yield news_item
        elif global_div:
            news_item = get_global_news_info(response)

            yield news_item
        elif bj_div:
            news_item = get_bj_news_info(response)

            yield news_item
        elif mrdx_div:
            news_item = get_mrdx_news_info(response)

            yield news_item
        elif politics_div:
            news_item = get_politics_news_info(response)

            yield news_item
        elif world_div:
            next_pages, news_item = get_world_news_info(response)
            page_index = 0
            if next_pages:
                yield Request(
                    url=response.urljoin(next_pages[page_index]),
                    callback=self.parse_next_page_info,
                    meta={
                        'item': news_item,
                        'page_list': next_pages,
                        'page_index': page_index + 1,
                        'parse_func': {
                            'content': get_world_content,
                            'picture_urls': get_word_pic_urls
                        }
                    }
                )
            else:
                yield news_item
        elif asia_news_div:
            news_item = get_asia_news_div(response)

            yield news_item
        else:
            raise ValueError('Page style not in list: ' + response.url)

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow:  ' + str(self.f_count) + '   ' + response.url)

    def parse_next_page_info(self, response):
        news_item = response.meta['item']
        page_list = response.meta['page_list']
        page_index = response.meta['page_index']

        parse_func_dict = response.meta['parse_func']
        for key in parse_func_dict:
            func_value = parse_func_dict[key](response)
            if key in news_item.fields and news_item[key]:
                if isinstance(news_item[key], dict):
                    news_item[key].update(func_value)
                else:
                    news_item[key] += func_value

        if len(page_list) > page_index:
            yield Request(
                url=response.urljoin(page_list[page_index]),
                callback=self.parse_next_page_info,
                meta={
                    'item': news_item,
                    'page_list': page_list,
                    'page_index': page_index + 1,
                    'parse_func': parse_func_dict
                }
            )
        else:
            yield news_item

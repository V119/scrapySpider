#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from sina_news_spider.items import NewsItem

check_value = lambda x: x.strip() if x and isinstance(x, str) else ''
urljoin_list = lambda r, x: [r.urljoin(y) for y in x if y] if x else []


def get_news_1_info(response):
    sel = Selector(response)
    news_item = NewsItem()

    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    path_div = sel.xpath('//div[contains(@class, "site-header")]/div[@class="bread"]/a')
    path_text, path_href = get_path(response, path_div)
    news_item['path_text'] = check_value(path_text)
    news_item['path_url'] = path_href

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="artibodyTitle"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    participant_num = sel.xpath('//*[@id="commentCount1"]/text()').extract_first()
    news_item['participant_num'] = participant_num if participant_num else '0'

    published_time = sel.xpath('//meta[@property="article:published_time"]/@content').extract_first()
    news_item['date_time'] = check_value(published_time)

    comment_id = sel.xpath('//meta[@name="comment"]/@content').extract_first()
    news_item['comment_id'] = check_value(comment_id)

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    editor = sel.xpath('//p[@class="article-editor"]').xpath('string(.)').extract_first()
    news_item['editor'] = check_value(editor)

    media_div = sel.xpath('//span[@data-sudaclick="media_name"]/a')
    media_text = media_div.xpath('string(.)').extract_first()
    media_href = media_div.xpath('./@href').extract_first()

    news_item['from_media'] = check_value(media_text)
    news_item['from_media_url'] = check_value(media_href)

    content = sel.xpath('//div[@id="artibody"]//p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    pic_urls = sel.xpath('//div[@id="artibody"]//img/@src').extract()
    news_item['picture_urls'] = urljoin_list(response, pic_urls)

    return news_item


def get_news_2_info(response):
    sel = Selector(response)
    news_item = NewsItem()

    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    path_div = sel.xpath('//div[@class="path"]/div/a')
    path_text, path_href = get_path(response, path_div)
    news_item['path_text'] = check_value(path_text)
    news_item['path_url'] = path_href

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="main_title"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    participant_num = sel.xpath('//*[@id="commentCount1"]/text()').extract_first()
    news_item['participant_num'] = participant_num if participant_num else '0'

    date_time = sel.xpath('//span[@class="time-source"]/span[@class="titer"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time)

    comment_id = sel.xpath('//meta[@name="comment"]/@content').extract_first()
    news_item['comment_id'] = check_value(comment_id)

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    editor = sel.xpath('//p[@class="article-editor"]').xpath('string(.)').extract_first()
    news_item['editor'] = check_value(editor)

    from_div = sel.xpath('//span[@class="source"]/a')
    from_href = from_div.xpath('./@href').extract_first()
    from_text = from_div.xpath('string(.)').extract_first()
    news_item['from_media'] = check_value(from_text)
    news_item['from_media_url'] = check_value(from_href)

    content = sel.xpath('//div[@id="artibody"]//p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    pic_urls = sel.xpath('//div[@id="artibody"]//img/@src').extract()
    news_item['picture_urls'] = urljoin_list(response, pic_urls)

    return news_item


def get_pic_info(response):
    sel = Selector(response)
    news_item = NewsItem()

    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    news_item['path_text'] = '新浪图片'
    news_item['path_url'] = 'http://photo.sina.com.cn/'

    key_words = sel.xpath('//meta[@name="keywords"]/@content |'
                          ' //meta[@name="Keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@property="og:url"]/@content').extract_first()
    if not news_id:
        news_id = response.url
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//meta[@property="og:title"]/@content').extract_first()
    if not title:
        title = sel.xpath('//title/text()').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@property="og:description"]/@content').extract_first()
    if not description:
        description = sel.xpath('//meta[@name="Description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    # participant_num = sel.xpath('//a[@class="more J_Comment_Count_Txt"]/span[@class="f_red"]/text()').extract()
    # news_item['participant_num'] = participant_num[-1]
    news_item['participant_num'] = '-1'

    date_time = sel.xpath('//meta[@property="article:published_time"]/@content').extract_first()
    if not date_time:
        date_time = sel.xpath('//*[@id="eData"]/dl[1]/dd[4]/text()').extract_first()
    news_item['date_time'] = date_time

    comment_id = '-1'
    news_item['comment_id'] = comment_id

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    editor = sel.xpath('//meta[@name="Editor"]/@content').extract_first()
    news_item['editor'] = check_value(editor)

    news_item['from_media'] = '新浪'
    news_item['from_media_url'] = 'http://slide.mil.news.sina.com.cn/'

    content_list = []
    picture_url_list = []
    picture_div = sel.xpath('//*[@id="eData"]/dl')
    for picture_info in picture_div:
        picture_url = picture_info.xpath('./dd[1]/text()').extract_first()
        picture_text = picture_info.xpath('./dd[5]/text()').extract_first()
        content_list.append(check_value(picture_text))
        picture_url_list.append(check_value(picture_url))

    news_item['content'] = content_list
    news_item['picture_urls'] = urljoin_list(response, picture_url_list)

    return news_item


def get_discuss_info(response):
    sel = Selector(response)

    news_item = NewsItem()
    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    news_item['path_text'] = '网易评论'
    news_item['path_url'] = 'http://news.sina.com.cn/opinion/'

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="artibodyTitle"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    date_time = sel.xpath('//*[@id="pub_date"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time)

    comment_id = sel.xpath('//meta[@name=comment]/@content').extract_first()
    news_item['comment_id'] = check_value(comment_id)

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    editor = sel.xpath('//p[@class="article-editor"]').xpath('string(.)').extract_first()
    news_item['editor'] = check_value(editor)

    news_item['from_media'] = '网易新闻'
    news_item['from_media_url'] = 'http://news.sina.com.cn/opinion/'

    content = sel.xpath('//*[@id="artibody"]//p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    img_url = sel.xpath('//*[@id="artibody"]//img/@src').extract()
    news_item['picture_urls'] = urljoin_list(response, img_url)

    participant_num = sel.xpath('//*[@id="media_comment"]/span[@class="f_red"]/text()').extract_first()
    news_item['participant_num'] = participant_num if participant_num else '0'


def get_old_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    path_div = sel.xpath('//*[@id="lo_links"]/a')
    path_text, path_href = get_path(response, path_div)

    news_item['path_text'] = check_value(path_text)
    news_item['path_url'] = check_value(path_href)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="artibodyTitle"]/text()').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    date_time = sel.xpath('//*[@id="pub_date"]/text()').extract_first()
    news_item['date_time'] = check_value(date_time)

    news_item['comment_id'] = '-1'

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)
    news_item['editor'] = ''

    from_media = sel.xpath('//*[@id="media_name"]/text()').extract_first()
    from_media_url = sel.xpath('//*[@id="media_name"]/@href').extract_first()

    news_item['from_media'] = check_value(from_media)
    news_item['from_media_url'] = check_value(from_media_url)

    content = sel.xpath('//*[@id="artibody"]//p/text()').extract()
    picture_url = sel.xpath('//*[@id="artibody"]//img/@src').extract()

    news_item['content'] = check_value(''.join(content))
    news_item['picture_urls'] = urljoin_list(response, picture_url)

    participant_num = '-1'
    news_item['participant_num'] = participant_num

    return news_item


def get_old_div_2_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    path_div = sel.xpath('//*[@id="lo_links"]/span[@style]/a')

    path_text, path_href = get_path(response, path_div)
    news_item['path_text'] = check_value(path_text)
    news_item['path_url'] = path_href

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="artibodyTitle"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    date_time_line = sel.xpath('//*[@id="artibodyTitle"]/div[@class="from_info"]/text()').extract_first()
    date_time = date_time_line.strip().split(' ')[-1]

    news_item['date_time'] = check_value(date_time)

    news_item['comment_id'] = '-1'

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    news_item['editor'] = ''

    from_div = sel.xpath('//*[@id="artibodyTitle"]/div[@class="from_info"]/span[@class="linkRed02"]/a')
    from_media = from_div.xpath('string(.)').extract_first()
    from_media_url = from_div.xpath('./@href').extract_first()

    news_item['from_media'] = check_value(from_media)
    news_item['from_media_url'] = check_value(from_media_url)

    content = sel.xpath('//*[@id="artibody"]//p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    picture_url = sel.xpath('//*[@id="artibody"]//img/@src').extract()
    news_item['picture_urls'] = urljoin_list(response, picture_url)

    news_item['participant_num'] = '0'

    return news_item


def get_old_3_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    news_item['url'] = response.url

    news_type = sel.xpath('//meta[@property="og:type"]/@content').extract_first()
    news_item['news_type'] = check_value(news_type)

    path_div = sel.xpath('//table/tr/td[@valign="bottom"]/font/a')

    path_text, path_href = get_path(response, path_div)
    news_item['path_text'] = check_value(path_text)
    news_item['path_url'] = path_href

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//meta[@name="tags"]/@content').extract_first()
    news_item['tags'] = check_value(tags)

    news_id = sel.xpath('//meta[@name="publishid"]/@content').extract_first()
    news_item['news_id'] = check_value(news_id)

    title = sel.xpath('//*[@id="article"]//h1').xpath('string(.)').extract_first()
    if not title:
        title = sel.xpath('//head/title/text()').extract_first().split('_')[0]

    news_item['title'] = check_value(title)

    description = sel.xpath('//meta[@name="description"]/@content').extract_first()
    news_item['description'] = check_value(description)

    date_time_line = sel.xpath('//*[@id="article"]/table/tr[3]/td/text()').extract_first()
    date_time = date_time_line.strip().split(' ')[-1]

    news_item['date_time'] = check_value(date_time)

    news_item['comment_id'] = '-1'

    author = sel.xpath('//meta[@property="article:author"]/@content').extract_first()
    news_item['author'] = check_value(author)

    news_item['editor'] = ''

    from_div = sel.xpath('//*[@id="article"]/table/tr[3]/td/font')
    from_media = from_div.xpath('string(.)').extract_first()
    from_media_url = ''

    news_item['from_media'] = check_value(from_media)
    news_item['from_media_url'] = check_value(from_media_url)

    content = sel.xpath('//*[@id="article"]//p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    picture_url = sel.xpath('//*[@id="article"]//img/@src').extract()
    news_item['picture_urls'] = urljoin_list(response, picture_url)

    news_item['participant_num'] = '0'

    return news_item



def get_path(response, path_div):
    path_text_list = []
    path_href_list = []

    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(check_value(path_text))
        path_href_list.append(response.urljoin(path_href))

    return '; '.join(path_text_list), '; '.join(path_href_list)

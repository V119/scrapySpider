#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector, Item

from xinhuaNewsSpider.items import NewsItem

check_value = lambda x: x if x else ''


def get_news_1_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = key_words

    # 路径
    path_div = sel.xpath('//span[@class="curNews domPC"]/a')
    if not path_div:
        path_div = sel.xpath('//td[@class="weizhi02"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(check_value(path_text))
        path_href_list.append(response.urljoin(path_href))

    news_item['path_text'] = '; '.join(path_text_list)
    news_item['path_href'] = '; '.join(path_href_list)

    # 标题
    title = sel.xpath('//*[@id="title"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//span[@class="time"] | //*[@id="pubtime"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 来源
    source = sel.xpath('//*[@id="source"]').xpath('string(.)').extract_first()
    if not source:
        source = sel.xpath('//span[@class="sourceText"]').xpath('string(.)').extract_first()
    if not source:
        source = sel.xpath('//td[@align="left"]/font').xpath('string(.)').extract_first()

    news_item['source'] = check_value(source).strip()

    # 内容
    content = sel.xpath('//div[@class="article"]/p').xpath('string(.)').extract()
    if not content:
        content = sel.xpath('//div[@id="Content"]/p').xpath('string(.)').extract()
        content = ''.join(content)
    else:
        content = ''.join(content)

    news_item['content'] = check_value(content)

    # 图片链接
    picture_urls = sel.xpath('//div[@class="article"]//img/@src | //div[@id="Content"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 编辑
    editor = sel.xpath('//span[@class="editor"]').xpath('string()').extract_first()
    if not editor:
        editor = sel.xpath('//td[@class="zrbj" and @align="right"]')
        if editor:
            editor_text = editor[1].xpath('string(.)').extract_first().strip().split('\n')[:-1]
            editor = ''.join(editor_text)
    news_item['editor'] = check_value(editor).strip()

    # 作者
    author = ''
    news_item['author'] = author

    # 获取后面页的链接
    next_pages_url = sel.xpath('//div[@id="div_currpage"]/a[@class="page-Article"]/@href').extract()
    if not next_pages_url:
        next_pages_url = []
        next_pages_div = sel.xpath('//div[@class="pagebar"]/div/a')

        for next_page_div in next_pages_div:
            next_page_url = next_page_div.xpath('./@href').extract_first()
            next_page_text = next_page_div.xpath('string(.)').extract_first()
            if 'javascript:void(0)' not in next_page_url and '一页' not in next_page_text:
                next_pages_url.append(response.urljoin(next_page_url))

    if not next_pages_url:
        next_pages_url = []
        next_pages_div = sel.xpath('//div[@id="div_currpage"]/a')

        for next_page_div in next_pages_div:
            next_page_url = next_page_div.xpath('./@href').extract_first()
            next_page_text = next_page_div.xpath('string(.)').extract_first()
            if 'javascript:void(0)' not in next_page_url and '一页' not in next_page_text:
                next_pages_url.append(response.urljoin(next_page_url))

    if next_pages_url:
        return next_pages_url, news_item

    return None, news_item


def get_news_1_content(response):
    sel = Selector(response)
    # 内容
    content = sel.xpath('//div[@class="article"]').xpath('string(.)').extract_first()
    if not content:
        content = sel.xpath('//div[@id="Content"]/p').extract()
        content = ''.join(content)

    return check_value(content)


def get_news_1_pic_urls(response):
    sel = Selector(response)
    # 图片链接
    picture_urls = sel.xpath('//div[@class="article"]//img/@src').extract()
    return [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]


def get_science_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = key_words

    # 路径
    path_div = sel.xpath('//div[@class="place"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    news_item['path_text'] = '; '.join(path_text_list)
    news_item['path_href'] = '; '.join(path_href_list)

    # 标题
    title = sel.xpath('//*[@id="title"]').xpath('string(.)').extract_first()
    news_item['title'] = title

    # 日期时间, 来源
    info_div = sel.xpath('//div[@class="info"]/text()').extract_first()
    if info_div:
        info_list = info_div.strip().split('\n')
        date_time = info_list[0]
        source = info_list[1].strip().split(' ')[-1]

        news_item['date_time'] = date_time
        news_item['source'] = source
    else:
        news_item['date_time'] = ''
        news_item['source'] = ''

    # 内容
    content_div = sel.xpath('//*[@id="content"]')
    content = content_div.xpath('string(.)').extract_first()
    picture_urls = content_div.xpath('./*//img/@src').extract()

    news_item['content'] = content
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 编辑和作者
    editor = sel.xpath('//*[@id="articleEdit"]/span[@class="editor"]').xpath('string(.)').extract_first()
    author = sel.xpath('//*[@id="articleEdit"]/span[@class="zuozhe"]').xpath('string(.)').extract_first()

    news_item['editor'] = check_value(editor)
    news_item['author'] = check_value(author)

    return news_item


def get_old_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    # 路径
    path_div = sel.xpath('//*[@id="position"]//a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    news_item['path_text'] = '; '.join(path_text_list)
    news_item['path_href'] = '; '.join(path_href_list)

    # 标题
    title = sel.xpath('//*[@id="article"]/h2').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title)

    # 日期时间和来源
    info_div = sel.xpath('//*[@id="source"]').xpath('string(.)').extract_first()
    div_list = info_div.split('\u3000\u3000')
    news_item['source'] = div_list[-1][3:] if div_list[-1].startswith('来源：') else div_list[-1]
    news_item['date_time'] = div_list[-2]

    # 内容
    content = sel.xpath('//*[@id="mainText"]').xpath('string(.)').extract_first()
    picture_urls = sel.xpath('//*[@id="mainText"]//img/@src').extract()

    news_item['content'] = check_value(content)
    news_item['picture_urls'] = picture_urls

    news_item['editor'] = ''
    news_item['author'] = ''

    return news_item


def get_daily_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    # 路径
    path_div = sel.xpath('//td[@class="dh03"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    if path_div:
        news_item['path_text'] = '; '.join(path_text_list)
        news_item['path_href'] = '; '.join(path_href_list)
    else:
        news_item['path_text'] = ''
        news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//head/title/text()').extract_first()
    news_item['title'] = check_value(title)

    # 时间来源
    source_div = sel.xpath('//td[@class="wht12"]/font[@color]/text()').extract()
    news_item['date_time'] = ''
    if source_div:
        date_time = source_div[0].split('\n')[1].strip()
        news_item['date_time'] = check_value(date_time)

        source = source_div[-1].split('\n')[1].strip()
        news_item['source'] = check_value(source)
    else:
        source_div = sel.xpath('//td[@class="box"]/table[2]/tr[2]/td[@align="center"]/text()').extract_first()
        if source_div:
            news_item['source'] = source_div.strip().split('\n')[0]
        else:
            news_item['source'] = ''

    content = sel.xpath('//*[@id="Zoom"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content)

    picture_urls = sel.xpath('//td[@class="black14"]//img/@src').extract()
    if not picture_urls:
        picture_urls = sel.xpath('//*[@id="Zoom"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    editor = sel.xpath('//*[@id="Zoom"]/p[@align="right"]').xpath('string(.)').extract_first()
    if not editor:
        editor = sel.xpath('//td[@class="hei12"]/div[@align="center"]/text()').extract_first()
    news_item['editor'] = check_value(editor)

    return news_item


def get_pic_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 路径
    path_div = sel.xpath('//div[@class="detail_location"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    if path_div:
        news_item['path_text'] = '; '.join(path_text_list)
        news_item['path_href'] = '; '.join(path_href_list)
    else:
        news_item['path_text'] = ''
        news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//*[@id="title"] | //*[@id="news_title"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期来源
    date_time = sel.xpath('//*[@id="pubtime"] | //span[@class="head_detail_t"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    source_div = sel.xpath('//div[@class="info"]').xpath('string(.)').extract_first()
    if source_div:
        news_item['source'] = source_div.strip().split('\n')[-1][5:]
    else:
        source_div = sel.xpath('//a[@class="head_detail_u"]').xpath('string(.)').extract_first()

    if not source_div:
        source_div = sel.xpath('//*[@id="pubtime"]/parent::node()').xpath('string(.)').extract_first()
        if source_div:
            news_item['editor'] = check_value(source_div.strip().split('|')[-2]).strip()
            source_div = source_div.strip().split('|')[-1].strip()

    news_item['source'] = check_value(source_div).strip()

    # 内容
    content = sel.xpath('//span[@id="content"]').xpath('string(.)').extract_first()
    if not content:
        content = sel.xpath('//div[@class="news-mian"]/div[@class="rui-comment"] '
                            '| //div[@class="news-mian"]/p').xpath('string(.)').extract()
        content = ''.join(content)
    news_item['content'] = check_value(content)

    # 图片
    picture_urls = sel.xpath('//span[@id="content"]//img/@src').extract()
    if not picture_urls:
        picture_urls = sel.xpath('//div[@class="news-mian"]/p//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 下面页码的链接
    next_pages = sel.xpath('//*[@id="div_currpage"]/a[@class="page-Article"]/@href').extract()
    if not next_pages:
        next_pages = sel.xpath('//*[@id="div_currpage"]/a/@href').extract()
    if not next_pages:
        next_pages = sel.xpath('//div[@class="pagebar"]/div/a/@href').extract()

    if not next_pages:
        return None, news_item

    return next_pages, news_item


def get_pic_content(response):
    sel = Selector(response)
    content = sel.xpath('//span[@id="content"]').xpath('string(.)').extract_first()
    if not content:
        content = sel.xpath('//div[@class="news-mian"]/div[@class="rui-comment"] '
                            '| //div[@class="news-mian"]/p').xpath('string(.)').extract()
        content = ''.join(content)
    return check_value(content)


def get_pic_pic_url(response):
    sel = Selector(response)
    picture_urls = sel.xpath('//span[@id="content"]//img/@src').extract()
    if not picture_urls:
        picture_urls = sel.xpath('//div[@class="news-mian"]/p//img/@src').extract()
    return [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]


def get_data_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 路径
    news_item['path_text'] = ''
    news_item['path_href'] = ''

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    # 标题
    title = sel.xpath('//div[@class="title"]/h1/text()').extract_first()
    news_item['title'] = check_value(title).strip()

    # 时间
    date_time = sel.xpath('//span[@class="time"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 来源
    source = sel.xpath('//*[@id="source"]/text()').extract_first()
    news_item['source'] = check_value(source).strip()

    # 编辑
    editor = sel.xpath('//span[@class="editor"]').xpath('string(.)').extract()
    news_item['editor'] = check_value(''.join(editor)).strip()

    # 内容
    content = sel.xpath('//div[@class="article"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content).strip()

    # 图片URL
    picture_urls = sel.xpath('//div[@class="article"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    return news_item


def get_global_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words)

    # 路径
    news_item['path_text'] = '环球'
    news_item['path_href'] = 'http://www.xinhuanet.com/world/globe.htm'

    # 标题
    title = sel.xpath('//head/title/text()').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间、来源
    info_div = sel.xpath('//td[@align="center"]/font')
    news_item['date_time'] = ''
    news_item['source'] = ''
    if info_div:
        date_time_div = info_div[0].xpath('./text()').extract_first()
        if date_time_div:
            info = date_time_div.strip().split('\n')
            if info:
                news_item['date_time'] = check_value(info[-2]).strip()

        source_div = info_div[1].xpath('./text()').extract_first()
        if source_div:
            source = source_div.strip().split('\n')
            if source:
                news_item['source'] = check_value(source[-1]).strip()

    # content
    content = sel.xpath('/html/body/div/table[4]/tr/td[1]/table[2]/tr/td/table[2]/tr/td') \
        .xpath('string(.)').extract_first()
    news_item['content'] = check_value(content)

    # 图片
    picture_urls = sel.xpath('/html/body/div/table[4]/tr/td[1]/table[2]/tr/td/table[2]/tr/td//img/@src').extract()
    news_item['picture_urls'] = picture_urls

    # 编辑
    editor = sel.xpath('/html/body/div/table[4]/tr/td[1]/table[2]/tr/td/table[2]/tr/td'
                       '/p[2]/text()').extract_first()
    news_item['editor'] = check_value(editor).strip()

    news_item['author'] = ''

    return news_item


def get_bj_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words).strip()

    # 路径
    path_div = sel.xpath('//*[@id="location"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    if path_div:
        news_item['path_text'] = '; '.join(path_text_list)
        news_item['path_href'] = '; '.join(path_href_list)
    else:
        news_item['path_text'] = '北京新闻'
        news_item['path_href'] = 'http://www.bj.xinhuanet.com/'

    # 标题
    title = sel.xpath('//*[@id="title"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//*[@id="pubtimeandfrom"]/text()').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 来源
    source = sel.xpath('//*[@id="from"]/text()').extract_first()
    if source:
        news_item['source'] = check_value(source.strip().split('\n')[-1]).strip()
    else:
        news_item['source'] = ''

    # 内容
    content = sel.xpath('//*[@id="contentblock"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content)

    # 图片URL
    picture_urls = sel.xpath('//*[@id="contentblock"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 编辑
    editor = sel.xpath('//*[@id="editblock"]/text()').extract_first()
    if editor:
        news_item['editor'] = check_value(editor.strip().split('\n')[1]).strip()
    else:
        news_item['editor'] = ''

    news_item['author'] = ''

    return news_item


def get_mrdx_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words).strip()

    # 路径
    news_item['path_text'] = ''
    news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//*[@id="Title"]/text()').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//td[@class="gray fs12"]/text()').extract_first()
    if date_time:
        news_item['date_time'] = date_time.strip().split('\n')[0].strip()
    else:
        news_item['date_time'] = ''

    # 来源
    source = sel.xpath('//td[@class="gray fs12"]/font/text()').extract_first()
    news_item['source'] = check_value(source).strip()

    # 内容
    content = sel.xpath('//*[@id="Content"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content)

    # 图片
    picture_urls = sel.xpath('//*[@id="Content"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 编辑作者
    news_item['editor'] = ''
    news_item['author'] = ''

    return news_item


def get_politics_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words).strip()

    # 路径
    path_div = sel.xpath('//div[@class="left"]/a[not(@class="index")]')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    if path_div:
        news_item['path_text'] = '; '.join(path_text_list)
        news_item['path_href'] = '; '.join(path_href_list)
    else:
        news_item['path_text'] = ''
        news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//*[@id="title"]/text()').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//*[@id="pubtime"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 来源
    source = sel.xpath('//*[@id="source"]/text()').extract_first()
    if source:
        news_item['source'] = check_value(source.strip().split('\n')[-1]).strip()
    else:
        news_item['source'] = ''

    # 内容
    content = sel.xpath('//*[@id="content"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content).strip()

    # 图片
    picture_urls = sel.xpath('//*[@id="content"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    editor = sel.xpath('//div[@class="share"]/div[@class="right"]/text()').extract()
    if editor:
        editor = editor[-1]
    else:
        editor = sel.xpath('//div[@class="share"]').xpath('string(.)').extract_first()

    if editor:
        news_item['editor'] = check_value(''.join(editor.strip().split('\n')[-6:])).strip()
    else:
        news_item['editor'] = ''

    author = ''
    news_item['author'] = author

    return news_item


def get_world_news_info(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words).strip()

    # 路径
    path_div = sel.xpath('//*[@id="location"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(response.urljoin(path_href))

    if path_div:
        news_item['path_text'] = '; '.join(path_text_list)
        news_item['path_href'] = '; '.join(path_href_list)
    else:
        news_item['path_text'] = ''
        news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//*[@id="title"]').xpath('string(.)').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//*[@id="pubtime"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 来源
    source = sel.xpath('//*[@id="from"]/a').xpath('string(.)').extract_first()
    news_item['source'] = check_value(source).strip()

    # 内容
    content = sel.xpath('//*[@id="contentblock"]/span/p').xpath('string(.)').extract()
    news_item['content'] = check_value(''.join(content))

    # 图片
    picture_urls = sel.xpath('//*[@id="contentblock"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # 编辑
    editor_div = sel.xpath('//*[@id="editblock"]/text()').extract_first()
    if editor_div:
        editor = editor_div.strip().split('\n')[:-1]
        news_item['editor'] = check_value(''.join(editor)).strip()
    else:
        news_item['editor'] = ''

    # 作者
    news_item['author'] = ''

    # 下一页
    next_pages = sel.xpath('//*[@id="div_currpage"]/a[@class="page-Article"]/@href').extract()
    next_page_urls = [response.urljoin(next_url) for next_url in next_pages if next_url]

    if next_page_urls:
        return next_page_urls, news_item

    return None, news_item


def get_world_content(response):
    sel = Selector(response)
    content = sel.xpath('//*[@id="contentblock"]/span/p').xpath('string(.)').extract()
    return check_value(''.join(content))


def get_word_pic_urls(response):
    sel = Selector(response)
    picture_urls = sel.xpath('//*[@id="contentblock"]//img/@src').extract()

    return [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]


def get_asia_news_div(response):
    sel = Selector(response)
    news_item = NewsItem()
    url = response.url

    news_item['url'] = url

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    news_item['key_words'] = check_value(key_words).strip()

    # 路径
    news_item['path_text'] = ''
    news_item['path_href'] = ''

    # 标题
    title = sel.xpath('//span[@class="zt_titi"]/text()').extract_first()
    news_item['title'] = check_value(title).strip()

    # 日期时间
    date_time = sel.xpath('//*[@id="pubtime"]').xpath('string(.)').extract_first()
    news_item['date_time'] = check_value(date_time).strip()

    # 编辑和来源
    info_div = sel.xpath('//*[@id="pubtime"]/parent::node()').xpath('string(.)').extract_first()
    if info_div:
        news_item['editor'] = check_value(info_div.strip().split('|')[-2]).strip()
        news_item['source'] = check_value(info_div.strip().split('|')[-1]).strip()
    else:
        news_item['editor'] = ''
        news_item['source'] = ''

    news_item['author'] = ''

    # 内容
    content = sel.xpath('//div[@class="bai14"]').xpath('string(.)').extract_first()
    news_item['content'] = check_value(content).strip()

    # 图片
    picture_urls = sel.xpath('//div[@class="bai14"]//img/@src').extract()
    news_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    return news_item

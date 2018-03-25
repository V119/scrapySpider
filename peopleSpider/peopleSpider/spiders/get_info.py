#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from peopleSpider.items import NewsItem

check_value = lambda x: x if x else ''


# 新版本的新闻
def get_news_1_info(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()

    item['url'] = url

    # 路径
    path_div = sel.xpath('//*[@id="rwb_navpath"]/a | //div[contains(@class, "path")]/div[@class="fl"]/a[@class]')
    path_href = ''
    path_text = ''
    for path in path_div:
        href = path.xpath('./@href').extract_first()
        text = path.xpath('string(.)').extract_first()

        path_href = path_href + href + '; '
        path_text = path_text + text + '; '

    item['path_text'] = path_text[:-2]
    item['path_url'] = path_href[:-2]

    # 发布时间
    date_time_div = sel.xpath('//div[@class="box01"]/div[@class="fl"]/text() ').extract_first()
    if date_time_div:
        date_time = date_time_div.strip().split('\xa0')[0]
    else:
        date_time = ''

    item['date_time'] = check_value(date_time)

    # 来源
    source_text = sel.xpath('//div[@class="box01"]/div[@class="fl"]/a').xpath('string(.)').extract_first()
    source_href = sel.xpath('//div[@class="box01"]/div[@class="fl"]/a/@href').extract_first()

    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = sel.xpath('//p[@class="author"]').xpath('string(.)').extract_first()
    item['author'] = check_value(author)

    # 编辑
    editor = sel.xpath('//div[contains(@class, "edit")]').xpath('string(.)').extract_first()
    item['editor'] = check_value(editor)

    # 关键字
    key_words = sel.xpath('//meta[@name="name"]/@content').extract_first()
    item['key_words'] = check_value(key_words)

    # paper 期号
    paper_num = sel.xpath('//*[@id="paper_num"]').xpath('string(.)').extract_first()
    if paper_num:
        paper_num = paper_num.strip()
    item['paper_num'] = check_value(paper_num)

    # title
    title_div = sel.xpath('//div[contains(@class, text_title)]')
    pre_title = title_div.xpath('./h3[@class="pre"]').xpath('string(.)').extract_first()
    title = title_div.xpath('./h1').xpath('string(.)').extract_first()
    sub_title = title_div.xpath('./h4[@class="sub"]').xpath('string(.)').extract_first()
    item['pre_title'] = check_value(pre_title)
    item['title'] = check_value(title)
    item['sub_title'] = check_value(sub_title)

    # 内容 和图片URL
    content_div = sel.xpath('//*[@id="rwb_zw"]/p | //div[@class="box_con"]/p')
    content = []
    img_urls = []
    box_pic = sel.xpath('//div[@class="text_con_left"]/div[@class="box_con"]//img/@src').extract()
    if box_pic:
        img_urls += box_pic

    for content_p in content_div:
        content_text = content_p.xpath('string(.)').extract_first()
        content.append(content_text)

        img_url = content_p.xpath('./img/@src | ./*//img/@src').extract()
        if img_url:
            img_urls = img_urls + img_url

    if img_urls:
        img_urls = [response.urljoin(x) for x in img_urls if x]

    item['content'] = ''.join(content)
    item['pictures_url'] = img_urls

    # 获得分页的所有url
    page_div = sel.xpath('//div[contains(@class, "zdfy")]/a/@href').extract()
    if page_div:
        page_href = [response.urljoin(x) for x in page_div if x]
        if page_href:
            return page_href, item

    return None, item


def get_news_2_info(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()

    item['url'] = url

    # 路径
    path_text = ''
    path_href = ''
    path_div = sel.xpath('//*[@id="p_navigator"]/a '
                         '| //div[contains(@class, "path")]/div[@class="fl"]/a '
                         '| //div[contains(@class, "path")]/a')
    for path in path_div:
        text = path.xpath('string(.)').extract_first()
        href = path.xpath('./@href').extract_first()

        if text:
            path_text = path_text + text + '; '
        if href:
            path_href = path_href + href + '; '

    item['path_text'] = path_text[:-2]
    item['path_url'] = path_href[:-2]

    # 日期时间
    date_time = sel.xpath('//*[@id="p_publishtime"]/text() | //p[@class="sou"]/text()').extract_first()
    if date_time:
        date_time = date_time.strip().split('\xa0')[0]
    item['date_time'] = check_value(date_time)

    # 来源
    source_text = sel.xpath('//*[@id="p_origin"]/a/text() '
                            '| //p[@class="sou"]/a/text() '
                            '| //span[@class="left_8px"]/a/text()').extract_first()
    source_href = sel.xpath('//*[@id="p_origin"]/a/@href '
                            '| //p[@class="sou"]/a/@href '
                            '| //span[@class="left_8px"]/a/@href').extract_first()

    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = sel.xpath('//p[contains(@class, "author")] | //p[@class="zz"]').xpath('string(.)').extract_first()
    item['author'] = check_value(author)

    # 编辑
    editor = sel.xpath('//*[@id="p_editor"] | //div[@class="edit"]').xpath('string(.)').extract_first()
    item['editor'] = check_value(editor)

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(key_words)

    # paper_num
    paper_num = sel.xpath('//*[@id="paper_num"]/text()').extract_first()
    if paper_num:
        paper_num = paper_num.strip()
    item['paper_num'] = check_value(paper_num)

    # 标题
    pre_title = sel.xpath('//h3[@class="pre"]/text() '
                          '| //*[@id="jtitle"]/text() '
                          '| //div[@class="text_c"]/h3/text()'
                          '| //h3[@class="yt"]/text()').extract_first()
    item['pre_title'] = check_value(pre_title)

    title = sel.xpath('//*[@id="p_title"]/text() | //div[@class="text_c"]/h1/text()').extract_first()
    item['title'] = title

    sub_title = sel.xpath('//h4[@class="sub"]/text() '
                          '| //*[@id="ftitle"]/text() '
                          '| //div[@class="text_c"]/h2/text() '
                          '| //h4[@class="ft"]/text()').extract_first()
    item['sub_title'] = check_value(sub_title)

    # 内容和图片
    content_text = sel.xpath('//*[@id="p_content"]/p').xpath('string(.)').extract()
    if not content_text:
        content_text = sel.xpath('//div[@class="show_text"]').xpath('string(.)').extract_first()

    picture_url = sel.xpath('//*[@id="p_content"]/p//img/@src').extract()
    if not picture_url:
        picture_url = sel.xpath('//div[@class="show_text"]//img/@src').extract()

    if content_text:
        item['content'] = ''.join(content_text) if content_text else ''
    else:
        item['content'] = ''

    if picture_url:
        item['pictures_url'] = [response.urljoin(pic_url) for pic_url in picture_url if pic_url]
    else:
        item['pictures_url'] = []

    return item


def get_pic_news_info(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()

    item['url'] = url
    path_div = sel.xpath('//div[contains(@class, "path ")]/div[@class="fl"]/a')
    path_text = ''
    path_href = ''
    if path_div:
        for x in path_div[1:]:
            text = x.xpath('./@href').extract_first()
            if text:
                path_text = path_text + text + '; '

            href = x.xpath('string(.)').extract_first()
            if href:
                path_href = path_href + href + '; '

        path_text = path_text[:-2]
        path_href = path_href[:-2]

    if not path_div:
        path_div = sel.xpath('//div[contains(@class, "x_nav")]/a | //h6[contains(@class, "x_nav")]/a')
        if path_div:
            for x in path_div:
                text = x.xpath('./@href').extract_first()
                if text:
                    path_text = path_text + text + '; '

                href = x.xpath('string(.)').extract_first()
                if href:
                    path_href = path_href + href + '; '

            path_text = path_text[:-2]
            path_href = path_href[:-2]

    item['path_text'] = path_text
    item['path_url'] = path_href

    source_date_div = sel.xpath('//div[@class="page_c" and @style]')
    if not source_date_div:
        source_date_div = sel.xpath('//div[@class="page_c"]/div[@class="fr"]')
    if not source_date_div:
        source_date_div = sel.xpath('//div[@class="text width978 clearfix"]/h2')

    date_time = source_date_div.xpath('string(.)').extract_first()
    if date_time:
        date_time = date_time.strip().split('\xa0')[-1]
    else:
        date_time = []

    item['date_time'] = date_time

    # 来源
    source_text = source_date_div.xpath('./a/text()').extract_first()
    source_href = source_date_div.xpath('./a/@href').extract_first()
    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    item['author'] = ''

    # 编辑
    editor = sel.xpath('//*[@id="p_editor"] | //div[@class="editor"]').xpath('string(.)').extract_first()
    item['editor'] = editor

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = key_words

    # paper_num
    item['paper_num'] = ''

    # title
    pre_title = sel.xpath('//h3[@class="jian"]/text()').extract_first()
    item['pre_title'] = check_value(pre_title)
    sub_title = sel.xpath('//h3[@class="fu"]/text()')
    item['sub_title'] = check_value(sub_title)
    title = sel.xpath('//div[@class="title"]/h1/text() '
                      '| //div[@class="text width978 clearfix"]/h1/text()').extract_first()
    item['title'] = check_value(title)

    # 内容
    content_text = get_pic_content(response)
    item['content'] = []
    if content_text:
        item['content'].append(content_text)

    picture_url = get_pic_picture_url(response)
    item['pictures_url'] = []
    if picture_url:
        item['pictures_url'] += picture_url

    # 获取后面链接
    next_page_urls = sel.xpath('//div[contains(@class, "zdfy")]/a/@href').extract()
    if not next_page_urls:
        next_page_urls = sel.xpath('//div[@class="page_c"]/div[@class="page_n"]/a/@href').extract()
    next_page_urls = [response.urljoin(x) for x in next_page_urls[1:] if x]

    if next_page_urls:
        return next_page_urls, item
    return None, item


def get_dang_news_info(response):
    sel = Selector(response)
    item = NewsItem()

    url = response.url
    item['url'] = check_value(url)

    # 路径
    path_href = sel.xpath('//a[@class="clink"]/@href').extract()
    path_text = sel.xpath('//a[@class="clink"]/text()').extract()

    if path_href:
        item['path_url'] = '; '.join(path_href)
    else:
        item['path_url'] = ''

    if path_text:
        item['path_text'] = '; '.join(path_text)
    else:
        item['path_text'] = ''

    # 日期时间
    date_div = sel.xpath('//td[@class="ly_red"]/text()').extract_first()
    if date_div:
        date_time = date_div.strip().split('\xa0')[0]
    else:
        date_time = ''
    item['date_time'] = check_value(date_time)

    # 来源
    source_div = sel.xpath('//td[@class="ly_red"]/a')
    source_text = source_div.xpath('./text()').extract_first()
    source_href = source_div.xpath('./@href').extract_first()
    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = sel.xpath('//td[@class="fwriter"]').xpath('string(.)').extract_first()
    item['author'] = author

    # 编辑
    edit = sel.xpath('//div[@class="edit"]/i/text()').extract_first()
    item['editor'] = check_value(edit)

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(key_words)

    # paper_num
    item['paper_num'] = ''

    # title
    title = sel.xpath('//td[@class="ftitle"]').xpath('string(.)').extract_first()
    item['title'] = check_value(title)

    pre_title = sel.xpath('//td[@class="fsubtitle"]').xpath('string(.)').extract_first()
    item['pre_title'] = pre_title

    sub_title = ''
    item['sub_title'] = sub_title

    # 内容和图片
    content_text, content_img_urls, content_urls = get_dang_content_div(response)
    item['content'] = check_value(content_text)
    item['pictures_url'] = [response.urljoin(img_url) for img_url in content_img_urls if img_url]
    item['content_url'] = content_urls

    # 获得后面页面的链接
    next_pages = sel.xpath('//div[contains(@class, "zdfy")]/a/@href').extract()
    next_pages = [response.urljoin(page_url) for page_url in next_pages if page_url]

    if next_pages:
        return next_pages, item

    return None, item


def get_dang_content_div(response):
    """
    :param response:
    :return: (content, img_url, content_url)
    """
    sel = Selector(response)
    content_text = sel.xpath('//font[@id="zoom"]').xpath('string(.)').extract_first()

    content_img_urls = sel.xpath('//font[@id="zoom"]//img/@src').extract()

    content_urls = sel.xpath('//font[@id="zoom"]//a')
    content_url_text_href = {}
    for content_url in content_urls:
        content_url_text = content_url.xpath('string(.)').extract_first()
        content_url_href = content_url.xpath('./@href').extract_first()
        content_url_text_href[content_url_href] = content_url_text

    return content_text, content_img_urls, content_url_text_href


def get_pic_content(response):
    sel = Selector(response)
    content = sel.xpath('//*[@id="picG"]/p/text()').extract()
    if not content:
        content = sel.xpath('//div[@class="content clear clearfix"]/p/text()').extract()
    if not content:
        content = sel.xpath('//div[@class="text width978 clearfix"]/p').xpath('string(.)').extract()

    if content:
        content_text = ''.join(content)
    else:
        content_text = ''

    return content_text


def get_pic_picture_url(response):
    sel = Selector(response)
    picture_urls = sel.xpath('//*[@id="picG"]/p//img/@src').extract()
    if not picture_urls:
        picture_urls = sel.xpath('//div[@class="content clear clearfix"]/p//img/@src').extract()

    if not picture_urls:
        picture_urls = sel.xpath('//*[@id="picG"]//img/@src').extract()

    if not picture_urls:
        picture_urls = sel.xpath(
            '//div[@class="text width978 clearfix"]/dl//img[@alt!="上一页" and @alt!="下一页"]/@src').extract()

    return [response.urljoin(url) for url in picture_urls if url]


def get_fanfu_info(response):
    sel = Selector(response)
    item = NewsItem()
    url = response.url

    item['url'] = url

    # 路径
    path_div = sel.xpath('//div[@class="x_nav"]/a | //div[contains(@class, "path")]/a')
    path_text_list = []
    path_href_list = []

    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()

        path_text_list.append(path_text)
        path_href_list.append(path_href)

    item['path_text'] = '; '.join(path_text_list)
    item['path_url'] = '; '.join(path_href_list)

    # 日期时间
    date_time = sel.xpath('//div[contains(@class, "text_c")]/h5/text() | //p[@class="sou"]/text()').extract_first()
    if date_time:
        item['date_time'] = date_time.strip().split('\xa0')[0]
    else:
        item['date_time'] = ''

    # 来源
    source_div = sel.xpath('//div[contains(@class, "text_c")]/h5/a | //p[@class="sou"]/a')
    source_text = source_div.xpath('string(.)').extract_first()
    source_href = source_div.xpath('./@href').extract_first()
    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = sel.xpath('//p[@class="sou1"]').xpath('string(.)').extract_first()
    item['author'] = author

    # 编辑
    editor = sel.xpath('//div[@class="edit"]').xpath('string(.)').extract_first()
    item['editor'] = editor

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = key_words

    # paper_num
    paper_num = sel.xpath('//*[@id="paper_num"]').xpath('string(.)').extract_first()
    item['paper_num'] = check_value(paper_num)

    # title
    pre_title = sel.xpath('//*[@id="jtitle"]/text() | //div[@class="text_c"]/h3/text()').extract_first()
    title = sel.xpath('//div[@class="text_c"]/h1').xpath("string(.)").extract_first()
    sub_title = sel.xpath('//*[@id="ftitle"]/text() | //div[@class="text_c"]/h2/text()').extract_first()

    item['pre_title'] = check_value(pre_title)
    item['title'] = check_value(title)
    item['sub_title'] = check_value(sub_title)

    content = sel.xpath('//div[@class="show_text"]').xpath('string()').extract_first()
    item['content'] = content

    img_urls = sel.xpath('//text_img//img/@src | //div[@class="show_text"]//img/@src').extract()
    item['pictures_url'] = [response.urljoin(img_url) for img_url in img_urls if img_url]

    return item


def get_dangshi_info(response):
    sel = Selector(response)
    item = NewsItem()
    url = response.url
    item['url'] = url

    # 路径
    path_div = sel.xpath('//*[contains(@class, "lujing")]/a')
    path_text = []
    path_href = []
    for path in path_div:
        path_text.append(path.xpath('string(.)').extract_first())
        path_href.append(path.xpath('./@href').extract_first())

    item['path_text'] = '; '.join(path_text)
    item['path_url'] = '; '.join(path_href)

    # 日期时间
    date_time = sel.xpath('//p[@class="sou"]/text()').extract_first()
    if date_time:
        item['date_time'] = date_time.strip().split('\xa0')[0]
    else:
        item['date_time'] = ''

    # 来源
    source_div = sel.xpath('//p[@class="sou"]/a')
    if source_div:
        source_text = source_div.xpath('string(.)').extract_first()
        if source_text == '手机看新闻':
            item['source_text'] = ''
            item['source_href'] = ''
        else:
            item['source_text'] = check_value(source_text.strip())
            source_href = source_div.xpath('./@href').extract_first()
            item['source_href'] = check_value(source_href.strip())
    else:
        item['source_text'] = ''
        item['source_href'] = ''

    # 作者
    author = sel.xpath('//p[@class="author"]').xpath('string(.)').extract_first()
    item['author'] = check_value(author)

    # 编辑
    editor = sel.xpath('//div[@class="editor"]').xpath('string(.)').extract_first()
    item['editor'] = check_value(editor)

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(key_words)

    # paper_num
    paper_num = sel.xpath('//*[@id="paper_num"]').xpath('string(.)').extract_first()
    item['paper_num'] = check_value(paper_num)

    # title
    title = sel.xpath('//div[contains(@class, "content_text")]/h1').xpath('string(.)').extract_first()
    item['title'] = check_value(title)

    pre_title = sel.xpath('//div[contains(@class, "content_text")]/h3').xpath('string(.)').extract_first()
    item['pre_title'] = check_value(pre_title)

    sub_title = sel.xpath('//div[contains(@class, "content_text")]/h2').xpath('string(.)').extract_first()
    item['sub_title'] = check_value(sub_title)

    # 内容
    content = sel.xpath('//*[@id="p_content"]').xpath('string(.)').extract_first()
    item['content'] = check_value(content)

    # 图片链接
    picture_urls = sel.xpath('//div[@class="pic"]//img/@src | //*[@id="p_content"]//img/@src').extract()
    item['pictures_url'] = [response.urljoin(picture_url) for picture_url in picture_urls if picture_url]

    item['content_url'] = ''

    return item


def get_dangshi_2_info(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()

    item['url'] = url

    # 路径
    path_div = sel.xpath('//div[@class="x_nav"]/a')
    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(path_text)
        path_href_list.append(path_href)

    item['path_text'] = '; '.join(path_text_list)
    item['path_url'] = '; '.join(path_href_list)

    # 日期时间
    date_time = sel.xpath('//div[@class="text_c clearfix"]/h5/text()').extract_first()
    if date_time:
        date_time = date_time.strip().split('\xa0')[0]
        item['date_time'] = date_time
    else:
        item['date_time'] = ''

    # 来源
    source_div = sel.xpath('//div[@class="text_c clearfix"]/h5/a')
    source_text = source_div.xpath('string(.)').extract_first()
    source_href = source_div.xpath('./@href').extract_first()
    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = sel.xpath('//p[@class="tc"]').xpath('string(.)').extract_first()
    item['author'] = check_value(author)

    # 编辑
    editor = sel.xpath('//span[@class="fr"]').xpath('string(.)').extract_first()
    item['editor'] = check_value(editor)

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = check_value(key_words)

    # paper_num
    paper_num = sel.xpath('//*[@id="paper_num"]').xpath('string(.)').extract_first()
    item['paper_num'] = check_value(paper_num)

    # title
    title = sel.xpath('//div[@class="text_c clearfix"]/h1').xpath('string(.)').extract_first()
    item['title'] = title

    pre_title = sel.xpath('//div[@class="text_c clearfix"]/h3').xpath('string(.)').extract_first()
    item['pre_title'] = pre_title

    sub_title = sel.xpath('//div[@class="text_c clearfix"]/h4').xpath('string(.)').extract_first()
    item['sub_title'] = sub_title

    # 内容
    content = sel.xpath('//div[@class="text_show"]').xpath('string(.)').extract_first()
    item['content'] = check_value(content)

    # 图片
    picture_urls = sel.xpath('//div[@class="text_show"]//img/@src').extract()
    item['pictures_url'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    # content_url
    item['content_url'] = ''

    return item


def get_qunzhong_info(response):
    sel = Selector(response)
    item = NewsItem()
    url = response.url

    item['url'] = url

    # 路径
    path_div = sel.xpath('//h3[@class="d2_1 clear"]/a')
    text_list = []
    href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        text_list.append(path_text)
        href_list.append(path_href)

    item['path_text'] = '; '.join(text_list)
    item['path_url'] = '; '.join(href_list)

    # 日期时间
    head_div = sel.xpath('//div[@class="d2_left d2txt_left fl"]')
    date_time = head_div.xpath('./h2[not(@class)]/text()').extract_first()
    if date_time:
        date_time = date_time.strip().split('\xa0')[0]
        item['date_time'] = date_time
    else:
        item['date_time'] = ''

    # 来源
    source_text = head_div.xpath('./h2[not(@class)]/a/text()').extract_first()
    source_href = head_div.xpath('./h2[not(@class)]/a/@href').extract_first()
    item['source_text'] = check_value(source_text)
    item['source_href'] = check_value(source_href)

    # 作者
    author = head_div.xpath('./h2[@class="author"]').xpath('string(.)').extract_first()
    item['author'] = check_value(author)

    # 编辑
    editor = sel.xpath('//span[@class="fr"]').xpath('string(.)').extract_first()
    item['editor'] = editor

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['key_words'] = key_words

    # paper_num
    paper_num = sel.xpath('//*[@id="paper_num"]').xpath('string(.)').extract_first()
    item['paper_num'] = check_value(paper_num)

    # title
    pre_title = head_div.xpath('./h4').xpath('string(.)').extract_first()
    item['pre_title'] = pre_title

    title = head_div.xpath('./h1').xpath('string(.)').extract_first()
    item['title'] = title

    sub_title = head_div.xpath('./h5').xpath('string(.)').extract_first()
    item['sub_title'] = sub_title

    # 内容
    item['content'] = get_qunzhong_content(response)

    # 图片
    item['pictures_url'] = []
    picture_urls = get_qunzhong_picture(response)
    if picture_urls:
        item['pictures_url'] += picture_urls

    # 页面中的链接
    page_href = sel.xpath('//div[contains(@class, "zdfy")]/a/@href').extract()

    if page_href:
        return page_href, item

    return None, item


def get_qunzhong_content(response):
    sel = Selector(response)
    content_list = sel.xpath('//div[@class="d2txt_1 clear"]/p').xpath('string(.)').extract()
    content = ''.join(content_list)

    return check_value(content)


def get_qunzhong_picture(response):
    sel = Selector(response)
    picture_urls = sel.xpath('//div[@class="d2txt_1 clear"]//img/@src').extract()
    picture_urls = [response.urljoin(pic_url) for pic_url in picture_urls
                    if pic_url and pic_url != '/img/next_page.jpg' and pic_url != '/img/prev_page.jpg']

    return picture_urls

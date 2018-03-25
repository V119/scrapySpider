#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

import demjson
from scrapy import Selector

from sanqinSpider.items import NewsItem

check = lambda x: x if x else ''


def get_news_info(response):
    sel = Selector(response)
    url = response.url

    item = NewsItem()
    item['url'] = url

    # 获取面包屑路径
    nav_div = sel.xpath('//div[@class="nva-tree-list"]/p[@class="nav_tree"]/a')

    path_text = ''
    path_url = ''
    for path in nav_div:
        text = path.xpath('string(.)').extract_first()
        href = path.xpath('./@href').extract_first()
        path_text = path_text + text + '; '
        path_url = path_url + href + '; '

    item['path_url'] = path_url[:-2] if path_url and len(path_url) > 2 else ''
    item['path_text'] = path_text[:-2] if path_text and len(path_text) > 2 else ''

    # 获取标题
    title = sel.xpath('//div[@class="article-info"]/h1/text()').extract_first()
    item['title'] = title

    # 获取来源和来源链接
    source_div = sel.xpath('//span[@class="source"]')
    source_text = source_div.xpath('string(.)').extract_first()
    source_href = source_div.xpath('./a/@href').extract_first()

    item['source_text'] = check(source_text).strip()
    item['source_href'] = check(source_href)

    # 获取发表时间
    date_time = sel.xpath('//div[@class="title-info"]/div[@class="fleft"]/span[3]/text()').extract_first()
    item['publish_time'] = check(date_time)

    # 获取标签
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    key_words_array = []
    if key_words:
        key_words_array = key_words.split(' ')

    if key_words_array:
        item['key_words'] = check(key_words_array[:-1])

    # 获取文章的编辑
    editor = sel.xpath('//div[@class="share-box"]/div[@class="copy"]').xpath('string(.)').extract_first()
    if editor and editor.strip() and len(editor.strip()) > 7:
        item['editor'] = editor.strip()[6:-1]
    else:
        item['editor'] = ''

    # 文章核心提示
    abstract = sel.xpath('//meta[@name="description"]/@content').extract_first()
    item['abstract'] = check(abstract)

    # 获取文章内容
    content_div = sel.xpath('//div[contains(@class, "article-content")]')
    content = ''
    image_urls = []
    if content_div:
        content = content_div.xpath('string(.)').extract_first()
        image_urls = Selector(text=content_div.extract_first()).xpath('//img/@src').extract()

    item['content'] = content
    item['picture_urls'] = image_urls

    # 获取文章的图片

    # 文章是否有分页显示， 若有分页显示则返回文章ID
    page = sel.xpath('//div[@class="article-page"]/table[@class="page"]')
    if page:
        content_id = sel.xpath('//script/text()').re('var\s+contentid\s*=\s*\'(.*)\'')
        if content_id:
            content_id = content_id[0]

        return content_id, item

    return None, item


def get_pic_item(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()

    item['url'] = check(url)

    # 面包屑路径
    path_div = sel.xpath('//div[@class="column m-crumb"]/a')
    path_text = ''
    path_url = ''
    for path in path_div:
        text = path.xpath('string(.)').extract_first()
        if text:
            path_text = path_text + text + '; '

        href = path.xpath('./@href').extract_first()
        if href:
            path_url = path_url + href + '; '

    item['path_url'] = path_url[:-2] if path_url and len(path_url) > 2 else ''
    item['path_text'] = path_text[:-2] if path_text and len(path_text) > 2 else ''

    # 标题
    title = sel.xpath('//h1[@class="article-content-title"]').xpath('string(.)').extract_first()
    item['title'] = check(title)

    # 发布时间
    date_time = sel.xpath('//span[contains(@class, "date")]').xpath('string(.)').extract_first()
    item['publish_time'] = check(date_time)

    # 来源
    source = sel.xpath('//div[contains(@class, "article-infos")]/a[contains(@class, "source")]')
    source_text = source.xpath('string(.)').extract_first()
    source_href = source.xpath('./@href').extract_first()
    item['source_text'] = check(source_text)
    item['source_href'] = check(source_href)

    # 责任编辑
    editor = sel.xpath('//span[contains(@class, "editor")]').xpath('string(.)').extract_first()
    item['editor'] = editor

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    key_words_array = []
    if key_words:
        key_words_array = key_words.split(' ')
    item['key_words'] = key_words_array

    # 摘要
    abstract = sel.xpath('//meta[@name="description"]/@content').extract_first()
    item['abstract'] = check(abstract)

    # 获取全部的文件和图片
    content_list = sel.xpath('//ul[@id="thumb"]/li')
    img_urls = []
    img_texts = []
    for content in content_list:
        img_src = content.xpath('./i[@title="img"]/text()').extract_first()
        img_urls.append(img_src)
        img_text = content.xpath('./i[@title="timg"]/text()').extract_first()
        img_texts.append(img_text)

    item['picture_urls'] = img_urls
    item['content'] = img_texts

    return item


def get_dark_pic_item(response):
    sel = Selector(response)
    url = response.url
    item = NewsItem()
    item['url'] = url

    # 面包屑碎片
    path_div = sel.xpath('//div[@class="crumb"]/a')
    path_text = ''
    path_href = ''
    for path in path_div:
        text = path.xpath('string(.)').extract_first()
        if text:
            path_text = path_text + text + '; '

        href = path.xpath('./@href').extract_first()
        if href:
            path_href = path_href + href + '; '

    item['path_url'] = path_href[:-2] if path_href and len(path_href) > 2 else ''
    item['path_text'] = path_text[:-2] if path_text and len(path_text) > 2 else ''

    # 标题
    title = sel.xpath('//header[@class="picture-header"]/h1[@class="h1"]/text()').extract_first()
    item['title'] = check(title)

    # 发表时间
    date = sel.xpath('//div[@class="picture-infos"]/span[@class="post-time"]/text()').extract_first()
    item['publish_time'] = check(date)

    # 编辑
    editor = sel.xpath('//div[@class="picture-infos"]/span[@class="editor"]/text()').extract_first()
    if editor and len(editor) > 5:
        item['editor'] = check(editor[5:])
    else:
        item['editor'] = ''

    # 来源
    source = sel.xpath('//div[@class="picture-infos"]/span[@class="source"]/a')
    if not source:
        source_text = sel.xpath('//div[@class="picture-infos"]/span[@class="source"]')\
            .xpath('string(.)').extract_first()
        item['source_text'] = check(source_text)
        item['source_href'] = ''
    else:
        source_text = source.xpath('string(.)').extract_first()
        source_href = source.xpath('./@href').extract_first()
        item['source_text'] = check(source_text)
        item['source_href'] = check(source_href)



    # 总结摘要
    abstract = sel.xpath('//p[@class="summary"]').xpath('string(.)').extract_first()
    if not abstract:
        abstract = sel.xpath('//meta[@name="description"]/@content').extract_first()
    item['abstract'] = check(abstract)

    # 关键字
    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    key_words_array = []
    if key_words:
        key_words_array = key_words.strip().split(' ')
    item['key_words'] = key_words_array

    # 图片和内容
    content_text = []
    content_href = []
    # content_div = sel.xpath('//ul[@class="gallery-thumb-items"]/li')
    # for content in content_div:
    #     text = content.xpath('./a/img/@alt').extract_first()
    #     img_href = content.xpath('./a/img/@src').extract_first()
    #     if img_href:
    #         a_piece = img_href.split('/')
    #         a_last_piece = a_piece[-1].split('_')
    #         a_piece[-1] = a_last_piece[-1]
    #         img_href = '/'.join(a_piece)
    #
    #     content_text.append(text)
    #     content_href.append(img_href)

    pic_divs = sel.xpath('//script/text()').re('photos\.push\((.*)\);')
    for pic_div in pic_divs:
        try:
            json_data = demjson.decode(pic_div)
            pic_href = json_data['big'] or json_data['orig']
            pic_text = json_data['note']

            content_href.append(pic_href)
            content_text.append(pic_text)
        except Exception as e:
            print(e)

    item['content'] = content_text
    item['picture_urls'] = content_href

    return item

def get_all_content(response):
    body = response.body.decode()
    img_urls = []
    content_text = ''
    if body:
        try:
            json_data = json.loads(body[1:-2])
            content = Selector(text=json_data['content'])
            img_href = content.xpath('//img/@src').extract()
            img_urls = [x for x in img_href if not x.startswith('file://')]
            content_text = content.xpath('string(.)').extract_first()

        except Exception as e:
            print(e)

    return img_urls, content_text

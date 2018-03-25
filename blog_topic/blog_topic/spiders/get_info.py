#!/usr/bin python3
# -*- encoding:  utf-8 -*-
import json

import time
from scrapy import Selector

from blog_topic.items import UserInfoItem, BlogItem, CommentItem, TopicItem
from blog_topic.utils.page_info import get_page_conf_info, get_dom_html

check_value = lambda x: x.strip() if x and isinstance(x, str) else ''
urljoin_list = lambda r, x: [r.urljoin(y) for y in x if y] if x else []


def get_user_info(response):
    # sel = Selector(response)
    if 'http://weibo.com/sorry?pagenotfound&' == response.url:
        return None

    user_item = UserInfoItem()
    user_item['url'] = response.url

    user_id = check_value(get_page_conf_info(response, 'oid'))
    user_item['user_id'] = user_id

    page_id = check_value(get_page_conf_info(response, 'page_id'))
    user_item['page_id'] = page_id

    info_div = get_dom_html(response, 'Pl_Official_PersonalInfo__')
    if info_div:
        info_list = Selector(text=info_div).xpath('//li[@class="li_1 clearfix"]')
        for info in info_list:
            info_title = info.xpath('./span[contains(@class, "pt_title S_txt")]').xpath('string(.)').extract_first()
            info_detail = info.xpath('./span[contains(@class, "pt_detail")]').xpath('string(.)').extract()
            info_detail = [info_.strip() for info_ in info_detail if info_]

            if '昵称' in info_title:
                user_item['nick_name'] = check_value(''.join(info_detail))
            elif '真实姓名' in info_title:
                user_item['real_name'] = check_value(''.join(info_detail))
            elif '所在地' in info_title:
                user_item['location'] = check_value(''.join(info_detail))
            elif '性别' in info_title:
                user_item['sex'] = check_value(''.join(info_detail))
            elif '性取向' in info_title:
                user_item['sexual_orientation'] = check_value(''.join(info_detail))
            elif '感情状况' in info_title:
                user_item['Relationship_status'] = check_value(''.join(info_detail))
            elif '生日' in info_title:
                user_item['birthday'] = check_value(''.join(info_detail))
            elif '博客' in info_title:
                user_item['blog_address'] = check_value(''.join(info_detail))
            elif '个性域名' in info_title:
                user_item['personal_url'] = check_value(''.join(info_detail))
            elif '简介' in info_title:
                user_item['description'] = check_value(''.join(info_detail))
            elif '注册时间' in info_title:
                user_item['register_date'] = check_value(''.join(info_detail))
            elif '公司' in info_title:
                user_item['company'] = check_value('\n'.join(info_detail))
            elif '大学' in info_title:
                user_item['education'] = check_value('\n'.join(info_detail))
            elif '标签' in info_title:
                user_item['tag'] = check_value('\n'.join(info_detail))
            elif '邮箱' in info_title:
                user_item['mail'] = check_value(''.join(info_detail))
            elif 'QQ' in info_title:
                user_item['qq'] = check_value(''.join(info_detail))
            elif '血型' in info_title:
                user_item['blood_type'] = check_value(''.join(info_detail))
            else:
                print('info div more value!! ' + info_title)

    else:
        raise ValueError('no info div')

    # 关注、粉丝、微博数
    num_div = get_dom_html(response, 'Pl_Core_T8CustomTriColumn__')
    if num_div:
        num_list = Selector(text=num_div).xpath('//td[contains(@class, "S_line")]/a[contains(@class, "t_link S_txt")]')
        for num_ in num_list:
            num_data = num_.xpath('./*[contains(@class, "W_f")]').xpath('string(.)').extract_first()
            num_name = num_.xpath('./span[contains(@class, "S_txt")]').xpath('string(.)').extract_first()
            if not num_data or not num_data.strip().isdigit():
                num_data = -1

            if '关注' in num_name:
                user_item['friends_num'] = num_data
            elif '粉丝' in num_name:
                user_item['fans_num'] = num_data
            elif '微博' in num_name:
                user_item['blog_num'] = num_data
            else:
                print('num div more value!! ' + num_name)
    else:
        raise ValueError('no num div')

    head_div = get_dom_html(response, 'Pl_Official_Headerv6')
    if head_div:
        head_info = Selector(text=head_div).xpath('//a[@class="icon_bed"]/em/@class').extract_first()
        if not head_info:
            user_item['is_v'] = 'nil'
        else:
            user_item['is_v'] = check_value(head_info)

        # 获取头像URL
        head_img_url = Selector(text=head_div).xpath('//div[@node-type="photo"]'
                                                     '//img[@class="photo"]/@src').extract_first()
        if head_img_url:
            user_item['head_img_url'] = head_img_url
        else:
            user_item['head_img_url'] = ''

    else:
        raise ValueError('head div error!!')

    level_div = get_dom_html(response, 'Pl_Official_RightGrowNew')
    if level_div:
        level_info = Selector(text=level_div) \
            .xpath('//div[contains(@class,"level_box S_txt")]').xpath('string(.)').extract_first()
        user_item['rank'] = check_value(level_info)
    else:
        raise ValueError('level div error!!')

    user_item['parse_time'] = time.time()

    return user_item


def get_fans_ids(response):
    """
    获取粉丝列表或关注列表的用户ID和主页url
    :param response:
    :return:
    """

    fans_div = get_dom_html(response, 'Pl_Official_HisRelation_')
    user_list = Selector(text=fans_div).xpath('//ul[contains(@class, "follow_list")]/li')

    fans_ids = []
    fans_urls = []

    for fans_user in user_list:
        fans_data = fans_user.xpath('./@action-data').extract_first()
        if fans_data:
            for info in fans_data.strip().split('&'):
                o = info.split('=')
                if 'uid' in o[0] and ':' not in o[-1]:  # 关注的不是话题
                    fans_ids.append(o[-1])
                    break

        fans_url = fans_user.xpath('./dl//div[contains(@class, "info_name")]'
                                   '/a[contains(@class, "S_txt")]/@href').extract_first()
        if fans_url:
            fans_urls.append(fans_url)

    fans_urls = urljoin_list(response, fans_urls)

    return fans_ids, fans_urls


def get_fans_next_page(response):
    """
    获取粉丝列表2-5页的url
    :return:
    """
    fans_div = get_dom_html(response, 'Pl_Official_HisRelation_')
    page_list = Selector(text=fans_div).xpath('//div[@class="W_pages"]/'
                                              'a[contains(@class, "page S_txt")]/@href').extract()[:4]

    return urljoin_list(response, page_list)


def get_fans_next_page_url(response=None):
    """
    获取下一页的url, 若没有下一页，返回None
    :param response:
    :return: next_page_url
    """
    fans_div = get_dom_html(response, 'Pl_Official_HisRelation_')
    next_page_div = Selector(text=fans_div) \
        .xpath('//div[@class="W_pages"]/a[contains(@class, "page next S_txt")]')
    next_page_url = next_page_div.xpath('./@href').extract_first()
    is_limited = next_page_div.xpath('./@page-limited').extract_first()

    if not is_limited:
        return None
    elif 'true' in is_limited:
        return None
    else:
        return response.urljoin(next_page_url)


def get_blog_list(response, total_page_response=None, ajax_html=None):
    """
    获取当页的微博文章
    :param ajax_html:
    :param total_page_response:
    :param response:
    :return:
    """
    if response:
        blog_html = get_dom_html(response, 'Pl_Third_App_')
        try:
            sel = Selector(text=blog_html)
        except Exception as e:
            raise e
        blog_div = sel.xpath('//div[contains(@class, "WB_feed WB_feed_v")]/div[@mid]')
        # blog_user_id = get_page_conf_info(response, 'oid')
        # user_id = sel
    else:
        blog_div = Selector(text=ajax_html).xpath('//body/div[@mid]')
        # blog_user_id = get_page_conf_info(total_page_response, 'oid')

    for blog_ in blog_div:
        blog_item = BlogItem()
        # blog_item['user_id'] = blog_user_id
        blog_item['praise_time'] = str(time.time())

        mid = blog_.xpath('./@mid').extract_first()
        blog_item['mid'] = check_value(mid)

        user_href = blog_.xpath('./div[@node-type="feed_content"]/div[@class="WB_detail"]'
                                '/div[@class="WB_info"]/a[@class]/@href').extract_first()
        blog_item['user_href'] = check_value(user_href)

        user_card = blog_.xpath('./div[@node-type="feed_content"]/div[@class="WB_detail"]'
                                '/div[@class="WB_info"]/a[@class]/@usercard').extract_first()
        user_card_s = user_card.split('&')
        blog_user_id = None
        for x in user_card_s:
            y = x.split('=')
            if y[0] == 'id':
                blog_user_id = y[1]

        blog_item['user_id'] = check_value(blog_user_id)

        # 如果是转发的，获得转发的信息
        is_forward = blog_.xpath('./@isforward').extract_first()
        if is_forward and is_forward == '1':
            blog_item['is_forward'] = 'True'

            o_mid = blog_.xpath('./@omid').extract_first()
            blog_item['o_mid'] = o_mid

            m_info = blog_.xpath('./@minfo').extract_first()
            tb_info = blog_.xpath('./@tbinfo').extract_first()

            o_user_id = ''
            if m_info:
                m_info_d = m_info.strip().split('&')
                for x in m_info_d:
                    info_key_value = x.strip().split('=')
                    if info_key_value[0] == 'ru':
                        o_user_id = info_key_value[-1]
                        blog_item['o_user_id'] = o_user_id
                    elif info_key_value[0] == 'rm':
                        if not o_mid:
                            blog_item['o_mid'] = info_key_value[-1]

            if tb_info:
                tb_info_d = tb_info.strip().split('&')
                for x in tb_info_d:
                    tb_key_value = x.strip().split('=')
                    if tb_key_value[0] == 'ouid':
                        if not blog_user_id:
                            blog_item['user_id'] = tb_key_value[-1]
                    elif tb_key_value[0] == 'rouid':
                        if not o_user_id:
                            blog_item['o_user_id'] = tb_key_value[-1]

            # 获取转发的文章
            forward_item = BlogItem()
            sub_div = blog_.xpath('./div/div[@class="WB_detail"]/div[@class="WB_feed_expand"]'
                                  '/div[@node-type="feed_list_forwardContent"]')
            is_empty = sub_div.xpath('./div[@class="WB_empty"]')  # 转发是否已经被删除
            if not is_empty:
                forward_item['is_forward'] = 'False'
                sub_info_div = sub_div.xpath('./div[@class="WB_info"]/a[contains(@class, "W_fb")]')
                sub_user_info = sub_info_div.xpath('./@usercard').extract_first()
                forward_item['user_id'] = '-1'
                if sub_user_info:
                    x = sub_user_info.strip().split('&')
                    for y in x:
                        z = y.strip().split('=')
                        if z[0] == 'id':
                            forward_item['user_id'] = z[-1]

                sub_mid_info = sub_info_div.xpath('./@suda-uatrack').extract_first()
                forward_item['mid'] = '-1'
                if sub_mid_info:
                    forward_item['mid'] = sub_mid_info.strip().split(':')[-1]

                # 转发的微博内容
                sub_blog_info = sub_div.xpath('./div[@class="WB_text"]').extract_first()

                forward_item['praise_time'] = str(time.time())

                sub_unflod_url, sub_info_dict = get_blog_content_info(sub_blog_info)
                forward_item['blog_info'] = sub_info_dict['text_list']
                forward_item['at_url_list'] = sub_info_dict['at_url_list']
                forward_item['at_list'] = sub_info_dict['at_text_list']
                forward_item['topic_list'] = sub_info_dict['topic_list']
                forward_item['topic_url_list'] = sub_info_dict['topic_url_list']
                forward_item['article_url'] = sub_info_dict['article_url_list'][0] \
                    if sub_info_dict['article_url_list'] else ''
                forward_item['picture_url'] = sub_info_dict['img_url_list']

                # 获得转发的图片
                sub_pic_div = sub_div.xpath('./div[@node-type="feed_list_media_prev"]'
                                            '//div[@class="media_box"]/ul//img/@src').extract()
                forward_item['picture_url'] += sub_pic_div
                forward_item['picture_url'] = turn_to_big_pic(forward_item['picture_url'])

                # 时间日期，来自
                sub_foot_div = sub_div.xpath('./div[contains(@class, "WB_func")]')
                sub_from_div = sub_foot_div.xpath('./div[contains(@class, "WB_from")]/a')
                forward_item['date_time'] = check_value(sub_from_div[0].xpath('./@title').extract_first())
                forward_item['data_from'] = check_value(
                    sub_from_div[1].xpath('string(.)').extract_first()) if len(sub_from_div) > 1 else ''
                forward_item['exact_time'] = check_value(sub_from_div[0].xpath('./@date').extract_first())

                # 评论、转发、赞
                forward_item['forward_num'] = -1
                forward_item['prise_num'] = -1
                forward_item['comment_num'] = -1
                sub_mid = sub_foot_div.xpath('./div[@class="WB_handle W_fr"]/@mid').extract_first()
                if 'mid' not in forward_item.fields and not forward_item['mid'].isdigit():
                    forward_item['mid'] = sub_mid
                sub_num_div = sub_foot_div.xpath('./div[@class="WB_handle W_fr"]//ul/li')
                for sub_div in sub_num_div:
                    sub_type = sub_div.xpath('./span/a/span//em[@class]/@class').extract_first()
                    sub_num = sub_div.xpath('./span/a/span//em[not(@class)]/text()').extract_first()

                    if sub_type and 'ficon_forward' in sub_type:
                        if '转发' in sub_num:
                            forward_item['forward_num'] = '0'
                        elif sub_num.strip().isdigit():
                            forward_item['forward_num'] = sub_num.strip()
                        else:
                            print('Parse sub forward_num error!!  ' + sub_num)

                    elif sub_type and 'ficon_repeat' in sub_type:
                        if '评论' in sub_num:
                            forward_item['comment_num'] = '0'
                        elif sub_num.strip().isdigit():
                            forward_item['comment_num'] = sub_num.strip()
                        else:
                            print('Parse sub comment_num error!!  ' + sub_num)

                    elif sub_type and 'ficon_praised' in sub_type:
                        if '赞' in sub_num:
                            forward_item['prise_num'] = '0'
                        elif sub_num.strip().isdigit():
                            forward_item['prise_num'] = sub_num.strip()
                        else:
                            print('Parse sub prise_num error!!  ' + sub_num)

                yield sub_unflod_url, forward_item
            else:
                blog_item['is_forward'] = 'Forward delete'

        else:
            blog_item['is_forward'] = 'False'

        # head_img_url = blog_.xpath('./div[@node-type="feed_content"]/'
        #                            'div[contains(@class, "WB_face")]//img/@src').extract_first()
        # blog_item['head_img_url'] = check_value(head_img_url)

        blog_info = blog_.xpath('./div[@node-type="feed_content"]/'
                                'div[@class="WB_detail"]/div[contains(@class, "WB_text")]').extract_first()

        # 获得日期时间和来源
        date_div = blog_.xpath('./div[@node-type="feed_content"]/'
                               'div[@class="WB_detail"]/div[contains(@class, "WB_from")]/a')
        blog_item['date_time'] = check_value(date_div[0].xpath('./@title').extract_first())
        blog_item['data_from'] = check_value(date_div[1].xpath('string(.)').extract_first()) \
            if len(date_div) > 1 else ''
        blog_item['exact_time'] = check_value(date_div[0].xpath('./@date').extract_first())

        unflod_url, info_dict = get_blog_content_info(blog_info)
        blog_item['blog_info'] = info_dict['text_list']
        blog_item['at_url_list'] = info_dict['at_url_list']
        blog_item['at_list'] = info_dict['at_text_list']
        blog_item['topic_list'] = info_dict['topic_list']
        blog_item['topic_url_list'] = info_dict['topic_url_list']
        blog_item['article_url'] = info_dict['article_url_list'][0] if info_dict['article_url_list'] else ''
        blog_item['picture_url'] = info_dict['img_url_list']

        media_div = blog_.xpath('./div[@node-type="feed_content"]/'
                                'div[@class="WB_detail"]//div[@class="media_box"]//img/@src').extract()
        if 'picture_url' in blog_item.fields:
            blog_item['picture_url'] += media_div
        else:
            blog_item['picture_url'] = media_div
        if blog_item['picture_url']:
            if response:
                blog_item['picture_url'] = urljoin_list(response, blog_item['picture_url'])
            else:
                blog_item['picture_url'] = urljoin_list(total_page_response, blog_item['picture_url'])
        blog_item['picture_url'] = turn_to_big_pic(blog_item['picture_url'])

        # 获取点赞、评论、转发数
        blog_item['forward_num'] = -1
        blog_item['prise_num'] = -1
        blog_item['comment_num'] = -1

        foot_div = blog_.xpath('./div//ul[contains(@class, "WB_row_line")]/li')
        for sub_div in foot_div:
            sub_type = sub_div.xpath('./a/span[@class="pos"]//em[@class]/@class').extract_first()
            sub_num = sub_div.xpath('./a/span[@class="pos"]//em[not(@class)]/text()').extract_first()

            if sub_type and 'ficon_forward' in sub_type:
                if '转发' in sub_num:
                    blog_item['forward_num'] = '0'
                elif sub_num.strip().isdigit():
                    blog_item['forward_num'] = sub_num.strip()
                else:
                    print('Paese forward_num error!!  ' + sub_num)

            elif sub_type and 'ficon_repeat' in sub_type:
                if '评论' in sub_num:
                    blog_item['comment_num'] = '0'
                elif sub_num.strip().isdigit():
                    blog_item['comment_num'] = sub_num.strip()
                else:
                    print('Paese comment_num error!!  ' + sub_num)

            elif sub_type and 'ficon_praised' in sub_type:
                if '赞' in sub_num:
                    blog_item['prise_num'] = '0'
                elif sub_num.strip().isdigit():
                    blog_item['prise_num'] = sub_num.strip()
                else:
                    print('Paese prise_num error!!  ' + sub_num)

        yield unflod_url, blog_item


# 产生a的占位符
gen_a_text = lambda t, h: '[[(' + str(t) + ')--' + str(h) + ']]'

# 产生表情的占位符
gen_emjo_text = lambda title, href: '[[(emjo_' + str(title) + ')--' + str(href) + ']]'


def get_blog_content_info(blog_content_html, is_unflod=False):
    sel = Selector(text=blog_content_html)

    # 微博文字信息
    if is_unflod:
        blog_text_div = sel.xpath('//body/child::node()').extract()
    else:
        blog_text_div = sel.xpath('//div[contains(@class, "WB_text")]/child::node()').extract()

    text_list = []
    at_url_list = []
    at_text_list = []
    topic_list = []
    topic_url_list = []
    article_url_list = []
    img_url_list = []
    unfold_url = None
    for child_div in blog_text_div:
        content_sel = Selector(text=child_div)
        a_sel = content_sel.xpath('//a')
        img_sel = content_sel.xpath('//img')

        if a_sel:
            a_type = a_sel.xpath('./i/@class | ./span/i/@class').extract_first()
            # 转发的时候带着图片
            if a_type and 'ficon_cd_img' in a_type:
                action_data = a_sel.xpath('./@action-data').extract_first()
                uid = ''
                mid = ''
                pid = ''
                short_url = ''
                if action_data:
                    for x in action_data.split('&'):
                        x_key = x.strip().split('=')[0]
                        x_value = x.strip().split('=')[1]
                        if x_key == 'uid':
                            uid = x_value
                        elif x_key == 'mid':
                            mid = x_value
                        elif x_key == 'pid':
                            pid = x_value
                        elif x_key == 'short_url':
                            short_url = x_value
                if short_url:
                    img_url_list.append(short_url)
                elif uid and mid and pid:
                    img_url = 'http://photo.weibo.com/' \
                              + uid \
                              + '/wbphotos/large/mid/' \
                              + mid \
                              + '/pid/' \
                              + pid
                    img_url_list.append(img_url)
                else:
                    print('No img url' + str(a_sel.extract()))
                text_list.append(check_value(a_sel.xpath('string(.)').extract_first()))

            elif a_sel.xpath('./@extra-data') and a_sel.xpath('./@extra-data').extract_first() == 'type=atname':
                at_text = check_value(a_sel.xpath('string(.)').extract_first())
                at_text_list.append(at_text)
                text_list.append(at_text)
                at_url_list.append(a_sel.xpath('./@href').extract_first())
            elif a_sel.xpath('./@extra-data') and a_sel.xpath('./@extra-data').extract_first() == 'type=topic':
                topic_text = check_value(a_sel.xpath('string(.)').extract_first())
                text_list.append(topic_text)
                topic_list.append(topic_text)
                topic_url_list.append(a_sel.xpath('./@href').extract_first())
            elif a_sel.xpath('./@action-type') and a_sel.xpath('./@action-type').extract_first() == 'fl_unfold':
                # 获取展开全文的URL，这个URL只用于获取内容的ajax请求
                fl_action_data = a_sel.xpath('./@action-data').extract_first()
                unfold_url = 'http://weibo.com/p/aj/mblog/getlongtext?ajwvr=6&' + fl_action_data
            elif content_sel.xpath('//a/img'):
                img_type = content_sel.xpath('//a/img/@type').extract_first()
                # 如果是表情
                if img_type and img_type == 'face':
                    title = img_sel.xpath('./@title').extract_first()
                    src = img_sel.xpath('./@src').extract_first()
                    text = gen_emjo_text(title, src)
                    text_list.append(text)
                else:
                    text_list.append(check_value(img_sel.xpath('string(.)').extract_first()))

            elif a_type:
                a_href = check_value(a_sel.xpath('./@href').extract_first())
                if 'ficon_cd_longwb' in a_type:
                    article_url_list.append(a_href)
                part_text = gen_a_text(a_type, a_href)
                text_list.append(check_value(a_sel.xpath('string(.)').extract_first()) + part_text)

            else:
                print('blogs has more type!! ' + str(a_sel.extract()) + ' \n' + blog_content_html)
        elif img_sel:
            img_type = img_sel.xpath('./@type').extract_first()
            # 如果是表情
            if img_type and img_type == 'face':
                title = img_sel.xpath('./@title').extract_first()
                src = img_sel.xpath('./@src').extract_first()
                text = gen_emjo_text(title, src)
                text_list.append(text)
            else:
                text_list.append(check_value(img_sel.xpath('string(.)').extract_first()))
        else:
            text_list.append(check_value(content_sel.xpath('string(.)').extract_first()))

    return unfold_url, {
        'text_list': ''.join(text_list),
        'at_url_list': at_url_list,
        'at_text_list': at_text_list,
        'topic_list': topic_list,
        'topic_url_list': topic_url_list,
        'article_url_list': article_url_list,
        'img_url_list': img_url_list
    }


def turn_to_big_pic(url_list):
    new_list = []
    for url in url_list:
        if '.sinaimg.cn':
            s_url = url.split('/')
            s_url[3] = s_url[3] if s_url[3] == 'images' or s_url[3] == 'large' else 'mw690'
            new_url = '/'.join(s_url)
            new_list.append(new_url)
        else:
            new_list.append(url)

    return new_list


def get_article_info(response):
    sel = Selector(response)
    title = sel.xpath('//div[@class="title"]').xpath('string(.)').extract_first()
    date_time = sel.xpath('//span[@class="time"]').xpath('string(.)').extract_first()
    preface = sel.xpath('//div[@class="preface"]').xpath('string(.)').extract_first()
    content = sel.xpath('//div[@class="WB_editor_iframe"]').xpath('string(.)').extract_first()
    media_url = sel.xpath('//div[@class="WB_editor_iframe"]//a/@href').extract()
    media_url = urljoin_list(response, media_url)

    imgs_div = sel.xpath('//p[@class="picbox"]')
    pic_url_desc = []
    for img in imgs_div:
        img_url = img.xpath('./img/@src').extract_first()
        img_desc = img.xpath('./span[@class="picinfo"]').xpath('string(.)').extract_first()
        pic_url_desc.append({img_url: img_desc})

    read_num = sel.xpath('//span[@class="num"]').extract_first()

    return {
        'title': check_value(title),
        'date_time': check_value(date_time),
        'preface': check_value(preface),
        'content': check_value(content),
        'pic_url_desc': pic_url_desc,
        'media_url': media_url,
        'read_num': check_value(read_num)
    }


def get_ajax_next_page(response, page, ajax_page):
    domain = get_page_conf_info(response, 'domain')
    page_id = get_page_conf_info(response, 'page_id')
    script_uri = '/' + '/'.join(response.url.split('?')[0].split('/')[3:])
    # page_id = get_page_conf_info(response, 'page_id')

    next_ajax_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=' \
                    + domain \
                    + '&profile_ftype=1&is_all=1&pagebar=' \
                    + str(ajax_page) \
                    + '&pl_name=Pl_Third_App__11&id=' \
                    + page_id \
                    + '&script_uri=' \
                    + script_uri \
                    + '&feed_type=1&page=' \
                    + str(page) \
                    + '&pre_page=' \
                    + str(page) \
                    + '&domain_op=' \
                    + domain

    return next_ajax_url


def get_ajax_blog(total_page_response, html, is_first_page=False):
    """
    获取ajax获得的微博数据中的微博
    :param is_first_page:
    :param total_page_response:
    :param html:
    :return:
    """
    blog_list = []
    for blog_tuple in get_blog_list(response=None, total_page_response=total_page_response, ajax_html=html):
        blog_list.append(blog_tuple)

    next_page_urls = None

    if is_first_page:  # 获得翻页按钮的页面url， 一次性获得所有URL
        sel = Selector(text=html)
        next_page_div = sel.xpath('//div[@node-type="feed_list_page"]'
                                  '//div[@action-type="feed_list_page_morelist"]/ul/li[not(@class)]/a/@href').extract()
        if next_page_div:
            next_page_urls = urljoin_list(total_page_response, next_page_div)

    return next_page_urls, blog_list


def get_ajax_first_page_blog(response):
    """
    获取点击下一页按钮后的页面的blogs
    :param response:
    :return:
    """
    blog_list = []
    for blog_tuple in get_blog_list(response):
        blog_list.append(blog_tuple)

    return blog_list


def _get_comment_info(response, blog_id, html_=None, parent_comment_id='0'):
    comment_div = None
    if parent_comment_id == '0':
        json_data = response.text
        try:
            json_obj = json.loads(json_data)
            html_ = json_obj['data']['html']

            sel = Selector(text=html_)
            comment_div = sel.xpath('//div[@class="list_box"]/div[@class="list_ul"]/div[@comment_id]')
        except:
            print('Parse comment json error!! ')
    elif html_:
        sel = Selector(text=html_)
        comment_div = sel.xpath('//div[@comment_id]')
    else:
        raise ValueError('None param html_')

    if comment_div:
        for comment_info in comment_div:
            # 获得根comment的信息
            root_comment = CommentItem()

            root_comment['parent_comment_id'] = str(parent_comment_id)

            root_comment['blog_id'] = blog_id
            root_comment['parse_time'] = str(time.time())

            comment_id = comment_info.xpath('./@comment_id').extract_first()
            root_comment['comment_id'] = check_value(comment_id)

            user_info_div = comment_info.xpath('./div[@class="list_con"]/div[@class="WB_text"]/a[1]')
            nick_name = user_info_div.xpath('string(.)').extract_first()
            root_comment['comment_user_nick'] = check_value(nick_name)

            user_id = user_info_div.xpath('./@usercard').extract_first()
            id_str = check_value(user_id).split('=')
            root_comment['comment_user_id'] = id_str[1] if len(id_str) > 1 else ''

            user_url = user_info_div.xpath('./@href').extract_first()
            root_comment['comment_user_page'] = response.urljoin(user_url)

            date_time_div = comment_info.xpath('./div[@class="list_con"]/div[contains(@class, "WB_func")]')
            date_time = date_time_div.xpath('./div[contains(@class, "WB_from")]').xpath('string(.)').extract_first()

            root_comment['comment_date_time'] = check_value(date_time)

            praise_num = date_time_div.xpath('./div[contains(@class, "WB_handle")]'
                                             '/ul//span[@node-type="like_status"]/em[not(@class)]/text()').extract_first()
            if isinstance(praise_num, int) or praise_num.isdigit():
                root_comment['praise_num'] = str(praise_num)
            elif '赞' in praise_num:
                root_comment['praise_num'] = '0'
            else:
                root_comment['praise_num'] = '-1'

            comment_content_div = comment_info.xpath('./div[@class="list_con"]/div[@class="WB_text"]').extract_first()
            info_dic = get_comment_content(comment_content_div)

            root_comment['content'] = info_dic['text_list']
            root_comment['at_url_list'] = info_dic['at_url_list']
            root_comment['at_name_list'] = info_dic['at_text_list']
            root_comment['topic_url_list'] = info_dic['topic_url_list']
            root_comment['topic_text_list'] = info_dic['topic_list']
            root_comment['img_url_list'] = info_dic['img_url_list']

            # 获得更多回复的链接
            more_replay = None
            if parent_comment_id == '0':
                more_replay = comment_info.xpath('./div[@node-type="replywrap"]'
                                                 '//a[@action-type="click_more_child_comment_big"]/@action-data') \
                    .extract_first()

            # 是否有子评论
            child_div = comment_info.xpath('./div[@class="list_con"]/div[contains(@class, "list_box_in")]'
                                           '/div[@node-type="child_comment"]').extract_first()
            root_comment['child_comment_ids'] = []
            if child_div and parent_comment_id == '0':  # and not more_replay:
                for child_comment in get_child_comment(response, blog_id, child_div, comment_id):
                    root_comment['child_comment_ids'].append(child_comment['comment_id'])
                    yield None, child_comment

            yield more_replay, root_comment


def get_root_comment(response, blog_id):
    """
    获得评论微博的评论
    :param response:
    :param blog_id:
    :return:
    """
    for more_replay, comment_item in _get_comment_info(response, blog_id):
        more_comment_url = ''
        if more_replay:
            more_comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&' + more_replay + '&from=singleWeiBo'
        yield more_comment_url, comment_item


def get_child_comment(response, blog_id, html_, parent_comment_id):
    """
    获得评论评论的评论
    :param response:
    :param blog_id:
    :param html_:
    :param parent_comment_id:
    :return:
    """
    for _, child_item in _get_comment_info(response, blog_id, html_=html_, parent_comment_id=parent_comment_id):
        yield child_item


def get_more_child_comment(response, blog_id, parent_comment_id):
    """
    展开查看更多评论的回复
    :param response:
    :param blog_id:
    :param parent_comment_id:
    :return:
    """
    json_data = response.text
    try:
        json_obj = json.loads(json_data)
        html_ = json_obj['data']['html']
        comment_list = []
        next_comment_url = None

        sel = Selector(text=html_)
        action_data = sel.xpath('//a[@action-type="click_more_child_comment_big"]/@action-data').extract_first()
        if action_data:
            next_comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&' + action_data \
                               + '&from=singleWeiBo&__rnd=' + get_rnd_str()

        for _, child_item in _get_comment_info(response, blog_id, html_, parent_comment_id):
            comment_list.append(child_item)

        return next_comment_url, comment_list

    except ValueError as e:
        raise e


def get_comment_content(comment_div):
    sel = Selector(text=comment_div)

    # 微博文字信息
    blog_text_div = sel.xpath('//body/div/child::node()').extract()

    text_list = []
    at_url_list = []
    at_text_list = []
    topic_list = []
    topic_url_list = []
    img_url_list = []

    for child_div in blog_text_div:
        content_sel = Selector(text=child_div)
        a_sel = content_sel.xpath('//a')
        img_sel = content_sel.xpath('//img')

        if a_sel:
            a_type = a_sel.xpath('./i/@class | ./span/i/@class').extract_first()
            # 转发的时候带着图片
            if a_type and 'ficon_cd_img' in a_type:
                action_data = a_sel.xpath('./@action-data').extract_first()
                uid = ''
                mid = ''
                pid = ''
                short_url = ''
                if action_data:
                    for x in action_data.split('&'):
                        x_key = x.strip().split('=')[0]
                        x_value = x.strip().split('=')[1]
                        if x_key == 'uid':
                            uid = x_value
                        elif x_key == 'mid':
                            mid = x_value
                        elif x_key == 'pid':
                            pid = x_value
                        elif x_key == 'short_url':
                            short_url = x_value
                if short_url:
                    img_url_list.append(short_url)
                elif uid and mid and pid:
                    img_url = 'http://photo.weibo.com/' \
                              + uid \
                              + '/wbphotos/large/mid/' \
                              + mid \
                              + '/pid/' \
                              + pid
                    img_url_list.append(img_url)
                else:
                    print('No img url' + str(a_sel.extract()))
                text_list.append(check_value(a_sel.xpath('string(.)').extract_first()))

            elif a_sel.xpath('./@extra-data') and a_sel.xpath('./@extra-data').extract_first() == 'type=atname':
                at_text = check_value(a_sel.xpath('string(.)').extract_first())
                at_text_list.append(at_text)
                text_list.append(at_text)
                at_url_list.append(a_sel.xpath('./@href').extract_first())
            elif a_sel.xpath('./@extra-data') and a_sel.xpath('./@extra-data').extract_first() == 'type=topic':
                topic_text = check_value(a_sel.xpath('string(.)').extract_first())
                text_list.append(topic_text)
                topic_list.append(topic_text)
                topic_url_list.append(a_sel.xpath('./@href').extract_first())
            elif content_sel.xpath('//a/img'):
                img_type = content_sel.xpath('//a/img/@type').extract_first()
                # 如果是表情
                if img_type and img_type == 'face':
                    title = img_sel.xpath('./@title').extract_first()
                    src = img_sel.xpath('./@src').extract_first()
                    text = gen_emjo_text(title, src)
                    text_list.append(text)
                else:
                    text_list.append(check_value(img_sel.xpath('string(.)').extract_first()))

                    # else:

                    # print('blogs has more type!! ' + str(a_sel.extract()) + ' \n' + comment_div)
        elif img_sel:
            img_type = img_sel.xpath('./@type').extract_first()
            # 如果是表情
            if img_type and img_type == 'face':
                title = img_sel.xpath('./@title').extract_first()
                src = img_sel.xpath('./@src').extract_first()
                text = gen_emjo_text(title, src)
                text_list.append(text)
            else:
                text_list.append(check_value(img_sel.xpath('string(.)').extract_first()))
        else:
            text_list.append(check_value(content_sel.xpath('string(.)').extract_first()))

    return {
        'text_list': ''.join(text_list),
        'at_url_list': at_url_list,
        'at_text_list': at_text_list,
        'topic_list': topic_list,
        'topic_url_list': topic_url_list,
        'img_url_list': img_url_list
    }


def get_topic_info(response, orign_url):
    '''
    獲取topic的導語和topic名
    :param response:
    :param orign_url:
    :return:topic_item
    '''
    url = response.url
    topic_item = TopicItem()
    topic_item['topic_url'] = url
    topic_item['topic_orig_url'] = orign_url

    # 導語
    introduction_dom = get_dom_html(response, 'Pl_Third_Inline__')
    intro_sel = Selector(text=introduction_dom)
    intro_text = intro_sel.xpath('//p').xpath('string(.)').extract_first()

    topic_item['topic_introduction'] = check_value(intro_text)

    # topic 名
    topic_name = get_page_conf_info(response, 'onick')

    topic_item['topic_name'] = check_value(topic_name)

    return topic_item


def get_comment_first_url(blog_id):
    """
    获取微博评论第一页的url
    :param blog_id:
    :return:
    """
    rnd = get_rnd_str()
    url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=' + str(blog_id) + '&filter=all&from=singleWeiBo&__rnd=' + rnd

    return url


def get_comment_next_url(response):
    json_data = response.text
    try:
        json_obj = json.loads(json_data)
        html_ = json_obj['data']['html']
        sel = Selector(text=html_)

        action_data = sel.xpath('//div[@node-type="comment_loading"]/@action-data').extract_first()
        if not action_data:
            action_data = sel.xpath('//a[@action-type="click_more_comment"]/@action-data').extract_first()

        next_url = None
        if action_data:
            next_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&' + action_data + '&from=singleWeiBo&__rnd=' \
                       + get_rnd_str()
        return next_url

    except Exception as e:
        raise e


def get_rnd_int():
    """
    获取当前时间的13位，秒级
    :return:
    """
    return int(time.time() // 0.001)


def get_rnd_str():
    return str(get_rnd_int())

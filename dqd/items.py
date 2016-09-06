# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DqdItem(Item):
    #文章信息
    news_title=Field() #文章标题
    news_author=Field()#作者
    news_time=Field()#发表时间
    news_content=Field()#内容
    news_source=Field() #文章来源
    news_allCommentAllCount=Field() #总评论数量
    news_hotCommentHotCount=Field() #热评数量

    #评论信息
    news_hotCommentContent=Field()#热评内容
    news_hotCommentAuthor=Field() #评论留言人
    news_hotCommentTime=Field() #留言时间
    news_hotCommentLikeCount=Field()#热评点赞数量


    source = Field()     #标记slave
    source_url = Field() #文章链接

    image_urls=Field() #图片下载链接
    crawled = Field()
    spider = Field()


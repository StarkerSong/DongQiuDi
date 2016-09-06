# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

class DqdspiderSpider(CrawlSpider):
    name = 'dqdspider'
    allowed_domains = ['dongqiudi.com']
    # start_urls = ['http://www.dongqiudi.com/'  ]
    # start_urls = ['http://www.dongqiudi.com/special/43'  ]
    start_urls = ['http://www.dongqiudi.com/article/%s' % p for p in xrange(1,220000) ]

    rules = [
        Rule(LinkExtractor(allow=(r'/article/\d+$') ), follow=True, callback='parse_article'),#
         # Rule(LinkExtractor(allow=(r'/article/200024$')), follow=True, callback='parse_girl'),  #
    ]

    def parse_comment(self,response):
        for t in response.xpath("//*[@id='top_comment']/li/p[2]"):
            comments = t.xpath('string(.)').extract()
            return comments

    def parse_article(self, response):
            div=response
        # for div in response.xpath("//*[@id='con']"):
            news_title=div.xpath("//*[@id='con']/div[1]/div[1]/h1/text()").extract()[0]
            news_author = div.xpath("//*[@id='con']/div[1]/div[1]/h4/span[1]/text()").extract()[0] # 作者
            news_time = div.xpath("//*[@id='con']/div[1]/div[1]/h4/span[2]/text()").extract()[0]  # 发表时间
            news_content =''.join([t.xpath('string(.)').extract() for t in response.xpath("//*[@id='con']/div[1]/div[1]/div[1]")][0])   # 内容
            news_source_list=div.xpath("//*[@id='con']/div[1]/div[1]/ul/li[1]/a/span/text()").extract()    #消息参考来源
            if not news_source_list:
                news_source_list=div.xpath(' //ul[@class="sourse"]/li/text()').extract()[0]
            # //*[@id="con"]/div[1]/div[1]/ul/li[1]  懂球帝 //*[@id="con"]/div[1]/div[1]/ul
            # //*[@id="con"]/div[1]/div[1]/ul/li[1]/text()    没有署名
            # //*[@id="con"]/div[1]/div[1]/ul/li[1]
            news_source=news_source_list
 
            news_allCommentAllCount =  div.xpath("//*[@id='pjax-container']/div/h3/text()").extract()[0][5:-1] # 总评论数量
            news_hotCommentHotCount = div.xpath("//*[@id='comment']/div[2]/h3/text()").extract()[0][5:-1] # 热评数量

            #如下参考内容： http://stackoverflow.com/questions/31070660/scrapy-get-all-children-ignore-br
            news_hotCommentContent=[t.xpath('string(.)').extract() for t in response.xpath("//*[@id='top_comment']/li/p[2]")]
            news_hotCommentAuthor =div.xpath(" //*[@id='top_comment']/li/p[1]/span[1]/text()").extract()  # 评论留言人
            news_hotCommentTime = div.xpath("//*[@id='top_comment']/li/p[1]/span[2]/text()").extract() # 留言时间
            news_hotCommentLikeCount=div.xpath("//*[@id='top_comment']/li/div/a[3]/text()").extract()# //*[@id="com_27893056"]/a[3]

            image_urls = div.xpath("//*[@class='detail']/div/p/img/@src").extract()
            source_url=response.url #url
            # print news_title,source_url,news_hotCommentContent.encode('gbk','ignore')#.decode('utf-8')
            yield{
                'news_title': news_title ,
                'news_author': news_author,
                'news_time': news_time,
                'news_content': news_content,
                'news_source':news_source,
                'news_allCommentAllCount': news_allCommentAllCount,
                'news_hotCommentHotCount': news_hotCommentHotCount,

                'news_hotCommentContent':news_hotCommentContent,
                'news_hotCommentAuthor': news_hotCommentAuthor,
                'news_hotCommentTime': news_hotCommentTime,
                'news_hotCommentLikeCount': news_hotCommentLikeCount,
                'image_urls': image_urls,
                'source_url': source_url,
                'source': 'dongqiudi',
            }


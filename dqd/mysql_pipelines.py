# -*- coding:utf-8 -*-
from scrapy.conf import settings
import MySQLdb

_DEBUG=True

class MySQLPipeline(object):
    #Connect to the MySQL database
    def __init__(self):
        self.conn =  MySQLdb.connect(
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            db=settings['MYSQL_DBNAME'],
            host=settings['MONGODB_SERVER'],
            charset='utf8',
            use_unicode = True
        )
        self.cursor=self.conn.cursor()
        #清空表：注意区分和delete的区别
        self.cursor.execute("truncate table news_main;") #清空表的信息
        self.cursor.execute("truncate table news_comment;") #清空表的信息
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.insert_news(item)     #将文章信息插入到数据库中
            self.insert_comment(item,item["source_url"])     # 将评论信息信息插入到数据库中
            self.conn.commit()

        except MySQLdb.Error as e:
                print (("Error %d: %s") % (e.args[0],e.args[1]))
        return item

    #将文章信息插入到数据库中
    def insert_news(self,item):
        args = (item["source_url"], item["news_title"], item["news_author"],
                item["news_time"], item["news_content"],item["news_source"],
                item["news_allCommentAllCount"],  item["news_hotCommentHotCount"])

        newsSqlText = "insert into news_main(" \
                      "news_url,news_title,news_author,news_time,news_content,news_source," \
                      "news_commentAllCount,news_commentHotCount) " \
                      "values ('%s','%s','%s','%s','%s','%s','%s','%s')" % args
        self.cursor.execute(newsSqlText)
        self.conn.commit()

    # 将评论信息信息插入到数据库中
    def insert_comment(self, item,url):
        #因为评论是列表，以下为并列迭代
        for comment_content,comment_author,comment_time,comment_likeCount \
                in zip(item["news_hotCommentContent"],item["news_hotCommentAuthor"],
                     item["news_hotCommentTime"],item["news_hotCommentLikeCount"]):
            newsSqlText = "insert into news_comment(comment_content,comment_author,comment_time,comment_likeCount,source_url) " \
                          "values (\"%s\",'%s','%s','%s','%s')" % (comment_content,comment_author,comment_time,comment_likeCount[2:-1],url)
            # #加入调试代码 监视newsSqlText的取值
            # if _DEBUG == True:
            #     import pdb
            #     pdb.set_trace()
            # self.cursor.execute(newsSqlText.encode().decode("unicode-escape").replace('\\','').replace('\']','').replace('[u\'','').strip())
            self.cursor.execute(newsSqlText.encode().decode("unicode-escape").replace('\\',''))
            self.conn.commit()

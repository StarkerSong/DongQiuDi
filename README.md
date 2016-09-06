#基本设置
##配置环境
- **Python：**
Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 20:32:19) [MSC v.1500 32 bit (Intel)] on win32
- **Redis：**
Redis server v=3.2.100 sha=00000000:0 malloc=jemalloc-3.6.0 bits=64 build=dd26f1f93c5130ee
- **Scrapy：**
Scrapy 1.1.1
- **redis-py：**
2.10.5
- **scrapy-redis：**
scrapy-redis-0.6.3
- **jieba**
jieba-0.38 
开源代码：
https://github.com/fxsjy/jieba
学习笔记：
  - 绪论部分
https://segmentfault.com/a/1190000004061791
 - 分词模式 
https://segmentfault.com/a/1190000004065927
 - DAG（有向无环图） 
https://segmentfault.com/a/1190000004085949
 - 详细使用过程介绍 
http://blog.csdn.net/u010454729/article/details/40476483


##安装
进入到pip.exe目录下，使用安装命令`pip install redis`即可。如果缺少其他组件也可以通过方法`pip install modulename`安装。

![install redis-py](http://upload-images.jianshu.io/upload_images/1242974-a623573e3d3bd6fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##调试
python代码调试
http://www.cnblogs.com/qi09/archive/2012/02/10/2344959.html

#基本架构
Scrapy基于事件驱动网络框架 [Twisted](http://twistedmatrix.com/trac/) 编写。因此，Scrapy基于并发性考虑由非阻塞(即异步)的实现。Scrapy中的数据流由执行引擎控制，其过程如下:

1. 引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的URL(s)。
- 引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度。
- 引擎向调度器请求下一个要爬取的URL。
- 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给下载器(Downloader)。
- 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方向)发送给引擎。
- 引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
- Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
- 引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
- (从第二步)重复直到调度器中没有更多地request，引擎关闭该网站。

 
![Scrapy架构](http://upload-images.jianshu.io/upload_images/1242974-f1908012ebe3aabe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




## 文件目录结构
在Windows的命令窗口中输入`tree /f  dqd`命令，出现以下文件目录结构：
```
C:\Python27\Scripts>tree /f  dqd
文件夹 PATH 列表
卷序列号为 A057-81B6
C:\PYTHON27\SCRIPTS\DQD
│  docker-compose.yml
│  Dockerfile
│  mongodb2mysql.py
│  process_items.py
│  scrapy.cfg
│
├─.idea
│      dqd.iml
│      misc.xml
│      modules.xml
│      workspace.xml
│
├─dqd
│  │  image_pipelines.py
│  │  image_pipelines.pyc
│  │  items.py
│  │  mongo_pipelines.py
│  │  mongo_pipelines.pyc
│  │  mysql_pipelines.py
│  │  mysql_pipelines.pyc
│  │  redis_pipelines.py
│  │  redis_pipelines.pyc
│  │  settings.py
│  │  settings.pyc
│  │  __init__.py
│  │  __init__.pyc
│  │
│  └─spiders
│          dqdspider.py
│          dqdspider.pyc
│          __init__.py
│          __init__.pyc
│
└─Image
    └─full
        │  full.rar
        │
        └─女球迷采访：由萌yolanda
                480-150605104925433.jpg
                480-150605104940P1.jpg
                480-15060510522UT.jpg
                480-150605105242F9.jpg
                480-15060510525X18.jpg
                480-150605105312V0.jpg

```

## 下载和存储管理

**settings.py设置**
```
BOT_NAME = 'dqd'

SPIDER_MODULES = ['dqd.spiders']
NEWSPIDER_MODULE = 'dqd.spiders'

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    # 'dqd.image_pipelines.DownloadImagesPipeline':1,   #下载图片
    'dqd.redis_pipelines.DqdPipeline': 200,
    'scrapy_redis.pipelines.RedisPipeline': 300,
    'dqd.mongo_pipelines.MongoDBPipeline':400,
    'dqd.mysql_pipelines.MySQLPipeline': 1
}
IMAGES_STORE='.\Image'

# redis 在process_items.py文件中进行设置

#################    MONGODB     #############################
MONGODB_SERVER='localhost'
MONGODB_PORT=27017
MONGODB_DB='dqd_db'
MONGODB_COLLECTION='dqd_collection'

####################    MYSQL      #############################
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'dqd_database'
MYSQL_USER = 'root'
MYSQL_PASSWD = '******'

LOG_LEVEL = 'DEBUG'
DEPTH_LIMIT=1
# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 0.2

```

当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。

每个item pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的Python类。他们接收到Item并通过它执行一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。

- 清理HTML数据
- 验证爬取的数据(检查item包含某些字段)
- 查重(并丢弃)
- 将爬取结果保存到数据库中

**image_pipelines.py**

```
# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import codecs

class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)}) #添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标

        #图片文件名 
        image_guid = request.url.split('/')[-1]
        #图片下载目录  
        filename = u'full/{0}/{1}'.format(item['news_title'], image_guid)
        return filename

```
 以下图片为下载内容

![图片下载](http://upload-images.jianshu.io/upload_images/1242974-6fd8cbe3a8880971.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 
**redis_pipelines.py**

```
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

class DqdPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item

```
 在截图中，dqdspider中应该有3个队列，但是因为我已经下载完毕，所以`dqdspider:request`队列自动删除了。

- `dqdspider:request`待爬队列
- `dqdspider:dupefilter`用来过滤重复的请求
- `dqdspider:items`爬取的信息内容

![redis](http://upload-images.jianshu.io/upload_images/1242974-1b355ef6716ecce8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**mongo_pipelines.py**

```
# -*- coding:utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings
# from scrapy import log


class MongoDBPipeline(object):
    #Connect to the MongoDB database
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]



    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:

            self.collection.insert(dict(item))
            log.msg('question added to mongodb database!',
                    level=log.DEBUG,spider=spider)
        return item
```
为了展示MongoDB中的数据内容使用了管理工具Robomongo查看爬取的内容。


![Robomongo.png](http://upload-images.jianshu.io/upload_images/1242974-8031753fc6bc3477.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**mysql_pipelines.py**

```
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

```
在这里将爬取的信息进行清洗和转储。
 
![MySQL](http://upload-images.jianshu.io/upload_images/1242974-9375652d82588dd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 数据分析与展示


我懂（感觉好奇怪，人家还是很含蓄的，额，隔壁老王要喷我了，在他面前且叫你懂吧~）的每篇文章很有特色，每篇文章按主键自增，对应的URL都是唯一，所以我直接暴力爬取了全站的文章，但是这里为了快速加载数据只随机统计了部分爬取存入到MySQL中全部的文章数量。作为一名足球界的小菜鸟，当然要仔细分析数据，向老司机们学习，争取早日拿到驾照，安全驾驶。
 
## 文章数量

![爬取文章数量](http://upload-images.jianshu.io/upload_images/1242974-7351f28b04771c0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 发表文章作者

懂球帝的快速发展是离不开内部员工以及球迷们的辛勤耕耘的，且看这些带领懂球帝一路扶摇直上的老司机们都是哪些人，有时间就关注他们领略他们的“风骚”~

![作者发文数量](http://upload-images.jianshu.io/upload_images/1242974-513b87888df87c91.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

创业不易，不光要写文章，之前在懂球帝直播里，看了你懂的老司机陈老板带领的懂球帝足球队与宝坁碧水源的足球比赛，文武兼备，深入群众啊 


![陈老板](http://upload-images.jianshu.io/upload_images/1242974-216ee897ee34d7f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 内容来源

 作为国内以内容运营为主的最大足球媒介，除了自身实力过硬之外，还博采众长，从其他站点引进优质的“外援”。

![懂球帝原创](http://upload-images.jianshu.io/upload_images/1242974-7f9acb7ec269f283.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你可以感受下原创的文章数量与国外转载所占的比例，就知道为什么你懂在短短几年间吸引了这么多的用户。

![转载来源](http://upload-images.jianshu.io/upload_images/1242974-85a5eab012a77587.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从以上图表可以看出，文章主要还是来自自身原创文章，所以这里主要选取了其他网站来源的文章，从上图可以看出我懂转载的文章主要来自于推特、新华社、阿斯报以及天空体育等，这在一定程度上是对这些站点文章质量的认可。

## 文章评论分析
 
![文章全部评论](http://upload-images.jianshu.io/upload_images/1242974-f59f70f87bb6db18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


我们不光要分析作者的发文数量，还要分析用户的关注度，寻找出最具价值的老司机，很显然，GreatWall、elfiemini、鹰旗百夫长以微弱优势占据三甲。恩恩，懂球帝最受欢迎老司机新鲜出炉啦。

|作者|全部评论数量|热评数量|
|:----:|:----:|:----:|
|GreatWall|238738|21873|
|elfiemini|224058|23014|
|鹰旗百夫长|200386|10337|


![各年度评论数据](http://upload-images.jianshu.io/upload_images/1242974-9953252a7b9ea2bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
数据不能完全反应发展的实际情况，但不会撒谎，在一定程度上反应了懂球帝的快速发展。接下来，再单选2016年，评测各个月份的数据信息。

![2016年度评论数量](http://upload-images.jianshu.io/upload_images/1242974-685fc5e0b79cd0e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 
乍看一眼，我惊呆了！为毛从6月开始，这评论数量就增长的这么高，匪夷所思。实际上，在7月初欧洲杯开始，球迷的关注度提高，各种话题不断展开以至于评论数量突飞猛进。
 
还有许多数据信息可挖掘，其他信息下次再撸，最后供上评论区的老司机们。
 
![评论获赞](http://upload-images.jianshu.io/upload_images/1242974-05507f06760b092b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#参考资料
- scrapy-redis文档  
https://scrapy-redis.readthedocs.io/en/stable/readme.html
- redis-py文档 
http://redis-py.readthedocs.io/en/latest/
https://github.com/rolando/scrapy-redis
- [Python下用Scrapy和MongoDB构建爬虫系统
http://www.cnblogs.com/rrxc/p/4478936.html?utm_source=tuicool&utm_medium=referral
- 图片下载
http://doc.scrapy.org/en/latest/topics/item-pipeline.html
http://www.cnblogs.com/moon-future/p/5545828.html

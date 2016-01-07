# coding=utf8

'''
处理数据库链接模块。
需要在程序启动时引用一下该文件确保链接已经正常建立。
'''

from app import config

import pymongo
import mongoengine


host = config.get('mongo_host')
port = int(config.get('mongo_port'))
dbname = config.get('mongo_dbname')


#conn = mongoengine.connect(host=host, port=port, db=dbname,
#                           read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)

conn = mongoengine.connect(host=host, port=port, db=dbname)

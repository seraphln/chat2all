# coding=utf8

'''
处理数据库链接模块。
需要在程序启动时引用一下该文件确保链接已经正常建立。
'''

import pymongo
import mongoengine

from config import MONGO

conn = mongoengine.connect(read_preference=pymongo.ReadPreference.PRIMARY_PREFERRED,
                           **MONGO)


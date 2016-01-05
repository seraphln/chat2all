# coding=utf8
#

'''
配置模块。
使用一个单独的配置类来处理所有的配置信息
将所有的配置统一管理，
通过启动时传入的配置文件来选择开发配置或者是生产环境的配置
'''

from os.path import join, abspath, dirname
from ConfigParser import SafeConfigParser, NoOptionError

from singleton import Singleton


class Config(object):
    """use singleton avoid global variables"""
    __metaclass__ = Singleton

    SECTION_NAME = 'main'
    ACTUAL_CONFIG_FILE = None
    DEFAULT_CONFIG_FILE = abspath(join(dirname(__file__),
                                       '../conf/config.ini'))
    def __init__(self):
        self.load_config()

    def load_config(self):
        config_file = self.__class__.ACTUAL_CONFIG_FILE or self.__class__.DEFAULT_CONFIG_FILE
        self._cfg = SafeConfigParser()
        self._cfg.read([config_file, ])

    def get(self, option, section=None, value_type=str):
        return self._cfg._get(section or self.__class__.SECTION_NAME, value_type, option)

    def __getattr__(self, option):
        try:
            return self.get(option)
        except NoOptionError as e:
            print str(e)
            return None

if __name__ == '__main__':
    print Config().get('base_path')

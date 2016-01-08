# coding=utf8

import os
import tornado.web
import tornado.ioloop

import time
import pymongo
import datetime

from logger import getLogger

from sockjs.tornado import SockJSConnection, SockJSRouter, proto


db = pymongo.Connection()['map_demo']

logger = getLogger('demo')


config_dict = {'last_datetime': datetime.datetime.now(),
               'init_flag': False,
               'total_qps': 0,
               'distr': {'total': {},
                         'dongguan': {},
                         'tianjing': {},
                         'jiaxing': {},
                         'qingdao': {},
                         'fuzhou': {}}}

init_flag = False
total_qps = 0


class IndexHandler(tornado.web.RequestHandler):
    ''' '''
    def get(self):
        self.render('dynamic-attack/index.html')


class DemoConnection(SockJSConnection):
    ''' '''
    sockets = set()
    data = []
    attack_lst = []
    attacked_lst = []
    attacked_qps = 0

    def on_open(self, info):
        global init_flag
        self.sockets.add(self)
        if init_flag == False:
            print "INIT"
            init_flag = True
            self._load_data()
            self._sent_message()

            self.loop_load_data = tornado.ioloop.PeriodicCallback(self._load_data, 5000)
            self.loop_sent_message = tornado.ioloop.PeriodicCallback(self._sent_message, 5000)

            self.loop_load_data.start()
            self.loop_sent_message.start()
            print "DONE OF INIT"

    def _sent_message(self):
        ''' '''
        if not self.sockets:
            return

        global total_qps
        global config_dict
        now = datetime.datetime.now()
        now = time.mktime(now.timetuple())

        mapper = {'dongguan': u'东莞', 'tianjing': u'天津', 'jiaxing': u'嘉兴', 'qingdao': u'青岛', 'fuzhou': u'福州'}
        tmp_dict = {}

        for k, v in config_dict.get('distr', {}).iteritems():
            if k == 'total':
                continue
            tmp_dict[mapper[k]] = {'attack_lst': v.get('attack_lst', []),
                                   'attacked_lst': v.get('attacked_lst', []),
                                   'attacked_qps': v.get('attacked_qps'),
                                   'total': v.get('total')}

        result = {'status': 'ok', 'data': self.data, 'now': now,
                  'attack_lst': self.attack_lst, 'total': total_qps,
                  'attacked_lst': self.attacked_lst, 'qps': self.attacked_qps,
                  'dist_info': tmp_dict}
        logger.info('Get Total QPS: %s', total_qps)
        self.broadcast(self.sockets, result)


    def _do_load_province_data(self, pname, configs):
        ''' '''
        global total_qps
        result = []
        if not configs:
            configs.update({'cc_start': 0,
                            'cc_total_count': 0,
                            'per_page': 160,
                            'waf_start': 0,
                            'waf_total_count': 0,
                            'attack_dict': {},
                            'attacked_dict': {}})

        if pname == 'total':
            pname = 'message'

        cc_name, waf_name = generate_table_name(pname)

        cc_count = db[cc_name].count()
        waf_count = db[waf_name].count()

        if configs.get('cc_total_count') == 0:
            configs['cc_total_count'] = cc_count

        if configs.get('waf_total_count') == 0:
            configs['waf_total_count'] = waf_count

        if configs.get('cc_start') * configs.get('per_page') >= cc_count:
            configs['cc_start'] = 0

        if configs.get('waf_start') * configs.get('per_page') >= waf_count:
            configs['waf_start'] = 0

        cc_start = configs.get('cc_start')
        per_page = configs.get('per_page')
        waf_start = configs.get('waf_start')
        attack_dict = configs.setdefault('attack_dict', {})
        attacked_dict = configs.setdefault('attacked_dict', {})

        cc_data = list(db[cc_name].find().skip(cc_start*per_page).limit(per_page))
        waf_data = list(db[waf_name].find().skip(waf_start*per_page).limit(per_page))

        configs['cc_start'] = configs.get('cc_start', 0) + 1
        configs['waf_start'] = configs.get('waf_start', 0) + 1

        result.extend(format_data(cc_data))
        result.extend(format_data(waf_data))

        attack_qps = 0

        for r in result:
            attack_city = (r.get('attack_location') or {}).get('city')
            attacked_city = (r.get('attacked_location') or {}).get('city')
            try:
                qps = int(r.get('attacked_qps', '0'))
            except:
                qps = 0

            attack_dict[attack_city] = attack_dict.get(attack_city, 0) + qps
            attacked_dict[attacked_city] = attacked_dict.get(attacked_city, 0) + qps
            attack_qps += qps

        attack_lst = sorted(attack_dict.items(), key=lambda x: x[1], reverse=True)[:20]
        attacked_lst = sorted(attacked_dict.items(), key=lambda x: x[1], reverse=True)[:20]

        print attacked_lst, attacked_lst
        print '================'

        if pname == 'message':
            self.data = result
            self.attack_lst = attack_lst
            self.attacked_lst = attacked_lst
            self.attacked_qps = attack_qps
            total_qps += attack_qps
        else:
            total_qps += attack_qps
            configs['data'] = result
            configs['attack_lst'] = attack_lst
            configs['attacked_lst'] = attacked_lst
            configs['attacked_qps'] = attack_qps
            configs['total'] = configs.get('total', 0) + attack_qps


    def _load_data(self):
        ''' '''
        global config_dict
        global total_qps

        last_datetime = config_dict.get('last_datetime', datetime.datetime.now())
        now = datetime.datetime.now()

        if (now - last_datetime).days >= 1:
            total_qps = 0
            config_dict = {'last_datetime': datetime.datetime.now(),
                           'distr': {'total': {},
                                     'dongguan': {},
                                     'tianjing': {},
                                     'jiaxing': {},
                                     'qingdao': {},
                                     'fuzhou': {}}}

        for pname, configs in config_dict.get('distr', {}).iteritems():
            self._do_load_province_data(pname, configs)
        print config_dict.get('distr', {}).get('total')

    def on_close(self):
        self.sockets.remove(self)


if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    DemoRouter = SockJSRouter(DemoConnection, '/demo')

    # 2. Create Tornado application
    settings = {'static_path': os.path.join(os.path.dirname(__file__), 'dynamic-attack')}
    app = tornado.web.Application([(r"/", IndexHandler)] + DemoRouter.urls, **settings)

    # 3. Make Tornado app listen on port 8080
    app.listen(8766)
    print "Listening at 8766"

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()

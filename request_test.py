# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from kakou import Kakou
from union_kakou import UnionKakou

class UnionKakouTest(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5000
    
    def test_kakou_post(self):
        uk = UnionKakou(**{'host': self.host, 'port': self.port})
        data = [
            {
                'jgsj': arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                'hphm': '粤L70939',
                'kkdd_id': '441302004',
                'hpys_id': '0',
                'fxbh': 'IN',
                'cdbh':4,
                'img_path': 'http:///img/123.jpg'
            },
            {
                'jgsj': arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                'hphm': '粤L12345',
                'kkdd_id': '441302004',
                'hpys_id': '0',
                'fxbh': 'IN',
                'cdbh': 4,
                'img_path': 'http:///img/123.jpg',
                'cllx': 'K41'
            }
        ]

        r = uk.post_kakou(data)
        assert isinstance(r, dict) == True
        #assert r['headers'] == 201


class KakouTest(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5000

    def test_get_cltxs(self):
        k = Kakou(**{'host': self.host, 'port': self.port, 'city': 'hcq'})
        r = k.get_cltxs(123, 125)

        assert 'total_count' in r
        
    def test_get_maxid(self):
        k = Kakou(**{'host': self.host, 'port': self.port, 'city': 'hcq'})
        r = k.get_maxid()

        assert 'count' in r

if __name__ == '__main__':  # pragma nocover
    kt = UnionKakouTest()
    kt.test_kakou_post()


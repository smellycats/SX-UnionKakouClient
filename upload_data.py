﻿# -*- coding: utf-8 -*-
import time
import json

import arrow

from kakou import Kakou
from helper_kakou2 import Kakou as Kakou2
from union_kakou import UnionKakou
from sqlitedb import KakouDB
from ini_conf import MyIni
from my_logger import *


debug_logging(u'/home/logs/error.log')
logger = logging.getLogger('root')


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyIni()
        self.kk_ini = self.my_ini.get_kakou()
        self.uk_ini = self.my_ini.get_union()

        # request方法类
        self.kk = Kakou2(**self.kk_ini)
        self.uk = UnionKakou(**self.uk_ini)
	self.sq = KakouDB()
        #print self.uk_ini

        self.uk.status = True
        self.kk.status = True

        # ID上传标记
        self.id_flag = self.kk_ini['id_flag']
        self.step = 200

        self.hpys_id = {
            'WT': 0,
            'YL': 1,
            'BU': 2,
            'BK': 3,
            'QT': 4
        }

    def set_history_kakou(self):
	"""添加历史记录卡口"""
	maxid = self.kk.get_maxid()
	if self.id_flag + 30000 < maxid:
	    r = self.sq.add_idflag(self.id_flag+1, maxid)
	    self.set_id(maxid)
	    logger.info(r)
	logger.info('history has been set')

    def set_id(self, _id):
        """设置ID"""
        self.id_flag = _id
        self.my_ini.set_id(_id)
	logger.info(_id)

    def post_data(self, start_id, end_id):
	"""上传卡口数据"""
        car_info = self.kk.get_kakou(start_id, end_id)
        #print 'car_info count %s' % car_info['total_count']
        # 如果查询数据为0则退出
        if car_info['total_count'] == 0:
            return

        data = []
        for i in car_info['items']:
            if i['kkdd_id'] is None or i['kkdd_id'] == '':
		i['kkdd_id'] = '441302000'
            data.append({'jgsj': i['jgsj'],          # 经过时间
                         'hphm': i['hphm'],          # 号牌号码
                         'kkdd_id': i['kkdd_id'],    # 卡口地点ID
                         'hpys_id': self.hpys_id.get(i['hpys_code'], 4), # 号牌颜色ID
                         'fxbh': i['fxbh_code'],     # 方向编号
                         'cdbh': i['cdbh'],          # 车道
			 'clsd': i['clsd'],
			 'hpzl': i['hpzl'],
                         'img_path': i['imgurl']})   # 图片url地址
        r = self.uk.post_kakou(data)  #上传数据

    def post_info(self):
        print 'id_flag: %s' % self.id_flag
        """上传数据"""
        maxid = self.kk.get_maxid()
	#print 'maxid:%s' % maxid
        # 没有新数据则返回
        if maxid <= self.id_flag:
            return

        if maxid > (self.id_flag + self.step):
            last_id = self.id_flag + self.step
        else:
            last_id = maxid
        self.post_data(self.id_flag+1, last_id)
        # 设置最新ID
        self.set_id(last_id)

    def post_info2(self):
        """上传数据"""
	r = self.sq.get_idflag(banned=0)
	if r is None:
	    return
	if r[1] + self.step + 1 < r[2]:
	    last_id = r[1] + self.step
	else:
	    last_id = r[2]
	self.post_data(r[1], last_id)
        # 设置最新ID
        self.sq.set_idflag(r[0], last_id+1)
	# 结束此条历史记录
	if last_id == r[2]:
	    self.del_idflag(r[0])
	    

    def main_loop(self):
	ini_flag = False
        while 1:
	    if not ini_flag and self.kk.status and self.uk.status:
		self.set_history_kakou()
		ini_flag = True
            elif self.kk.status and self.uk.status:
                try:
                    self.post_info()
		    self.post_info2()
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
		    print self.kk.status
		    print self.uk.status
                    if not self.kk.status:
                        self.kk.get_maxid()
                        self.kk.status = True
                    if not self.uk.status:
                        self.uk.connect_test()
                        self.uk.status = True
                except Exception as e:
		    logger.error(e)
                    time.sleep(1)
        

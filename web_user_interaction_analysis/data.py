#-*- coding:utf-8 -*-

'''
Created on 2013-7-30

@author: Qiqun.H

'''

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from pprint import pprint
import MySQLdb
import datetime
from ConfigParser import SafeConfigParser
import sys
from DBUtils.PooledDB import PooledDB

count = len(sys.argv)
if count == 2:
	# python index.py develop
	environment = sys.argv[1]
elif count == 3:
	# python index.py 8080 develop
	environment = sys.argv[2]
else:
	environment = None
	
#environment = 'develop'

parser = SafeConfigParser()


def get_db_cfg():
	cfg_fpath = os.path.join(basepath, 'db.cfg') 

	parser.read(cfg_fpath)
	db_cfg = dict(parser.items(environment))
	
	db_cfg['port'] = int(db_cfg['port'])
	
	return db_cfg


def get_db_conn():
	db_cfg = get_db_cfg()
	table = db_cfg.pop('table')
	
	pool = PooledDB(MySQLdb,
					mincached=2, maxcached=2,
					maxshared=2, maxconnections=2,
					**db_cfg)
	
	conn = pool.connection()
	return conn, table


class WebUserInteractionAnalytics():
	def __init__(self):
		self.conn, self.table = get_db_conn()
		self.cur = self.conn.cursor()

	def get_last_login_datetime(self):
		output = []
		
		query = '''
				SELECT email, ip, MAX(create_date)
				FROM %s
				GROUP BY email
				ORDER BY MAX(create_date) DESC;''' % (self.table)
				
		self.cur.execute(query)
		records = self.cur.fetchall()
		
		for user, ip, last_login_time in records:
			date_time = last_login_time.strftime('%Y-%m-%d %H:%M:%S')
			output.append(map(str, [user, ip, date_time]))
	
		return output

	def get_all_info_for_one_user(self, user):
		output = []
		
		query = '''
				SELECT email, ip, create_date
				FROM %s
				where email = '%s'
				ORDER BY create_date DESC;''' % (self.table, user)
		
		self.cur.execute(query)

		records = self.cur.fetchall()
		for info in records:
			info = list(info)
			last_login_time = info[-1]
			date_time = last_login_time.strftime('%Y-%m-%d %H:%M:%S')
			info[-1] = date_time
			output.append(info)
	
		return output
	
	def close_conn(self):
		
		self.conn.close()
		
		return

	
if __name__ == "__main__":
	
	w = WebUserInteractionAnalytics()
 	pprint(w.get_last_login_datetime())
#  	pprint(w.get_all_info_for_one_user('mitani@sugarcrm.com'))
	w.close_conn()

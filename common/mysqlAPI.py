#-*- coding:utf-8 -*-

import sys
import MySQLdb
import traceback


class Mysql:
    def __init__(self, para, logger):
        # initial connection and cursor
        self.connection = 0
        self.cursor = 0
        self.insert_num = 0
        self.logger = logger

        # try to connect database
        try:
            # create connection to database
            self.connection = MySQLdb.connect(host=para['host'],
                                              port=para['port'],
                                              user=para['user'],
                                              passwd=para['pswd'],
                                              db=para['db'],
                                              charset="utf8")

            # create cursor
            self.cursor = self.connection.cursor()
        except Exception:
            traceback.print_exc()
            self.logger.error('connect to mysql failed')
            sys.exit()
        self.logger.info('connect to mysql success')

    def string2varchar(self, string):
        return self.connection.literal(string)

    def insert_init(self, record, table):
        varchars = map(self.string2varchar, record.values())

        sqlstr = "insert into %s (%s) values (%s)" % \
            (table, ", ".join(record.keys()), ", ".join(varchars))

        return sqlstr

    def update_init(self, record, find_dic, table):
        keys = record.keys()
        varchars = map(self.string2varchar, record.values())

        setstr = []
        for i in xrange(len(keys)):
            setstr.append(str(keys[i]) + "=" + varchars[i])

        find_key = find_dic.keys()[0]
        wherestr = find_key + "='" + str(find_dic[find_key]) + "'"

        sqlstr = "update %s set %s where %s" % \
            (table, ", ".join(setstr), wherestr)
        return sqlstr

    def execute(self, sqlstr):
        try:
            if sqlstr.lower().startswith('insert'):
                self.cursor.execute(sqlstr)
                id = self.connection.insert_id()
            elif sqlstr.lower().startswith('update'):
                self.cursor.execute(sqlstr)
                id = 0
            else:
                self.logger.error('sqlstr is not insert or update')
                id = 0

        except Exception:
            traceback.print_exc()
            self.logger.warn('insert data error')
            self.logger.warn(sqlstr)
            id = -1

        return id

    def find(self, sqlstr):
        try:
            self.cursor.execute(sqlstr)
        except Exception:
            self.logger.error('find sqlstr error')
            self.logger.error(sqlstr)
            traceback.print_exc()
        return self.cursor.fetchall()

    def findOne(self, sqlstr):
        try:
            self.cursor.execute(sqlstr)
        except Exception:
            self.logger.error('find sqlstr error')
            self.logger.error(sqlstr)
            traceback.print_exc()
        return self.cursor.fetchone()

    def find_step(self, sqlstr, step):
        flag = 0
        while True:
            temp = sqlstr + ' limit %s, %s' % (flag, step)
            flag += step
            records = self.find(temp)
            if len(records) == 0:
                break
            for record in records:
                yield record

    def insert_record(self, record, table):
        sqlstr = self.insert_init(record, table)

        id = self.execute(sqlstr)
        return id

    def update_record(self, id, record, table):
        sqlstr = self.update_init(record, {'id': id}, table)
        self.execute(sqlstr)

    def update(self, find_dic, record, table):
        sqlstr = self.update_init(record, find_dic, table)
        self.execute(sqlstr)

    def insert_if_not_exists(self, unique_key, unique_value, record, table):
        keys = record.keys()
        varchars = map(self.string2varchar, record.values())

        setstr = []
        for i in xrange(len(keys)):
            setstr.append(str(keys[i]) + "=" + varchars[i])

        sqlstr = "insert into %s set %s on duplicate key update %s=%s" % \
            (table, ", ".join(setstr), unique_key, unique_value)

        self.execute(sqlstr)

    def delete(self, table, key, value):
        sqlstr = "delete from %s where %s=%s" % (table, key, value)

        self.cursor.execute(sqlstr)

    def commit(self):
        self.connection.commit()

    def close(self):
        try:
            self.connection.close()
        except Exception:
            self.logger.error('break mysql connection failed')
            traceback.print_exc()

        self.logger.info('break mysql connection success')


if __name__ == "__main__":
    pass
#    config = ConfigParser.ConfigParser()
#    config.read('tag_to_mysql.cfg')
#
#    host = config.get('mysql', 'host')
#    port = int(config.get('mysql', 'port'))
#    user = config.get('mysql', 'user')
#    pswd = config.get('mysql', 'pswd')
#    db = config.get('mysql', 'db')
#    tag_table = config.get('mysql', 'tag_table')
#
#    mysql = Mysql(host, port, user, pswd, db)
#
#    mysql.close()

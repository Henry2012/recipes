#-*- coding:utf-8 -*-

import sys
import MySQLdb,traceback

class Mysql:
    def __init__(self,hst,prt,usr,pw,dbname):
        # initial connection and cursor
        self.connection = 0
        self.cursor = 0
        self.insert_num = 0

        # try to connect database
        try:
            # create connection to database
            self.connection = MySQLdb.connect(host=hst,port=prt,user=usr,passwd=pw,db=dbname, charset="utf8")

            # create cursor
            self.cursor = self.connection.cursor()
        except Exception:
            traceback.print_exc()
            print "[ ERROR ] connection failed"
            sys.exit()
        print "[ INFO ] connect to database success"

    def insert_init(self, record, table):
        values = record.values()

        for i in xrange(len(values)):
            if isinstance(values[i],str):
                values[i] = values[i].replace("\\"," ")
                values[i] = values[i].replace("'","\\'")
            else:
                values[i] = str(values[i])

        values = [x.replace("\\"," ") for x in values]
        values = [x.replace("'","\\'") for x in values]

        sqlstr = "insert into %s (%s) values('%s')" % (table, ", ".join(record.keys()), "', '".join(values))
        print sqlstr
        return sqlstr

    def update_init(self, record, find_dic, table):
        keys = record.keys()
        values = record.values()
        for i in xrange(len(values)):
            if isinstance(values[i],str):
                values[i] = values[i].replace("\\"," ")
                values[i] = values[i].replace("'","\\'")
            else:
                values[i] = str(values[i])

        values = [x.replace("\\"," ") for x in values]
        values = [x.replace("'","\\'") for x in values]

        setstr = []
        for i in xrange(len(keys)):
            setstr.append(str(keys[i]) + "='" + str(values[i]) + "'")

        find_key = find_dic.keys()[0]
        wherestr = find_key + "='" + str(find_dic[find_key]) + "'"

        sqlstr = "update %s set %s where %s" % (table, ", ".join(setstr), wherestr)
        return sqlstr

    def execute(self, sqlstr):
        try:
            sqlstr = sqlstr.strip()
            if (sqlstr.startswith('insert') or
                sqlstr.startswith('INSERT')):
                self.cursor.execute(sqlstr)
                corp_id = self.connection.insert_id()
            elif (sqlstr.startswith('update') or
                  sqlstr.startswith('UPDATE')):
                self.cursor.execute(sqlstr)
                corp_id = 0
            else:
                print '[ ERROR ] sqlstr not found'
                corp_id = 0

        except Exception:
            traceback.print_exc()
            print "[ WARN ] processing data error"
            #print sqlstr
            corp_id = -1

        return corp_id

    def find(self,sqlstr):
        try:
            self.cursor.execute(sqlstr)
        except Exception:
            print sqlstr
            traceback.print_exc()
        return self.cursor.fetchall()

    def findOne(self,sqlstr):
        try:
            self.cursor.execute(sqlstr)
        except Exception:
            traceback.print_exc()
        return self.cursor.fetchone()

    def find_step(self,sqlstr,step):
        flag = 0
        while True:
            temp = sqlstr + ' limit %s, %s' % (flag,step)
            flag += step
            records = self.find(temp)
            if len(records) == 0:
                break
            for record in records:
                yield record

    def insert_record(self, record, table):
        sqlstr = self.insert_init(record, table)

        corp_id = self.execute(sqlstr)
        return corp_id

    def insert_records(self, insert_keys, insert_value_package, table):
        #===============================================================================
        # 为了生成 INSERT INTO tbl_name (a,b,c) VALUES(1,2,3),(4,5,6),(7,8,9);
        # 1. 生成插入的字段
        # 2. 生成插入字段对应的所有值
        # 3. 整合成sqlstr
        #===============================================================================
        insert_keys_in_sqlstr = ",".join(insert_keys)

        all_insert_values_in_sqlstr = []
        for insert_values in insert_value_package:
            insert_values_in_sqlstr = []
            for each in insert_values:
                if isinstance(each, int):
                    each = "%d" % each
                elif each is None:
                    each = 'null'
                elif isinstance(each, basestring):
                    # 只有字符串才可以进行如此的字符替换
                    each = each.replace("\\"," ").replace("'","\\'")
                    each = "'%s'" % each

                insert_values_in_sqlstr.append(each)
            insert_values_in_sqlstr = map(str, insert_values_in_sqlstr)
            insert_values_in_sqlstr = "(" + ','.join(insert_values_in_sqlstr) + ")"
            all_insert_values_in_sqlstr.append(insert_values_in_sqlstr)
        all_insert_values_in_sqlstr = ','.join(all_insert_values_in_sqlstr)

        sqlstr = "insert INTO %s (%s) VALUES %s" % (table, insert_keys_in_sqlstr, all_insert_values_in_sqlstr)

        # execute SQL query
        record_id = self.execute(sqlstr)
        return record_id

    def update_record(self, corp_id, record, table):
        sqlstr = self.update_init(record, {'id':corp_id}, table)
        _ = self.execute(sqlstr)

    def update(self, find_dic, record, table):
        sqlstr = self.update_init(record, find_dic, table)
        _ = self.execute(sqlstr)

    def delete(self,table, key, value):
        sqlstr = "delete from %s where %s=%s" % (table, key, value)

        self.cursor.execute(sqlstr)

    def commit(self):
        self.connection.commit()

    def close(self):
        try:
            self.connection.close()
        except Exception:
            traceback.print_exc()
            print "[ ERROR ] break the connection failed"

        print "[ INFO ] break the connection "


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('tag_to_mysql.cfg')

    host = config.get('mysql', 'host')
    port = int(config.get('mysql', 'port'))
    user = config.get('mysql', 'user')
    pswd = config.get('mysql', 'pswd')
    db = config.get('mysql', 'db')
    tag_table = config.get('mysql', 'tag_table')

    mysql = Mysql(host, port, user, pswd, db)

    mysql.close()

#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: common.MongoAPI_QQ.py
Description: this program
Creation: 2014-1-2
Revision: 2014-1-2
"""

class MongoEye():
    pymongo = __import__('pymongo')
    
    def __init__(self,
                 mongo_host='192.168.0.116',
                 mongo_database='esdb',
                 mongo_port=27017):
        # connect to mongodb
        self.conn = MongoEye.pymongo.MongoClient(host=mongo_host,
                                               port=mongo_port)

        # go to database
        self.db = self.conn[mongo_database]
        self.collections = self.db.collection_names()
    
    def show_collections(self):
        '''
        Usage:
        e = TheEye(mongo_database='nlp')
        for k, v in e.show_collections().iteritems():
            print k, v
            
        Every database has a collection called 'system.indexes'
        '''
        
        statistics = dict()
        for collection_name in self.collections:
            if collection_name == 'system.indexes':
                continue
            col = self.db[collection_name]
            statistics.setdefault(collection_name, col.count()) 
            
        self.conn.disconnect()
        
        return statistics

    def get_records(self, collection, find_dic):
        # get collection
        col = self.db[collection]

        # get all unused
        records = col.find(find_dic, timeout=False).sort('_id', 1)

        for record in records:
            yield record

    def show_all_possible_keys(self, collection):
        keys = []
        
        records = self.get_records(collection, {})
        for record in records:
            keys.extend(record.keys())

        return set(keys)            
    
    def getId(self, collection):
        o = self.db['counters'].find_and_modify(query={'_id': collection}, update={'$inc': {'c': 1}})
        return o['c']

    def get_record_return(self, collection, find_dic, get_dic):
        # get collection
        collect = self.db[collection]

        # get all unused
        records = collect.find(find_dic, get_dic, timeout=False)

        for record in records:
            yield record

    #this function changes the value of a key in a dictionary
    def update(self, collection, find_dic, new_record):
        collect = self.db[collection]
        
        # insert into collection
        collect.update(find_dic, {'$set': new_record})
        
    def unset(self, collection, find_dic, rm_record):
        collect = self.db[collection]

        # insert into collection
        collect.update(find_dic, {'$unset': rm_record})

    #this function is to add something new into records relating to some specific "corp_id"
    def push(self, collection, find_dic, push_dic):
        collect = self.db[collection]

        # push the record to one column
        collect.update(find_dic, {'$push': push_dic})

##    def pushToDetail(self, collection, find_dic, key_level1, key_level2, value_level2, update_dic):
##        collect = self.db[collection]
##
##        # db.pc_test.update({_id:0,          'set.url':'www.baidu.com'},         {$push:   {'set.$.minor_id_new':          "3"}},             false, true)
##        # collect.update   ({find_dic,  'key_level1.key_level2':'value_level2'}, {'$push': {'key_level1.$.update_dic_key': update_dic_value}},False, True) 
##        #                     find_detail,                                                   push_dic
##        find_detail = find_dic.copy()
##        find_detail[key_level1+'.'+key_level2] = value_level2
##
##        push_dic_key = key_level1+'.$.'+update_dic.keys()[0]
##        push_dic_value = update_dic.values()[0]
##        push_dic = {push_dic_key : push_dic_value}
##
##        collect.update(find_detail, {'$push':push_dic}, False,False,False,True)
        
    #this function is to remove something new from records relating to some specific "corp_id" 
    def pullFromSet(self, collection, find_dic, del_dic):
        collect = self.db[collection]

        # add the record to one column
        collect.update(find_dic, {'$pull': del_dic})

##    def addToSet(self, collection, find_dic, set_dic):
##        collect = self.db[collection]
##
##        # add the record to one column
##        collect.update(find_dic, {'$addToSet': set_dic})

    #insert all records relating to a specific "corp_id" into mongoDB
    def insert(self, collection, new_record):
        collect = self.db[collection]

        collect.insert(new_record)
    
    def disconnect(self):
        self.conn.disconnect()
        
    def remove_all(self):
        for collection_name in self.collections:
            col = self.db[collection_name]
            col.remove({})
            
        self.disconnect()

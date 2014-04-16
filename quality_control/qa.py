#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: quality_control.qa_for_es_root_signals.py
Description: this program gives assessment for ES_root_signals.
Creation: 2014-1-14
Revision: 2014-1-14
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# Based on one collection, STATs from 2 views: (平均10分钟)
#     1. basic STAT
#     2. detailed STAT (1000s)
#             1. existing
#             2. all fields
#             3. type checking
#             4. nullable
#             5. empty
#===============================================================================

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

import json
import pdb
import pymongo
from bson.code import Code
from collections import defaultdict
from ConfigParser import ConfigParser
from timer import Timer
from utils import (EMPTY_VALUE_MAPPING,
                   get_current_time,
                   make_dirs)

class MongoEye(object):
    def __init__(self, mongo_uri, db_name, col_name):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.col = self.db[col_name]
    
    def close(self):
        self.client.close()

    #===============================================================================
    # basic STAT
    #     1. # documents
    #     2. # domains
    #     3. # unique domains
    #===============================================================================

    def get_basic_stat(self, merger_fpath,
                       basic_stat_fpath,
                       domain_fpath):
        (all_documents_counter,
         all_domains_counter,
         all_unique_domains_counter) = 0, 0, 0

        all_documents_counter = self.col.find().count()

        with open(merger_fpath) as f:
            for line in f:
                splitted = line.split('\t')
                if splitted[0] == 'domain':
                    existing, empty, nullable = map(int, splitted[2:5])
                    all_domains_counter = existing - empty - nullable

        #empty = EMPTY_VALUE_MAPPING.values()
        #empty.append(None)

        # time consumed for distinct domains: 539.521000147s
#         for i, each in enumerate(self.col.distinct("domain")):
#             if not (i % 100):
#                 print "%s/%s" % (i + 1, all_domains_counter)
#
#             if each not in empty:
#                 all_unique_domains_counter += 1

        # Alternative way to count unique domains
        with open(domain_fpath) as f:
            domains = json.load(f)
            all_unique_domains_counter = len(domains)

        with open(basic_stat_fpath, "w") as wf:
            wf.write("# documents\t%s" % int(all_documents_counter) + '\n')
            wf.write("# domains\t%s" % int(all_domains_counter) + '\n')
            wf.write("# unique domains\t%s" % int(all_unique_domains_counter) + '\n')

    def count_domains(self):
        output = set()

        mapper = Code("function() {"
               "    emit(this.domain, null);}")

        reducer = Code("function(key, values) {return null;}")

        # Add "limit" option for development env
        #options = {"jsMode": 1, "limit": 100000}
        # production env
        options = {"jsMode": 1}

        for doc in self.col.inline_map_reduce(mapper, reducer, **options):
            # One example of doc is {u'_id': u'_id', u'value': [1000.0]}
            print doc
            #raw_input()

            key = doc['_id']
            output.add(key)

        return list(output)

    def save_domain_counters(self, domain_fpath):
        domains = self.count_domains()

        with open(domain_fpath, 'w') as wf:
            wf.write(json.dumps(domains))

    #===============================================================================
    # detailed STAT for all fields
    #     1. existing
    #     684.508000135s
    #===============================================================================

    def existing_checking(self):
        output = {}

        mapper = Code("function() {"
               "    for (var key in this)"
               "    emit(key, 1);}")

        reducer = Code("function(key, values) {return Array.sum(values);}")

        # Add "limit" option for development env
        #options = {"jsMode": 1, "limit": 1000}
        # production env
        options = {"jsMode": 1}

        for doc in self.col.inline_map_reduce(mapper, reducer, **options):
            # One example of doc is {u'_id': u'_id', u'value': [1000.0]}
            #print doc

            key = doc['_id']
            existing = doc['value']
            if isinstance(existing, float):
                existing = int(existing)
            elif (isinstance(existing, list) and
                  len(existing) == 1):
                existing = int(existing[0])
            output[key] = existing
        return output

    def save_existing_checking(self, existing_checking_fpath):
        with Timer() as t:
            output = self.existing_checking()

        with open(existing_checking_fpath, 'w') as wf:
            wf.write(json.dumps(output))

        print "[ INFO ] time consumed for checking existing: %ss" % t.interval
        print "[ INFO ] existing checking is done."

    #===============================================================================
    # Get all fields
    #     2. all fields
    #===============================================================================

    def save_fields(self, existing_checking_fpath, field_fpath):
        with open(existing_checking_fpath) as f:
            output = json.load(f)

        with open(field_fpath, 'w') as wf:
            wf.write(json.dumps(output.keys()))

        print "[ INFO ] field collector is done."

    def get_fields(self, field_fpath):
        with open(field_fpath) as f:
            return json.load(f)

    #===============================================================================
    # detailed STAT for all fields
    #     3. type checking
    #     Time consumed: 104s only for 1000 documents
    #===============================================================================

    def type_checking(self, field_fpath):
        output = defaultdict(lambda: set())
        fields = self.get_fields(field_fpath)

        # for production
        # If find() without no limits, the speed will be too slow.
        # So we assume 1000 documents could represent all the documents/
        for doc in self.col.find().limit(1000):
        #for doc in col.find():
            for field in fields:
                if field not in doc:
                    continue
                value_type = type(doc[field]).__name__
                if value_type == "NoneType":
                    continue
                output[field].add(value_type)

        return output

    def save_type_checking(self, type_checking_fpath, field_fpath):
        with Timer() as t:
            output = self.type_checking(field_fpath)

        new_output = {}
        for k, v in output.iteritems():
            new_output[k] = list(v)

        with open(type_checking_fpath, "w") as wf:
            wf.write(json.dumps(new_output))

        print "[ INFO ] time consumed for checking type: %ss" % t.interval
        print "[ INFO ] type checking is done."

    #===============================================================================
    # detailed STAT for all fields
    #     4. nullable
    #     time consumed for checking nullable: 115.10800004s
    #===============================================================================

    def nullable_checking(self, field_fpath):
        output = {}
        fields = self.get_fields(field_fpath)

        count_of_fields = len(fields)

        for i, field in enumerate(fields):
            print "[ INFO ] # of keys processed for nullable checking: %s/%s" % (i + 1, count_of_fields)
            query = {field: {'$type': 10}}
            nullable = self.col.find(query).count()
            output[field] = nullable

        return output

    def save_nullable_checking(self, field_fpath, nullable_checking_fpath):
        with Timer() as t:
            output = self.nullable_checking(field_fpath)

        with open(nullable_checking_fpath, "w") as wf:
            wf.write(json.dumps(output))

        print "[ INFO ] time consumed for checking nullable: %ss" % t.interval
        print "[ INFO ] nullable checking is done."

    #===============================================================================
    # detailed STAT for all fields
    #     5. empty
    #     Give counts when a field exists and its value is empty. (Available for str, list, dict)
    #     Timer consumed: 29s
    #===============================================================================

    def empty_checking(self, type_checking_fpath):
        output = {}
        with open(type_checking_fpath) as f:
            type_checking_records = json.load(f)

        count_of_fields = len(type_checking_records)

        for i, field in enumerate(type_checking_records):
            print "[ INFO ] # of keys processed for empty checking: %s/%s" % (i + 1, count_of_fields)
            allowed_types = type_checking_records[field]
            #print allowed_types
            allowed_empty_values = []
            for t in allowed_types:
                if t in EMPTY_VALUE_MAPPING:
                    allowed_empty_values.append(EMPTY_VALUE_MAPPING[t])

            #print allowed_empty_values
            if not allowed_empty_values:
                output[field] = 'N/A'
            else:
                query = {field: {'$in': allowed_empty_values}}
                #print query
                empty = self.col.find(query).count()
                output[field] = empty

        return output

    def save_empty_checking(self, type_checking_fpath, empty_checking_fpath):
        with Timer() as t:
            output = self.empty_checking(type_checking_fpath)

        with open(empty_checking_fpath, "w") as wf:
            wf.write(json.dumps(output))

        print "[ INFO ] time consumed for checking empty: %ss" % t.interval
        print "[ INFO ] empty checking is done."

    #===============================================================================
    # Merger the above 4:
    #     1. type checking
    #     2. existing
    #     3. nullable
    #     4. empty
    # Calculate coverage:
    #     1 - (nullable+empty)/existing
    #===============================================================================

    def calculate_coverage(self, existing_checking_fpath,
                           nullable_checking_fpath,
                           empty_checking_fpath):
        output = {}

        with Timer() as t:
            # get values from the three source files
            with open(existing_checking_fpath) as f1:
                existing_checking = json.load(f1).items()
                existing_checking.sort()
            with open(nullable_checking_fpath) as f2:
                nullable_checking = json.load(f2).items()
                nullable_checking.sort()
            with open(empty_checking_fpath) as f3:
                empty_checking = json.load(f3).items()
                empty_checking.sort()
            assert ([field for field, _ in existing_checking] ==
                    [field for field, _ in nullable_checking] ==
                    [field for field, _ in empty_checking])

            # calculate the coverage
            for i, (field, counter) in enumerate(existing_checking):
                existing = counter
                nullable = nullable_checking[i][1]
                empty = empty_checking[i][1]

                if empty == "N/A":
                    empty = 0

                coverage = 1 - (nullable + empty) / float(existing)
                output[field] = coverage

        print "[ INFO ] time consumed for merger: %ss" % t.interval
        print "[ INFO ] merger is done."

        return output

    def save_coverage(self, existing_checking_fpath,
                    nullable_checking_fpath,
                    empty_checking_fpath,
                    coverage_fpath):
        coverage = self.calculate_coverage(existing_checking_fpath,
                                           nullable_checking_fpath,
                                           empty_checking_fpath)
        with open(coverage_fpath, "w") as wf:
            wf.write(json.dumps(coverage))

    def merger(self,
               field_fpath,
               type_checking_fpath,
               existing_checking_fpath,
               nullable_checking_fpath,
               empty_checking_fpath,
               coverage_fpath,
               merger_fpath):
        fields = self.get_fields(field_fpath)
        fields.sort()

        with open(existing_checking_fpath) as f1:
            existing_checking = json.load(f1)
        with open(nullable_checking_fpath) as f2:
            nullable_checking = json.load(f2)
        with open(empty_checking_fpath) as f3:
            empty_checking = json.load(f3)
        with open(coverage_fpath) as f4:
            coverage_checking = json.load(f4)
        with open(type_checking_fpath) as f5:
            type_checking = json.load(f5)

        with open(merger_fpath, "w") as wf:
            wf.write('\t'.join(['Field', 'Type', '# existing',
                                '# empty', '# nullable', 'Coverage']) + "\n")
            for field in fields:
                types = "::".join(type_checking[field])
                coverage = "%.3f" % coverage_checking[field]
                line = [field, types,
                        existing_checking[field],
                        empty_checking[field],
                        nullable_checking[field],
                        coverage]
                line = "\t".join(map(str, line)) + "\n"
                wf.write(line)

    def get_field_distribution(self, field):
        output = {}

        mapper = Code("function() {emit(this.%s, 1);}" % field)

        reducer = Code("function(key, values) {return Array.sum(values);}")

        # Add "limit" option for development env
        #options = {"jsMode": 1, "limit": 1000}
        # production env
        options = {"jsMode": 1}

        for doc in self.col.inline_map_reduce(mapper, reducer, **options):
            # One example of doc is {u'_id': u'_id', u'value': [1000.0]}
            #print doc
            #raw_input()

            key = doc['_id']
            existing = doc['value']
            if isinstance(existing, float):
                existing = int(existing)
            elif (isinstance(existing, list) and
                  len(existing) == 1):
                existing = int(existing[0])
            output[key] = existing
        return output

    def get_field_distribution_v2(self, field):
        output = {}
        distinct_values = self.col.distinct(field)

        for value in distinct_values:
            counter = self.col.find({field: value}).count()
            output[value] = counter
        return output

    def save_field_distribution(self, field, field_dist_fpath):
        with Timer() as t:
            output = self.get_field_distribution_v2(field)
        print "[ INFO ] time consumed for get __%s__ distribution: %.3f" % (field, t.interval)
        with open(field_dist_fpath, "w") as wf:
            wf.write(json.dumps(output))


def collection_qa_analyzer(col_name, env='active', fields=None):
    # parse configuration file
    cfg_fpath = os.path.join(basepath, "db_and_fpath.cfg")
    parser = ConfigParser()
    parser.read(cfg_fpath)

    # get detailed info from configuration
    mongo_uri = parser.get(env, 'uri')
    db_name = parser.get(env, 'db_name')
    io_fpath = parser.get(env, 'io_fpath')

    # get current time in string
    current_time = get_current_time(flag='short')

    # create directories if not existing, and return the collection's path
    col_fpath = make_dirs(io_fpath, current_time, db_name, col_name)

    # get all file paths that are required
    basic_stat_fpath = os.path.join(col_fpath, 'basic_stat.json')
    domain_fpath = os.path.join(col_fpath, 'domain.json')
    existing_checking_fpath = os.path.join(col_fpath, 'existing.json')
    field_fpath = os.path.join(col_fpath, 'fields.json')
    type_checking_fpath = os.path.join(col_fpath, 'type_checking.json')
    nullable_checking_fpath = os.path.join(col_fpath, 'nullable.json')
    empty_checking_fpath = os.path.join(col_fpath, 'empty.json')
    coverage_fpath = os.path.join(col_fpath, 'coverage.json')
    merger_fpath = os.path.join(col_fpath, 'merger.txt')

    # MongoEye
    mongoEye = MongoEye(mongo_uri, db_name, col_name)

    # get detailed STAT
    mongoEye.save_existing_checking(existing_checking_fpath)
    mongoEye.save_fields(existing_checking_fpath, field_fpath)
    mongoEye.save_type_checking(type_checking_fpath, field_fpath)
    mongoEye.save_nullable_checking(field_fpath, nullable_checking_fpath)
    mongoEye.save_empty_checking(type_checking_fpath, empty_checking_fpath)
    mongoEye.save_coverage(existing_checking_fpath,
                           nullable_checking_fpath,
                           empty_checking_fpath,
                           coverage_fpath)
    mongoEye.merger(field_fpath, type_checking_fpath,
                    existing_checking_fpath, nullable_checking_fpath,
                    empty_checking_fpath, coverage_fpath, merger_fpath)
    
    # get basic STAT
    mongoEye.save_domain_counters(domain_fpath)
    mongoEye.get_basic_stat(merger_fpath, basic_stat_fpath, domain_fpath)
    
    # test count unique domains
    #print mongoEye.count_domains()

    #===============================================================================
    # 获得某一个字段值的分布(distribution)
    #===============================================================================
    if fields:
        field_dist_collector(mongoEye, fields, col_fpath)

def field_dist_collector(mongo, fields, col_fpath):
    for field in fields:
        field_dist_fpath = os.path.join(col_fpath, '%s_dist.json' % field)
        sorted_field_dist_fpath = os.path.join(col_fpath, '%s_dist_sorted.txt' % field)
        mongo.save_field_distribution(field, field_dist_fpath)

        with open(field_dist_fpath) as f:
            field_dist = json.load(f).items()

        field_dist.sort(key=lambda k: k[1], reverse=True)
        with open(sorted_field_dist_fpath, 'w') as wf:
            for k, v in field_dist:
                wf.write("\t".join([k, str(v)]) + '\n')


if __name__ == "__main__":
    col_name = "zoominfo_comp_backup"
#     col_name = "zoominfo_people_backup"
    col_names = ['zoominfo_comp_backup']
    fields = ['city',
              'state',
              'zip']
    for col_name in col_names:
        with Timer() as t:
            collection_qa_analyzer(col_name, env='active', fields=fields)
        print "[ INFO ] total time consumed: %ss for %s" % (t.interval, col_name)

#-*- coding: utf-8 -*-
'''
Created on Sep 9, 2013

@author: pz
'''

from file_system import (get_merged_fpath,
                         get_entity_extractor_fpath,
                         get_news_id_fpath)
from mysqlAPI import Mysql

def extract_entity_without_db(ofpath, wfpath):
    host = "esdev-mysql.cloudapp.net"
    port = 3306
    user = "esapp"
    pwd = "esapp1"
    dbname = "mscndemo"
    db = Mysql(host, port, user, pwd, dbname)

    count = 0
    companies = db.find('select * from company')
    with open(wfpath, "w") as wf:
        with open(ofpath) as of:
            for line in of:
                title = get_title(line)
                related_comp = []
                for each in companies:
                    short_name = each[2]
                    #for _ in each:
                    #    print _
                    #print short_name
                    if short_name in title:
                        related_comp.append(short_name)
                if related_comp:
                    new_line = "\t".join([line.strip(), ">|<".join(related_comp)])
                    wf.write(new_line + '\n')
                    count += 1
    return count

def extract_entity(current_dir, concerned_date):

    ofpath = get_merged_fpath(current_dir, concerned_date)
    wfpath = get_entity_extractor_fpath(current_dir, concerned_date)
    print ofpath, wfpath

    host = "esdev-mysql.cloudapp.net"
    port = 3306
    user = "esapp"
    pwd = "esapp1"
    dbname = "mscndemo"
    db = Mysql(host, port, user, pwd, dbname)

    indy = []
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AShrCSRCName.txt') as f1:
        for line in f1:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AshrMotifName.txt') as f2:
        for line in f2:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AShrSWName_modified.txt') as f3:
        for line in f3:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    indy_words = list(set(indy))
    #print len(indy_words)

    filenames = [ofpath]
    id = int(db.findOne('select count(*) from news')[0])
    with open(get_news_id_fpath(current_dir), 'w') as wf:
        wf.write(str(id))
    for filename in filenames:
        output = open(wfpath, 'w')
        f = open(filename, 'r')
        for line in f:
            #print line
            id = id + 1
            publish_date = line.split('>|<')[1].strip('\t').strip('\r').strip('\n')
            title = line.split('>|<')[2].strip('\t').strip('\r').strip('\n')
            if ('最多' in title or '排名前' in title) and ('股' in title or '板块' in title):
                continue
            output_line = str(id) + '|' + publish_date + '|'
            for record in db.find('select * from company'):
                symbol = record[1]
                short_name = record[2]
                full_name = record[3]
                if '证券' in short_name or '证券' in full_name:
                    continue
                if symbol in line:
                    output_line += symbol+':'+str(line.count(symbol))+';'
                if short_name in line:
                    output_line += short_name+':'+str(line.count(short_name))+';'
                if full_name in line:
                    output_line += full_name+':'+str(line.count(full_name))+';'

            output_line = output_line.rstrip(';')+'|'
            for word in indy_words:
                if word in line:
                    output_line += word+':'+str(line.count(word))+';'
            output_line = output_line.rstrip(';')+'\n'
            #print output_line
            output.write(output_line)
            if id % 1000 == 0:
                print id
                output.flush()
    db.close()

def get_title(line):
    return line.strip().split("\t")[1]

def get_indy():
    indy = []
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AShrCSRCName.txt') as f1:
        for line in f1:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AshrMotifName.txt') as f2:
        for line in f2:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    with open('/mnt/data/CN-NLP-DATA/Corpus/INDY_AShrSWName_modified.txt') as f3:
        for line in f3:
            indy.append(line.strip('\n').strip('\t').strip('\r'))
    indy = list(set(indy))

    return indy

if __name__ == "__main__":
    ofpath = "io/news_200k_300k.txt"
    wfpath = "io/entity_extracted_from_news_200k_300k.txt"
    extract_entity_without_db(ofpath, wfpath)

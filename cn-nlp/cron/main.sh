#! /bin/bash

cd /mnt/data/qiqun.h/crawler_output/crawler-2014
java -jar /mnt/data/qiqun.h/crawler_output/crawler-2014/crawler-zzw-2014-v2.jar

now=`date +"%Y-%-m-%-d"`
python /mnt/data/qiqun.h/cn-nlp/cron/main.py $now

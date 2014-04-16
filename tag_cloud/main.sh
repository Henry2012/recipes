#! /bin/bash
#cd /mnt/data/zzf/zzw_data
#java -jar /mnt/data/zzf/zzw_data/crawler-zzw-now.jar
#cd /mnt/data/zzf/zqsbw_data
#java -jar /mnt/data/zzf/zqsbw_data/crawler-zqsbw-now.jar
now=`date +"%Y-%-m-%-d"`
#cat /mnt/data/zzf/zzw_data/$now.txt >> /mnt/data/qiqun.h/tag_cloud/io/merged/$now.txt
#cat /mnt/data/zzf/zqsbw_data/$now.txt >> /mnt/data/qiqun.h/tag_cloud/io/merged/$now.txt
python /mnt/data/qiqun.h/tag_cloud/main.py $now

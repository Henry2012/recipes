#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.merge_counters.py
Description: this program merges multiple sources of counters.
Creation: 2014-1-8
Revision: 2014-1-8
"""

from collections import defaultdict

mapping = {"company": "companies",
           "tag": "tags"}

def merge_counters(flag, today):
    entity = mapping[flag]
    one_prefix = "../io/zqsbw_counters/%s/%s_%s090000.txt"
    two_prefix = "../io/counters/%s/%s_%s090000.txt"
    merged_prefix = "../io/counters_merged/%s/%s_%s090000.txt"

    one_counter_fname = one_prefix % (entity, entity, today)
    two_counter_fname = two_prefix % (entity, entity, today)
    merged_counter_fname = merged_prefix % (entity, entity, today)

    counters = defaultdict(lambda: 0)
    for fname in [one_counter_fname, two_counter_fname]:
        with open(fname) as f:
            for line in f:
                key, value = line.strip().split("::")
                value = int(value)
                counters[key] += value

    sorted_counters = sorted(counters.items(), key=lambda k: k[1], reverse=True)

    with open(merged_counter_fname, "w") as wf:
        for k, v in sorted_counters:
            v = str(v)
            wf.write("::".join([k, v]) + "\n")

if __name__ == "__main__":

    today = "20140108"
    for each in ["company", "tag"]:
        merge_counters(each, today)

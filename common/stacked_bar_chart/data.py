# -*- coding: utf-8 -*-

import pdb
import json

'''
Created on 2013-7-3

@author: Qiqun Han
'''

'''
meta-data should be look like:
    event_type    comp_id   count_of_events
    
Then dataset is like:
    [[event_type_0, comp_id_0, count_of_events_0],
     [event_type_1, comp_id_1, count_of_events_1],
     ...]
'''

def preprocess_dataset():
    
    dataset = []
    
    with open("event_breakdown.txt").xreadlines() as f:
        for line in f:
            '''
            Transfrom the following string 
            '\'\'\t\'{"count": 524, "type": "AWARD", "name": "NONE"}\'\n'
            ...
            
            To the required dataset
            [["AWARD", "NONE", 524],
             ...]
            '''
            info = eval(eval(line))
            
            # produce meta_data
            event_type = info['type']
            comp_name = info['name']
            count_of_events = info['count']
            meta_data = [event_type, comp_name, count_of_events]
            
            dataset.append(meta_data)
    
    # sort based on count_of_events
    dataset.sort(key=lambda k: k[2], reverse=True)
    
    # sort based on event_type
    # ATTENTION: when multiple records have the same key, the original order is preserved.
    dataset.sort(key=lambda k: k[0])
    
    json.dump(dataset, open("event_breakdown.json", "wb"))
    
    return dataset
        
def get_dataset():
    dataset = None
    '''
    dataset = [
            ["ma", "1234", 1000],
            ["fr", "1234", 500],
            ["sp", "1234", 644],
            ["ma", "123", 542],
            ["fr", "123", 123],
            ["sp", "123", 444],
            ["ma", "23", 379],
            ["fr", "23", 359],
            ["sp", "23", 489],
            ["ma", "234", 2000],
            ["fr", "234", 856],
            ["sp", "234", 777],]
            
    Here dataset is sorted.
    '''
    
    with open("event_breakdown.json").xreadlines() as f:
        
        for line in f:
            dataset = eval(line)
            break
        
#     pdb.set_trace()
    
    return dataset

def get_global_features(dataset):
    '''
    Here dataset is sorted.
    
    event_types:
    {event_type_0: [count_of_events_with_event_type_0, first_index_for_event_type_0],
     event_type_1: [count_of_events_with_event_type_1, first_index_for_event_type_1],
     ...}
     
    companies:
    {comp_0: count_of_events_with_comp_0,
     comp_1: count_of_events_with_comp_1,
     ...}
    '''
    
    event_types = {}
    companies = {}
    
    for i, (event_type, comp_id, count_of_events) in enumerate(dataset):
        event_types.setdefault(event_type, [0, 0])
        event_types[event_type][0] += count_of_events
        
        if not i:
            event_types[event_type][1] = i
        
        # Decide whether or not the 1st index for each event type should be updated.
        # Update if event_type is different from the last event_type and vice versa.
        elif (event_type != last_event_type):
            event_types[event_type][1] = i
            
        companies.setdefault(comp_id, 0)
        companies[comp_id] += count_of_events
        
        last_event_type = event_type
        
    return event_types, companies

def convert_comp_id_to_comp_name(comp_id):
    comp_name = "Everstring"
    return comp_id
        
class EventBreakdown():
    
    def __init__(self, dataset):
        
        # get other global features: event_types & companies
        event_types, companies = get_global_features(dataset)
        
        # all global features
        self.dataset = dataset
        self.event_types = event_types
        self.companies = companies
    
    def break_down_events(self, count_of_top_companies):
        '''
        Output arguments:
        1. event_type_breakdown
        2. event_type_names
        
        event_type_breakdown:
        [
            [events_of_other_comps, 
            [top_n_comp, events_of_top_nth], 
            ...
            [top_1_comp, events_of_top_1st]],
            
            [events_of_other_comps, 
            [top_n_comp, events_of_top_nth], 
            ...
            [top_1_comp, events_of_top_1st]],
         ...]
         
        event_type_names:
        Event_type with the biggest number comes first in event_type_names.
        '''
        event_type_breakdown = []
        event_type_names = []
        
        # sort based on # of events for each event type
        event_types = sorted(self.event_types.items(), key=lambda k: k[1][0], reverse=True)
        
        for event_type, [count_of_events, first_index] in event_types:
            top_n = [[convert_comp_id_to_comp_name(each[1]), each[2]] for each in self.dataset[first_index: first_index + count_of_top_companies]]
            
            events_of_top_n = sum(count_of_events for comp_id, count_of_events in top_n)
            events_of_other_comps = count_of_events - events_of_top_n
            
            top_n.append(events_of_other_comps)
            top_n.reverse()
            
            event_type_breakdown.append(top_n)
            event_type_names.append(event_type)
            
        return zip(*event_type_breakdown), event_type_names

if __name__ == "__main__":
    
#     dataset = get_dataset()
#     eventBreakdown = EventBreakdown(dataset)
#     event_type_breakdown, event_type_names = eventBreakdown.break_down_events(3)
#     pdb.set_trace()

#     preprocess_dataset()
    print get_dataset()
    
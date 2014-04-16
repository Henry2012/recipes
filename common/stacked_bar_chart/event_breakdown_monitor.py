# -*- coding: utf-8 -*-

'''
Created on 2013-7-4

@author: Qiqun Han
'''

import web
import data
import pdb

urls = (
        '/', 'monitor',
        )

render = web.template.render('templates/')

class monitor:
    def GET(self):
        # top_n
        count_of_top_companies = 3
        
        dataset = data.get_dataset()
        eventBreakdown = data.EventBreakdown(dataset)
        event_type_breakdown, event_type_names = eventBreakdown.break_down_events(count_of_top_companies)
        
#         pdb.set_trace()
        return render.event2comp(event_type_breakdown, event_type_names, count_of_top_companies)
    
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()


#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: screenshot.py
Description: this program
Creation: 2013-12-2
Revision: 2013-12-2
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#!/usr/bin/python

# This file is released into the public domain.
# Originally Written by Andrew McCall - <andrew@textux.com>
# modified by Matt Biddulph - <matt@hackdiary.com> - to take screenshots

import os
import sys
import gtk
import gtk.gdk as gdk
import gtkmoz

class PyGtkMozExample:
    def __init__(self, URL = None, parent = None):        
        if parent == None:
            self.parent = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.parent.set_border_width(10)
        else:
            self.parent = parent
        
        # Initialize the widgets...
        self.widget = gtkmoz.MozEmbed()
        self.widget.set_size_request(816,600)
        
        # Connect signals
        self.widget.connect("net_stop", self.on_net_stop)
        self.widget.connect("progress", self.on_progress)

        self.parent.add(self.widget)

        if URL != None:
            self.widget.load_url(URL)
        
        self.parent.show_all()
        self.countdown = 3

    def on_progress(self, data, cur, max):
        print cur,"bytes loaded"
    def on_net_stop(self, data = None):
        gtk.timeout_add(1000,self.do_countdown,self)
        print "Taking screenshot in 3...",
        sys.stdout.flush()

    def do_countdown(self, data = None):
        self.countdown -= 1
        if(self.countdown > 0):
            print str(self.countdown)+"...",
            sys.stdout.flush()
            gtk.timeout_add(1000,self.do_countdown,self)
            return True
        else:
            print
            self.screenshot()

    def screenshot(self, data = None):
        window = self.widget.window
        (x,y,width,height,depth) = window.get_geometry()

        width -= 16

        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,width,height)
        pixbuf.get_from_drawable(window,self.widget.get_colormap(),0,0,0,0,width,height)
        pixbuf = pixbuf.scale_simple(133, 100, gdk.INTERP_HYPER)
        pixbuf.save("screenshot-thumb.png","png")
        print "Wrote screenshot-thumb.png"
        gtk.main_quit()
        return True
        
def __windowExit(widget, data=None):
    gtk.main_quit()
    
if __name__ == "__main__":
    try:
        HomeDir = os.environ["HOME"]
    except KeyError:
        raise "No Home Directory, Don't Know What to Do"
        
    ProfileDir = HomeDir + "/.gtkmozembedexample/"
    print "Note: a mozilla profile has been created in : " + ProfileDir
    
    gtkmoz.gtk_moz_embed_set_profile_path(ProfileDir, "helpsys")

    window = PyGtkMozExample(URL=sys.argv[1])
    window.parent.connect("destroy", __windowExit)
    gtk.main()
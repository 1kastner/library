#!/usr/bin/python
# -*- coding: utf-8 -*-

import thread
import time
import webbrowser

import cherrypy_layer

def new_thread(*args):
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8080')

thread.start_new_thread(new_thread, (1,2))
cherrypy_layer.run()


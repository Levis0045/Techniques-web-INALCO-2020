#!/usr/bin/python3
# coding: utf-8 


from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module run API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.1"

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from front.app import ceptyDataFront as frontend
from cepty.api import ceptyDataApi as backend

# ------------------------------------------------------------------

application = DispatcherMiddleware(frontend, {
    '/api': backend
})

cepty_app = Flask(__name__)
cepty_app.wsgi_app = application

# ------------------------------------------------------------------

if __name__ == '__main__':
    from os import environ
    cepty_app.run(host='127.0.0.1', port=environ['PORT'], use_evalex=True,
                  use_reloader=True, use_debugger=True)
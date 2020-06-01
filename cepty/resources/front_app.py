#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module treats HTTP Methods for clients resource API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.0.1"

from flask import send_from_directory, Response
from flask_restful import Resource
from pathlib import Path


__all__ = ['FrontAppStaticResource', 'DocRestApiResource']

parent = Path(__file__).parent.parent

class DocRestApiResource(Resource):
    """ Cepty Rest API documentation 

    -> [GET] /doc
    """

    def get(self): 
        import codecs
        url = parent / 'doc' / 'home-v0.2.html'
        content = codecs.open(str(url), "r", "utf-8").read()
        resp = Response(content, status=200, headers={},
                    content_type='text/html; charset=utf-8')
        return resp


class FrontAppResource(Resource):
    """ Front end app

    -> [GET] /home
    """

    def get(self): 
        url = parent / 'front_end' / 'public'
        return send_from_directory(url, 'index.html')


class FrontAppStaticResource(Resource):
    """ Static files of front end App

    -> [GET] /<path:path>
    """

    def get(self, path): 
        url_doc = parent / 'doc'
        url_svelte = parent / 'front_end' / 'public'
        return send_from_directory(url_doc, path)
     



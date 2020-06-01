#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    ------------------------------------------
    
    This module treats HTTP Methods for data resource API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""


__version__ = "0.0.1"


from flask_restful import Resource
from datetime import datetime
from flask import request

from ..lib.actions_data import *
from ..lib.utils import token_required, output_json, get_resource_data


__all__ = ['ContribGetPostResource', 'ContribUpdateDeleteResource']


class ContribGetPostResource(Resource):
    method_decorators = [token_required]

    """ Get and create contribution(s)

    -> [GET]  /contibutions
    -> [POST] /contibutions
    """

    def get(self, client):
        database = read_all_data('resources')
        args = request.args
        results = database['contributions']['data']
        results = sorted(results, key=lambda k: k['user_name'])
        if 'sort_name' in args:
            name = args['sort_name']
            database = [v for v in results if v['user_name'].lower() == name.lower()]
            if len(database) >= 1:
                len_data = len(database)
                message = 'Successfully load all contributions'
                msg = {'data':database, 'message':message,'status':200,
                        'time_server': datetime.now().isoformat(),'total':len_data}
                return output_json(msg, code=200)
            else:
                msg = {'data':{},'message':'No contributions found','status':404,
                        'time_server': datetime.now().isoformat(),'total':0}
                return output_json(msg, code=404)        
        elif 'sort_value' in args:
            name = args['sort_value']
            database = [v for v in results if v['contrib_name'].find(name) != -1]
            if len(database) >= 1:
                len_data = len(database)
                message = 'Successfully load all contributions'
                msg = {'data':database, 'message':message,'status':200,
                        'time_server': datetime.now().isoformat(),'total':len_data}
                return output_json(msg, code=200)
            else:
                msg = {'data':{},'message':'No contributions found','status':404,
                        'time_server': datetime.now().isoformat(),'total':0}
                return output_json(msg, code=404)
        elif 'sort_type' in args:
            name = args['sort_type']
            results = sorted(results, key=lambda k: str(k[name]))
            msg = {'data':results,'message':'Successfully load all contributions',
                    'status':200,'time_server':datetime.now().isoformat(),'total':len(results)}
            return output_json(msg, code=200)
        else:
            message = 'Successfully load all contributions'
            len_data = len(database.keys())
            msg = {'data': results, 'message': message, 'status': 200,
                    'time_server': datetime.now().isoformat(), 'total': len_data}
            return output_json(msg, code=200)

    def post(self, client): 
        data = request.get_json()
        try:
            message = 'Successfully create new contibution'
            results = create_data_by_id('resources', data, True)
            msg = {'data': results[0], 'message': message, 'status': 201,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=201)
        except Exception as e:
            message = 'Something wrong with your request body'
            msg = {'data': None, 'message': str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)


class ContribUpdateDeleteResource(Resource):
    method_decorators = [token_required]

    """ Update and delete contribution

    -> [GET]    /contibutions/<contrib_id>
    -> [PUT]    /contibutions/<contrib_id>
    -> [DELETE] /contibutions/<contrib_id>
    """

    def get(self, client, contrib_id): 
        database = read_all_data('resources')
        try:
            resource = get_resource_data(database, contrib_id)       
            message = 'Successfully load a contibution'
            msg = {'data': resource, 'message':message, 'status':200,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            msg = {'data': None, 'message': str(e), 'status': 404,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=404)

    def put(self, client, contrib_id): 
        database = read_all_data('resources')
        resource = get_resource_data(database, contrib_id)  
        data = request.get_json()
        try:
            message = 'Successfully update contibution'
            results = update_data_by_id(contrib_id, 'resources', data, True)
            msg = {'data': results[0], 'message': message, 'status': 200,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            msg = {'data': None, 'message':str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)

    def delete(self, client, contrib_id): 
        database = read_all_data('resources')
        resource = get_resource_data(database, contrib_id)  
        try:
            message = 'Successfully delete contribution'
            results = delete_data_by_id(contrib_id, 'resources', True)
            msg = {'data':results[0], 'message': message, 'status': 200,
                   'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            message = 'Something wrong with your request body'
            msg = {'data': None, 'message': str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)
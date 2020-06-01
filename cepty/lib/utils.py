#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    ------------------------------------------
    
    This module manage utilities functions for API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.0.1"


from pathlib import Path
from flask import request, current_app, render_template, Response
import json
import shelve
from functools import wraps

# ------------------------------------------------------------------

# Get access to functions out of the module
__all__ = ['get_resource_data', 'get_client_data', 'exclude_resource_data',
            'exclude_client_data', 'load_api_data', 'dump_api_data',
            'check_form_values', 'token_required', 'output_json']

# ------------------------------------------------------------------

# Get path of data
PARENT = Path(__file__).parent.parent
RESOURCE_DATA = PARENT / 'data' / 'DONNEES_CLIENT.json'
USER_DATA = PARENT / 'data' / 'LISTE_COLLABORATEURS.json'
SHELVE_DATA = str(PARENT / 'data' / 'ceptydatabase.sheve.db')

# ------------------------------------------------------------------

def load_api_data(form):
    """ Read and load api data """
    if not Path(SHELVE_DATA).exists():
        contrib_fl = RESOURCE_DATA.open()
        client_fl  = USER_DATA.open()
        with shelve.open(SHELVE_DATA) as save:
            save['contributions'] = json.load(contrib_fl)
            save['clients'] = json.load(client_fl)
        contrib_fl.close()
        client_fl.close()

    if form == 'resources':
        with shelve.open(SHELVE_DATA) as save:
            return save['contributions'] 
    elif form == 'clients':
        with shelve.open(SHELVE_DATA) as save:
            return save['clients']
    else: raise Exception('Invalid form type: contributions or clients')

def dump_api_data(form, data, dump_json=False):
    """ Read and dump api data """
    save_version = ''
    if form == 'resources':
        with shelve.open(SHELVE_DATA) as save:
            save_version = save['contributions'] 
            save['contributions'] = data
            if dump_json:
                try:
                    with RESOURCE_DATA.open('w', encoding='utf8') as t:
                        json.dump(data, t, indent=4)   
                except: 
                    with RESOURCE_DATA.open('w', encoding='utf8') as t:
                        json.dump(save_version, t, indent=4)                
    elif form == 'clients':
        with shelve.open(SHELVE_DATA) as save:
            save_version = save['clients'] 
            save['clients'] = data
            if dump_json:
                try:
                    with USER_DATA.open('w', encoding='utf8') as t: 
                        json.dump(data, t, indent=4)   
                except Exception as e:
                    print(str(e)) 
                    with USER_DATA.open('w', encoding='utf8') as t:
                        json.dump(save_version, t, indent=4) 

    else: raise Exception('Invalid form type: contributions or clients')
       
def get_resource_data(database, id_data):
    """ Get resource data by id """
    data_database = database['contributions']['data']
    crt_data = [x for x in data_database if x['public_id'] == id_data]
    if len(crt_data) == 0: raise Exception("Not contribution found with this id")
    crt_data = crt_data[0]
    return crt_data

def exclude_resource_data(database, id_data):
    """ Exclude resource data by id """
    data_database = database['contributions']['data']
    crt_data = [x for x in data_database if x['public_id'] != id_data]
    return crt_data

def get_client_data(database, id_data):
    """ Get client data by id """
    crt_data = [{k:v} for k, v in database.items() if k == id_data]
    if len(crt_data) == 0: raise Exception("Not client found with this id")
    crt_data = crt_data[0]
    return crt_data

def exclude_client_data(database, id_data):
    """ Exclude client data by id """
    crt_data = [{k:v} for k, v in database.items() if k != id_data]
    return crt_data

def check_form_values(form):
    """ Check form value """
    form_values = ['resources', 'clients']
    if form not in form_values: 
        raise Exception('Not correct value found')

def output_json(data, header={}, code=200):
    head = {
            "project": "Techniques web - M2-TAL - INALCO",
            "contributor": "Elvis",
            "Api-Version": "4.2",
            "license": "Creative Common 2.0",
            "contact": "contact@ceptyconsultant.com",
            "Access-Control-Allow-Origin":"*"
        }
    headers = dict(head, **header)
    resp = Response(json.dumps(data), status=code, headers=headers,
                    content_type='application/json')
    return resp
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        import jwt
        from flask import jsonify
        token, current_user = None, ''
        messageToken = "Token is missing! Please Login with admin account to perform this action."
        msg = {'message': messageToken, 'status': 401, 'uri': '/login'}
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if not token: return output_json(msg, code=401)
            try:
                data = jwt.decode(token, 'SECRET_KEY_CEPTY_CONSULTANT', algorithms=['HS256'])
                database = load_api_data("clients")
                current_client = get_client_data(database, data['public_id'])
            except Exception as e:
                msg = {'message': 'Token signature has expired or not valid! Login again', 
                       'status': 401, 'uri': '/login'}
                return output_json(msg, code=401)
        else: return output_json(msg, code=401)
        return f(current_client, *args, **kwargs)
    return decorated
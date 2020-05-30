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

from flask import request
from flask_restful import Resource
from datetime import datetime, timedelta
from ..lib.actions_data import *
from ..lib.utils import token_required, output_json, get_client_data


__all__ = ['ClientsGetPostResource', 'ClientsUpdateDeleteResource',
            'ClientsLoginResource']



class ClientsLoginResource(Resource):
    """ Login, create password and get token

    -> [GET]  /login
    -> [POST] /login
    """

    def get(self): 
        import jwt
        database = read_all_data('clients')
        auth = request.authorization
        head = {'WWW-Authenticate':'Basic realm="Login required!"'}
        msg  = {"message": 'Could not verify this client! Try again !'}

        if not auth or not auth.username or not auth.password:
            return output_json(msg, code=401, header=head)
        username = str(auth.username).strip()
        crt_client = [v for k, v in database.items() if v['nom'] == username]
        timed = datetime.now().isoformat()
        if len(crt_client) == 0: 
            msg = {'message': 'Username no found', 'status': 401, 'total': 0,
                    'url': self.endpoint, 'time_server': timed}
            return output_json(msg, code=401, header=head)
        elif 'password' not in crt_client[0]: 
            msg = {'message': 'Password not set!', 'status': 401, 'total': 0,
                    'url': self.endpoint, 'time_server': timed}
            return output_json(msg, code=401, header=head)        
        elif crt_client[0]['password'] != auth.password: 
            msg = {'message': 'Incorrect password !', 'status': 401, 'total': 0,
                    'url': self.endpoint, 'time_server': timed}
            return output_json(msg, code=401, header=head)        

        current_date = datetime.utcnow()+timedelta(minutes=120)
        token = jwt.encode({'public_id':crt_client[0]['id'], 'exp':current_date},
                                'SECRET_KEY_CEPTY_CONSULTANT', algorithm='HS256')
        del crt_client[0]['password']
        msg = {'data': crt_client[0], 'message': 'Successful login', 
                'time_server': timed, 'total': 1, 'url': self.endpoint, 
                'token': token.decode('utf-8'), 'status': 200}
        return output_json(msg, code=206)
     
    def post(self):
        data = request.json
        database = read_all_data('clients')
        client_name = request.args['client_name']
        crt_client = [v for k, v in database.items() if v['nom'] == client_name]
        if len(crt_client) == 0: 
            msg = {'data': {}, 'message':'Client not found! Try again!','status':404,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=404)
        crt_client == crt_client[0]
        if 'password' not in crt_client[0]: 
            try:
                client_id = crt_client[0]['id']
                print(client_id, crt_client[0])
                crt_client[0]['password'] = data['password']
                results = update_data_by_id(client_id,'clients',crt_client[0],save=True)
                print(results, 'aaaaaaaaaaaaaaaaaaaaaaa')
                data = results[0]
                
                del data[client_id]['password']
                msg = {'data': data[client_id], 'message':'Password created!', 'status':201,
                        'time_server': datetime.now().isoformat(), 'total': 1}
                return output_json(msg, code=201)
            except Exception as e:
                msg = {'client': client_name, 'message': 'Something bad happens: %s'%str(e), 
                        'status': 400,'time_server': datetime.now().isoformat(), 'total': 0}
                return output_json(msg, code=400)
        else:
            del crt_client[0]['password']
            msg = {'data': crt_client[0], 'message': 'Password found! Login now', 'status': 409,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=409)


class ClientsGetPostResource(Resource):
    method_decorators = [token_required]

    """ Get and create client(s)

    -> [GET]  /clients
    -> [POST] /clients
    """

    def get(self, client): 
        database = read_all_data('clients')
        args = request.args
        if 'sort_name' in args:
            name = args['sort_name']
            database = {k:v for k, v in database.items() if v['nom'] == name}
            if len(database.keys) >= 1:
                len_data = len(database.keys())
                message = 'Successful load all clients'
                results = []
                for c in database.values(): 
                    if 'password' in c: del c['password']
                    results.append(c)
                msg = {'data': results, 'message': message, 'status': 200,
                        'time_server': datetime.now().isoformat(), 'total': len_data}
                return output_json(msg, code=200)
            else:
                msg = {'data': {}, 'message': 'No data found', 'status': 404,
                        'time_server': datetime.now().isoformat(), 'total': 0}
                return output_json(msg, code=404)
        else:
            message = 'Successfully load all clients'
            len_data = len(database.keys())
            results = []
            for c in database.values(): 
                if 'password' in c: del c['password']
                results.append(c)
            msg = {'data': results, 'message': message, 'status': 200,
                    'time_server': datetime.now().isoformat(), 'total': len_data}
            return output_json(msg, code=200)

    def post(self, client): 
        data = request.json
        try:
            message = 'Successfully create new client'
            results = create_data_by_id('clients', data, True)
            msg = {'data': results[0], 'message': message, 'status': 201,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=201)
        except Exception as e:
            msg = {'data': None, 'message': str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)


class ClientsUpdateDeleteResource(Resource):
    method_decorators = [token_required]

    """ Update and delete client

    -> [GET]    /clients/<client_id>
    -> [PUT]    /clients/<client_id>
    -> [DELETE] /clients/<client_id>
    """

    def get(self, client, client_id): 
        database = read_all_data('clients')
        try:
            client = get_client_data(database, client_id)       
            message = 'Successfully load a client'
            if 'password' in client[client_id]: del client[client_id]['password']
            msg = {'data': client[client_id], 'message':message, 'status':200,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            msg = {'data': None, 'message': str(e), 'status': 404,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=404)

    def put(self, client, client_id): 
        database = read_all_data('clients')
        client = get_client_data(database, client_id)  
        data = request.json
        try:
            message = 'Successfully update client'
            results = update_data_by_id(client_id, 'clients', data, True)
            msg = {'data': results[0], 'message': message, 'status': 200,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            msg = {'data': None, 'message': str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)

    def delete(self, client, client_id): 
        database = read_all_data('clients')
        client = get_client_data(database, client_id)  
        try:
            message = 'Successfully delete client'
            results = delete_data_by_id(client_id, 'clients', True)
            msg = {'data': results[0], 'message': message, 'status': 200,
                    'time_server': datetime.now().isoformat(), 'total': 1}
            return output_json(msg, code=200)
        except Exception as e:
            msg = {'data': None, 'message': str(e), 'status': 400,
                    'time_server': datetime.now().isoformat(), 'total': 0}
            return output_json(msg, code=400)
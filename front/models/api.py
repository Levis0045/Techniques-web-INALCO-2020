# coding: utf-8 


"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module run API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.1"


import requests
import json

# -----------------------------------------------------------------------

HOST_API = "http://127.0.0.1:5000/api/v0.2"
URL_LOGIN = HOST_API+"/login"
URL_CLIENT_GET = HOST_API+"/clients"
URL_CLIENT_POST = HOST_API+"/clients/create"
URL_CLIENT_GET_PUT_DELETE = HOST_API+"/clients/{client_id}"
URL_CONTRIB_GET_POST = HOST_API+"/contributions"
URL_CONTRIB_GET_PUT_DELETE = HOST_API+"/contributions/{contrib_id}"

# -----------------------------------------------------------------------

__all__ = ['login_api', 'get_contributions', 'create_contribution',
            'delete_contribution', 'update_contribution', 'get_clients',
            'create_client', 'delete_client', 'delete_client',
            'update_client']

# -----------------------------------------------------------------------

def login_api(client, passw):
    data = (client, passw)
    data_json = {'username': client, 'password': passw}
    resp_api = requests.get(URL_LOGIN, auth=data)
    resp_json = resp_api.json()
    if resp_json['message'] == 'Password not set!':
        params = {'client_name': client}
        resp_api = requests.post(URL_LOGIN, json=data_json, params=params)
        if resp_api.status_code == 201:
            resp_api = requests.get(URL_LOGIN, auth=data)
        return resp_api.status_code, resp_api.json()
    else: return resp_api.status_code, resp_json

def get_contributions(token, data={}):
    headers = {"x-access-token": token}
    params = {}
    if "sort_type" in data: params["sort_type"] = data["sort_type"]
    elif "sort_name" in data: params["sort_name"] = data["sort_name"]
    resp_api = requests.get(URL_CONTRIB_GET_POST, params=params,
                            headers=headers)
    return resp_api.status_code, resp_api.json()

def create_contribution(token, data):
    headers = {"x-access-token": token}
    resp_api = requests.post(URL_CONTRIB_GET_POST, json=data, 
                            headers=headers)
    return resp_api.status_code, resp_api.json()

def delete_contribution(token, contrib_id):
    headers = {"x-access-token": token}
    URL_CONTRIB = URL_CONTRIB_GET_PUT_DELETE.format(contrib_id=contrib_id)
    resp_api = requests.delete(URL_CONTRIB, headers=headers)
    return resp_api.status_code, resp_api.json()

def update_contribution(token, contrib_id, data):
    headers = {"x-access-token": token}
    URL_CONTRIB = URL_CONTRIB_GET_PUT_DELETE.format(contrib_id=contrib_id)
    resp_api = requests.put(URL_CONTRIB, json=data, headers=headers)
    return resp_api.status_code, resp_api.json()

def get_clients(token, data={}):
    headers = {"x-access-token": token}
    params = {}
    if "sort_type" in data: params["sort_type"] = data["sort_type"]
    elif "sort_name" in data: params["sort_name"] = data["sort_name"]
    resp_api = requests.get(URL_CLIENT_GET, headers=headers, params=params)
    return resp_api.status_code, resp_api.json()

def create_client(data):
    resp_api = requests.post(URL_CLIENT_POST, json=data)
    return resp_api.status_code, resp_api.json()

def delete_client(token, client_id):
    headers = {"x-access-token": token}
    URL_CLIENT = URL_CLIENT_GET_PUT_DELETE.format(client_id=client_id)
    resp_api = requests.delete(URL_CLIENT, headers=headers)
    return resp_api.status_code, resp_api.json()

def update_client(token, client_id, data):
    headers = {"x-access-token": token}
    URL_CLIENT = URL_CLIENT_GET_PUT_DELETE.format(client_id=client_id)
    resp_api = requests.put(URL_CLIENT, json=data, headers=headers)
    return resp_api.status_code, resp_api.json()
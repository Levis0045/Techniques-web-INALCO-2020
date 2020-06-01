#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module manage data for API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""


__version__ = "0.0.1"


from .utils import *

# ------------------------------------------------------------------

# Get access to functions out of the module
__all__ = ['update_data_by_id', 'delete_data_by_id',
            'create_data_by_id', 'read_all_data']
            
# ------------------------------------------------------------------


def read_all_data(form):
    """ Read all data """
    check_form_values(form)
    database = load_api_data(form)  
    return database

def create_data_by_id(form, data, save):
    """ Create new api data """
    check_form_values(form)
    database = load_api_data(form)  
    try: 
        if form == 'resources':
            from uuid import uuid4
            uuidstr = str(uuid4())
            main_keys = {"dico_id": str, "user_id": str ,"user_name": str, 
                "article_id": str, "contrib_type": str,"contrib_data": str, 
                "contrib_path": str,"contrib_name": str, "ntealan": bool, 
                "validate": bool, "last_update": str}
            for k, v in data.items():
                if k not in main_keys.keys(): 
                    raise Exception("data key (%s) not valid "%k)
                if type(v) != main_keys[k]: 
                    raise Exception("data value type (%s) not valid for (%s)" \
                                    %(type(v), main_keys[k]))
            crt_data = database['contributions']['data']
            data['public_id'] = uuidstr
            crt_data.append(data)
            database['contributions']['data'] = crt_data
            if save: dump_api_data(form, database)
            return data, database
        elif form == 'clients':
            import random
            main_keys = {"nom": str, "prenom": str, 
                "fonction": str, "mise_a_jour": str, "conge": int, 
                "actionnaire": bool, "actif": bool, "anciennete": int, 
                "missions": list, 'password': str}
            crt_client = [v for k, v in database.items() if v['nom'] == data['nom']]
            if len(crt_client) != 0: raise Exception("Client name already exist")
            for k, v in data.items():
                if k not in main_keys.keys(): 
                    raise Exception("data key (%s) not valid "%k)
                if type(v) != main_keys[k]: 
                    raise Exception("data value type (%s) not valid for (%s)" \
                                    %(type(v), main_keys[k]))
            uuidstr = 'CEPTY_'+str(random.sample(range(900), 4)[0])
            data['id'] = uuidstr
            database.update({uuidstr:data})
            if save: dump_api_data(form, database)
            return data, database            
    except Exception as e: raise e

def update_data_by_id(id, form, data, save):
    """ Update api data by its id"""
    from datetime import datetime
    check_form_values(form)
    database = load_api_data(form)  
    try: 
        if form == 'resources':
            crt_data = get_resource_data(database, id)
            for k, v in data.items():
                if k in crt_data.keys(): crt_data[k] = v
            crt_data['last_update'] = datetime.now().isoformat()
            ext_data = exclude_resource_data(database, id)
            ext_data.append(crt_data)
            database['contributions']['data'] = ext_data
            if save: dump_api_data(form, database)
            return crt_data, database
        if form == 'clients':
            crt_data = get_client_data(database, id)
            
            for k, v in data.items():
                if k in crt_data[id].keys(): crt_data[id][k] = v
                if k == 'password': crt_data[id][k] = v
            crt_data[id]['mise_a_jour'] = datetime.now().isoformat()
            ext_data = exclude_client_data(database, id)
            ext_data.append(crt_data)
            database = {v:w for x in ext_data for v, w in x.items()}
            if save: dump_api_data(form, database)
            return crt_data, database            
    except Exception as e: raise e

def delete_data_by_id(id, form, save=True):
    """ Delete api data by its id"""
    check_form_values(form)
    database = load_api_data(form)  
    try: 
        if form == 'resources':
            crt_data = get_resource_data(database, id)
            ext_data = exclude_resource_data(database, id)
            database['contributions']['data'] = ext_data
            if save: dump_api_data(form, database)
            return crt_data, database
        if form == 'clients':
            crt_data = get_client_data(database, id)
            ext_data = exclude_client_data(database, id)
            database = {v:w for x in ext_data for v, w in x.items()}
            if save: dump_api_data(form, database)
            return crt_data, database            
    except Exception as e: raise e


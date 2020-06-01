#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    ------------------------------------------
    
    This module test all functionalities of API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""


__version__ = "0.1"


import unittest
from pathlib import Path
from flask import Response
from flask_restful import Api
import json


class ActionsDataTestCase(unittest.TestCase):
    """ TestCase for actions_data module: operations on data """
    parent_folder = Path(__file__).parent / 'cepty' / 'data'
    RESOURCE_DATA = parent_folder / 'DONNEES_CLIENT.json'
    USER_DATA = parent_folder / 'LISTE_COLLABORATEURS.json'

    def test_lib_load_read_data(self):
        """Test load all API database """
        from cepty.lib import load_api_data
        with self.RESOURCE_DATA.open() as t: current_resource = json.load(t)
        with self.USER_DATA.open() as r: current_client = json.load(r)
        result_resource = load_api_data('resources')
        result_clients = load_api_data('clients')
        self.assertEqual(type(result_resource), dict)
        self.assertEqual(type(result_clients), dict)
        self.assertEqual(result_resource, current_resource)
        self.assertEqual(result_clients, current_client)        
    
    def test_lib_create_data_by_id(self):
        """Test create component of files database """
        from cepty.lib import create_data_by_id
        with self.RESOURCE_DATA.open() as t: current_resources = json.load(t)
        with self.USER_DATA.open() as r: current_clients = json.load(r)
        resr_id = '94ec363b-0537-4929-820e-b0559c57ab4d'
        resr_data = {
            "dico_id": "yb_fr_3031",
            "user_id": "5184066e-8d5d-4809-1faa-60e384473935",
            "user_name": "Toto",
            "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967",
            "contrib_type": "sound",
            "contrib_data": "a-_sound_1-2020-03-26T111407.675Z-.wav",
            "contrib_path": "https://ntealan.net/soundcontrib/",
            "contrib_name": "azing",
            "ntealan": False,
            "validate": False,
            "last_update": "2020-03-26 11:15:38.811000"
        }
        result_resr = create_data_by_id('resources', resr_data, False)
        self.assertEqual(type(result_resr), tuple)
        self.assertEqual(type(result_resr[0]), dict)
        self.assertEqual(type(result_resr[1]), dict)
        self.assertNotEqual(len(result_resr[1]['contributions']['data']), 
                            len(current_resources['contributions']['data']))

        usr_data = {
            "nom": "Jules",
            "prenom": "Teukeu",
            "fonction": "Directeur des enseignements",
            "anciennete": 3,
            "mise_a_jour": "2020-03-06 11:55:11.827000",
            "conge": 5,
            "actif": False,
            "actionnaire": True,
            "missions": ["Bruxelle", "Paris"]
        }
        result_usr = create_data_by_id('clients', usr_data, False)
        self.assertEqual(type(result_usr), tuple)
        self.assertEqual(type(result_usr[0]), dict)
        self.assertEqual(type(result_usr[1]), dict)
        self.assertNotEqual(len(result_usr[1]), len(current_clients))

    def test_lib_update_data_by_id(self):
        """Test update files database component by id """
        from cepty.lib import update_data_by_id
        with self.RESOURCE_DATA.open() as t: current_resource = json.load(t)
        with self.USER_DATA.open() as r: current_client = json.load(r)
        resr_id = '94ec363b-0537-4929-820e-b0559c57ab4d'
        resr_data = {'ntealan': False, 'last_update': '2020-03-26 11:15:38.811000'}
        result_resr = update_data_by_id(resr_id, 'resources', resr_data, False)
        self.assertEqual(type(result_resr), tuple)
        self.assertEqual(type(result_resr[0]), dict)
        self.assertEqual(type(result_resr[1]), dict)
        self.assertEqual(result_resr[0]['ntealan'], False)

        usr_id = 'CEPTY_001'
        usr_data = {'prenom': False, 'conge': 30}
        result_usr = update_data_by_id(usr_id, 'clients', usr_data, False)
        self.assertEqual(type(result_usr), tuple)
        self.assertEqual(type(result_usr[0]), dict)
        self.assertEqual(type(result_usr[1]), dict)
        self.assertEqual(result_usr[0][usr_id]['conge'], 30) 
    
    def test_lib_delete_data_by_id(self):
        """Test delete files database component by id """
        from cepty.lib import delete_data_by_id
        with self.RESOURCE_DATA.open() as t: current_resources = json.load(t)
        with self.USER_DATA.open() as r: current_clients = json.load(r)
        resr_id = '94ec363b-0537-4929-820e-b0559c57ab4d'
        result_resr = delete_data_by_id(resr_id, 'resources', False)
        self.assertEqual(type(result_resr), tuple)
        self.assertEqual(type(result_resr[0]), dict)
        self.assertEqual(type(result_resr[1]), dict)
        self.assertNotEqual(len(result_resr[1]['contributions']['data']), 
                            len(current_resources['contributions']['data']))

        usr_id = 'CEPTY_001'
        result_usr = delete_data_by_id(usr_id, 'clients', False)
        self.assertEqual(type(result_usr), tuple)
        self.assertEqual(type(result_usr[0]), dict)
        self.assertEqual(type(result_usr[1]), dict)
        self.assertNotEqual(len(result_usr[1]), len(current_clients))



class RestApiTestCase(unittest.TestCase):
    """ TestCase for REST API: HTTP methods on data """

    def test_api_get_data(self): pass

    def test_api_create_data(self): pass

    def test_api_update_data(self): pass

    def test_api_delete_data(self): pass



if __name__ == '__main__':
    unittest.main(verbosity=8)
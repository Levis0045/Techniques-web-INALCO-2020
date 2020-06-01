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

__version__ = "0.2"

from flask import Flask
from flask_restful import Api
from flask_cors    import CORS

from .resources import *

# -----------------------------------------------------------------------

ceptyDataApi = Flask(__name__)
ceptyDataApi.app_context().push()
CORS(ceptyDataApi, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
ceptyRestApi = Api(ceptyDataApi, catch_all_404s=True, prefix='/v%s'%__version__,
                    serve_challenge_on_401=True, default_mediatype='json')

# -----------------------------------------------------------------------

ceptyRestApi.add_resource(DocRestApiResource, '/', '/doc', '/home',
                            endpoint='home_page_api')                          
ceptyRestApi.add_resource(FrontAppStaticResource, '/<path:path>',
                            endpoint='static_files_api')                            
ceptyRestApi.add_resource(ClientsLoginResource, '/login', 
                            endpoint='clients_login_api')
ceptyRestApi.add_resource(ClientsPostResource, '/clients/create', 
                            endpoint='clients_gp_api_post')
ceptyRestApi.add_resource(ClientsGetResource, '/clients', 
                            endpoint='clients_gp_api_get')                            
ceptyRestApi.add_resource(ClientsUpdateDeleteResource, '/clients/<client_id>', 
                            endpoint='clients_ud_api')
ceptyRestApi.add_resource(ContribGetPostResource, '/contributions', 
                            endpoint='contrib_gp_api')
ceptyRestApi.add_resource(ContribUpdateDeleteResource, '/contributions/<contrib_id>', 
                            endpoint='contrib_ud_api')

# -----------------------------------------------------------------------
"""
Map([<Rule '/v0.2/contributions' (HEAD, POST, GET, OPTIONS) -> contrib_gp>,
 <Rule '/v0.2/clients' (HEAD, POST, GET, OPTIONS) -> clients_gp_api>,
 <Rule '/v0.2/login' (HEAD, POST, GET, OPTIONS) -> clients_login_api>,
 <Rule '/v0.2/home' (HEAD, GET, OPTIONS) -> home_page_api>,
 <Rule '/v0.2/doc' (HEAD, GET, OPTIONS) -> home_page_api>,
 <Rule '/v0.2/' (HEAD, GET, OPTIONS) -> home_page_api>,
 <Rule '/v0.2/contributions/<contrib_id>' (PUT, OPTIONS, HEAD, GET, DELETE) -> contrib_ud_api>,
 <Rule '/v0.2/clients/<client_id>' (PUT, OPTIONS, HEAD, GET, DELETE) -> clients_ud_api>,
 <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/v0.2/<path>' (HEAD, GET, OPTIONS) -> static_files_api>])
"""

__all__ = ['ceptyDataApi']
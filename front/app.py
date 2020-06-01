# coding: utf-8 


"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module run API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.1"

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS

# -----------------------------------------------------------------------

__all__ = ['ceptyDataFront']

# -----------------------------------------------------------------------

class Config():
    FLASK_APP = "run_front.py"
    #SERVER_NAME = "ceptyconsultant.localhost"
    SECRET_KEY = "ceptyconsultant_2020_access_KEY"

def create_cepty_app():
    ceptyDataFront = Flask(__name__, instance_relative_config=True)
    ceptyDataFront.config.from_object(Config)
    Bootstrap(ceptyDataFront)
    
    # existing code omitted
    from .resources import auth
    from .resources import contributions
    from .resources import clients
    
    ceptyDataFront.register_blueprint(auth.authcepty)
    ceptyDataFront.register_blueprint(contributions.contrib)
    ceptyDataFront.register_blueprint(clients.client)

    ceptyDataFront.add_url_rule('/', endpoint='contributions.index')

    return ceptyDataFront

# -----------------------------------------------------------------------

ceptyDataFront = create_cepty_app()
ceptyDataFront.app_context().push()
CORS(ceptyDataFront, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# -----------------------------------------------------------------------

"""
Map([<Rule '/authcepty/register' (HEAD, POST, OPTIONS, GET) -> authcepty.register>,
 <Rule '/authcepty/logout' (HEAD, OPTIONS, GET) -> authcepty.logout>,
 <Rule '/authcepty/login' (HEAD, POST, OPTIONS, GET) -> authcepty.login>,
 <Rule '/create' (HEAD, POST, OPTIONS, GET) -> contributions.create>,
 <Rule '/' (HEAD, OPTIONS, GET) -> contributions.index>,
 <Rule '/' (HEAD, OPTIONS, GET) -> index>,
 <Rule '/static/bootstrap/<filename>' (HEAD, OPTIONS, GET) -> bootstrap.static>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/<id>/update' (HEAD, POST, OPTIONS, GET) -> contributions.update>,
 <Rule '/<id>/delete' (POST, OPTIONS) -> contributions.delete>])
"""
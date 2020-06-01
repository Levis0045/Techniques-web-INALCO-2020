# coding: utf-8 


"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module run API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""

__version__ = "0.1"

# -----------------------------------------------------------------------

from flask import (
    Blueprint, flash, g, redirect, render_template,
    session, request, url_for
)
from werkzeug.exceptions import abort

from front.resources.auth import login_required
from front.models.api import get_clients, create_client
from front.models.api import delete_client, update_client

# -----------------------------------------------------------------------

client = Blueprint('clients', __name__, url_prefix='/clients')

# -----------------------------------------------------------------------

@client.route('/', methods=('GET', 'POST'))
@login_required
def index(token):
    session['contrib_zone'] = False
    api_resp = {}
    if request.method == 'GET':
        api_resp = get_clients(token)
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = get_clients(token, data=body_data)

    code_resp = api_resp[0]
    data_response = api_resp[1]
    try:
        session['client_zone'] = True
        return render_template('clients/index.html', 
                                clients=data_response['data'])
    except:
        session.clear()
        session['client_zone'] = False
        return redirect(url_for('authcepty.login'))

@client.route('/create', methods=['POST'])
@login_required
def create(token):
    data = dict(request.form)
    data['actionnaire'] = bool(data['actionnaire'])
    data['anciennete'] = int(data['anciennete'])
    data['conge'] = int(data['conge'])
    if 'actif' not in data: data['actif'] = False
    else: data['actif'] = bool(data['actif'])
    api_resp = create_client(data)
    code_resp = api_resp[0]
    data_response = api_resp[1]

    if code_resp != 201:
        flash("error: %s"%code_resp)
        return render_template('clients/index.html', api_error=True,
                                api_message=data_response['message'])
    else: return redirect(url_for('clients.index'))


@client.route('/<public_id>/update', methods=('GET', 'POST'))
@login_required
def update(token, public_id):
    session['contrib_zone'] = False
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = update_client(token,public_id,body_data)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp not in [200, 201]:
            flash("error")
            session['client_zone'] = True
            session['client_new'] = None
        else:
            session['client_zone'] = True
            session['client_new'] = body_data
            return redirect(url_for('clients.index'))

    return render_template('clients/index.html')


@client.route('/<public_id>/delete', methods=('POST',))
@login_required
def delete(token, public_id):
    session['contrib_zone'] = False
    api_resp = delete_client(token,public_id)
    code_resp = api_resp[0]
    data_response = api_resp[1]

    if code_resp not in [200, 201]:
        flash("error")
        session['client_zone'] = True
        session['client_new'] = None
    else:
        session['client_zone'] = True
        return redirect(url_for('clients.index'))

    return render_template('clients/index.html')
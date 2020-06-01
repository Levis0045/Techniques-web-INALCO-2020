# coding: utf-8 


"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    -------------------------------------------
    
    This module run API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.

    credit: https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
"""

__version__ = "0.1"

# -----------------------------------------------------------------------

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from front.models.api import login_api, create_client

# -----------------------------------------------------------------------

authcepty = Blueprint('authcepty', __name__, url_prefix='/authcepty')

# -----------------------------------------------------------------------

@authcepty.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = dict(request.form)
        api_resp = create_client(data)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp != 201 :
            flash("error: %s"%code_resp)
            render_template('authcepty/register.html', api_error=True,
                            api_message=data_response['message'])
        else:
            return redirect(url_for('authcepty.login'), api_error=False)

    return render_template('authcepty/register.html')

@authcepty.before_app_request
def load_logged_in_user():
    client_id = session.get('client_id')
    if client_id is None:
        g.client = None
    else: g.client = client_id

@authcepty.route('/login', methods=('GET', 'POST'))
def login():
    data_response = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        api_resp = login_api(username, password)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp in [200, 201]:
            session.clear()
            session['user_id'] = data_response['data']['id']
            session['token'] = data_response['token']
            session['client'] = data_response['data']
            g.client = data_response['data']
            return redirect(url_for('contributions.index'))
        else:
            message_login = data_response['message']
            return render_template('authcepty/login.html', api_error=True, 
                                    api_message=message_login)

    elif request.method == 'GET':
        return render_template('authcepty/login.html', api_error=False)
    else: flash(error)

@authcepty.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authcepty.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'client' not in session:
            session.clear()
            return redirect(url_for('authcepty.login'))
        return view(session['token'], **kwargs)

    return wrapped_view
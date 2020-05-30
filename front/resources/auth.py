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

from front.models.api import login_api, create_clients

# -----------------------------------------------------------------------

authcepty = Blueprint('authcepty', __name__, url_prefix='/authcepty')

# -----------------------------------------------------------------------

@authcepty.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = ''
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db  is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            return redirect(url_for('authcepty.login'))

        flash(error)

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
        print(api_resp)

        if code_resp in [200, 201]:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            message_login = data_response['message']
            print('ffffffffffffffffffffff')
            return render_template('authcepty/login.html', login_access=False, 
                                    message_login = message_login)

    elif request.method == 'GET':
        print('rrrrrrrrrrrrrrrrrrrrrrrrrrr')
        return render_template('authcepty/login.html', login_access=True)
    else: flash(error)


@authcepty.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.client is None:
            return redirect(url_for('authcepty.login'))
        return view(g.token, **kwargs)

    return wrapped_view
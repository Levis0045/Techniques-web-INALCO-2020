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

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    session
)
from werkzeug.exceptions import abort

from front.resources.auth import login_required
from front.models.api import get_contributions, create_contribution
from front.models.api import delete_contribution, update_contribution 

# -----------------------------------------------------------------------

contrib = Blueprint('contributions', __name__, url_prefix='/contributions')

# -----------------------------------------------------------------------

@contrib.route('/', methods=('GET', 'POST'))
@login_required
def index(token):
    session['client_zone'] = False
    api_resp = {}
    if request.method == 'GET':
        api_resp = get_contributions(token)
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = get_contributions(token, data=body_data)

    code_resp = api_resp[0]
    data_response = api_resp[1]
    try:
        session['contrib_zone'] = True
        return render_template('contributions/index.html', 
                                contributions=data_response['data'])
    except:
        session.clear()
        session['contrib_zone'] = False
        return redirect(url_for('authcepty.login'))


@contrib.route('/create', methods=('GET', 'POST'))
@login_required
def create(token):
    session['contrib_new'] = None
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = create_contribution(token, body_data)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp != 201:
            flash("error")
            session['contrib_zone'] = True
            session['contrib_new'] = None
            return redirect(url_for('contributions.index'))
        else:           
            session['contrib_zone'] = True
            session['contrib_new'] = body_data
            return redirect(url_for('contributions.index'))

    session['contrib_zone'] = True
    return render_template('contributions/index.html')


@contrib.route('/<public_id>/update', methods=('GET', 'POST'))
@login_required
def update(token, public_id):
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = update_contribution(token, public_id, body_data)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp not in [200, 201]:
            flash("error")
        else:
            session['contrib_zone'] = True
            return redirect(url_for('contributions.index'))

    session['contrib_zone'] = True
    return redirect(url_for('contributions.index'))


@contrib.route('/<public_id>/delete', methods=('POST',))
@login_required
def delete(token, public_id):
    if request.method == 'POST':
        body_data = dict(request.form)
        api_resp = delete_contribution(token, public_id)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp not in [200, 201]:
            flash("error")
        else:
            session['contrib_zone'] = True
            return redirect(url_for('contributions.index'))

    session['contrib_zone'] = True
    return redirect(url_for('contributions.index'))
    
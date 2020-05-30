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
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from front.resources.auth import login_required
from front.models.api import get_clients, create_clients
from front.models.api import delete_clients, update_clients

# -----------------------------------------------------------------------

client = Blueprint('clients', __name__)

# -----------------------------------------------------------------------


@client.route('/')
def index():
    contributions_data = get_clients()
    return render_template('clients/index.html', posts=contributions_data)


@client.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = create_clients()
           
            return redirect(url_for('blog.index'))

    return render_template('clients/create.html')


@client.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = "get_post(id)"

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
           
            return redirect(url_for('blog.index'))

    return render_template('clients/update.html', post=post)


@client.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    return redirect(url_for('clients.index'))
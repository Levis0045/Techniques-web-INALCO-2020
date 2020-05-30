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
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from front.resources.auth import login_required
from front.models.api import get_contribution, create_contribution
from front.models.api import delete_contribution, update_contribution 

# -----------------------------------------------------------------------

contrib = Blueprint('contributions', __name__)

# -----------------------------------------------------------------------


@contrib.route('/')
@login_required
def index(token):
    contributions_data = get_contribution('token')
    return render_template('contributions/index.html', posts=contributions_data)


@contrib.route('/create', methods=('GET', 'POST'))
@login_required
def create(token):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = create_contribution()
           
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@contrib.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(token, id):
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

    return render_template('blog/update.html', post=post)


@contrib.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(token, id):
    return redirect(url_for('blog.index'))
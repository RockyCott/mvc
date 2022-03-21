
import flask
from app.forms import LoginForm, RegisterForm, CommunityForm, PostForm, searchForm
from . import comms as co
from flask import Flask, request, make_response, redirect, render_template, session, url_for, current_app, abort, flash
from flask.helpers import send_from_directory
from models import User, Community, Post, Comment, get_user, user_by_id
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db_service import db
from app.file_handling import allowed_file, validate_image
from uuid import uuid4
import os
from nudenet import NudeClassifierLite


###
### functions for files, community and posts management
###

def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)

def get_communities():
    community_list = Community.query.all()
    return community_list

###
### routes for community blueprint, list of communities, searching and add communities
###
@co.route('/explore')
def comms():
    community_list = get_communities()
    user = current_user
    search_form = searchForm()
    return render_template('communities.html', current_user=user, community_list=community_list, search_form=search_form)

@co.route('/add', methods=['GET', 'POST'])
@login_required
def addCommunity():
    community_form = CommunityForm()
    user = current_user
    if community_form.validate_on_submit():
        name = community_form.community_name.data
        description = community_form.description.data
        fb = community_form.facebook.data
        discord = community_form.discord.data
        pic = community_form.picture.data
        filename = secure_filename(pic.filename)
        
        if pic and allowed_file(filename):
            file_ext = os.path.splitext(filename)[1]
            if file_ext != validate_image(pic.stream):
                flash('Please upload an image file', 'info')
                return redirect(url_for('communities.addCommunity'))

            pic_name = uuid4().hex
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
            pic.save(path)
            pic_classifier = NudeClassifierLite()                  # this is a NSFW filter implementation to avoid users from posting NSFW images as community pictures.
            if pic_classifier.classify(path)[path]['safe'] > 0.50:     # check the image and the 'safe' parameter returned, it has to be over 50% safe to accept the image
                new_community = Community(name=name, description=description, facebook=fb, discord=discord,
                                        picture=pic_name, id_creator=current_user.id)

                db.session.add(new_community)
                db.session.commit()
                flash('The community has ben added, gg!')
                return redirect(url_for('communities.comms'))
            else:
                os.remove(path)
                flash('Try to upload a different image')
                return redirect(url_for('communities.addCommunity'))
        flash('Make sure you upload an image file', 'info')
    return render_template('newCommunity.html', community_form=community_form, current_user=user)

@co.route('/search')
def searchCommunity():
    query = request.args.get('query')
    user = current_user
    search_form = searchForm()
    community_list = Community.query.filter(Community.name.ilike(f'%{query}%')).all()
    return render_template('communities.html', current_user=user, community_list=community_list, search_form=search_form)


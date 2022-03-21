from operator import pos
import flask
from app.forms import LoginForm, RegisterForm, CommunityForm, PostForm, searchForm, UpdatePostForm, UpdateCommunityForm
from . import community as community
from flask import Flask, request, make_response, redirect, render_template, session, url_for, current_app, abort, flash
from flask.helpers import send_from_directory
from models import User, Community, Post, Comment, get_user, user_by_id
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.file_handling import allowed_file, validate_image
from db_service import db
from uuid import uuid4
import os
from nudenet import NudeClassifierLite

def get_community(id):
    return Community.query.get_or_404(id)

def community_posts(community_id):
    posts = Post.query.filter_by(community_id = community_id)
    return posts

def updatePost(post_id, content):
    post = Post.query.get_or_404(post_id)
    if post.postAuthor != current_user:  # doing this check in case that users try to change the post id value
        abort(403)                       # in the hidden input of the form to update a post that is not made by them.
    post.content = content
    db.session.commit()

def updateCommunity(id, description, facebook, discord, image=None):
    community = Community.query.get_or_404(id)
    if community.creator != current_user:  # this is the same check as in the updatePost function
        abort(403)
    if image is not None:    # if image.filename != ''
        community.picture = secure_filename(image)  # secure_filename(image.filename)
    community.description = description
    community.facebook = facebook
    community.discord = discord
    db.session.commit()
    
    return redirect(url_for('community.displayCommunity', id=id))

def scan_image(path):              # in case a community picture is updated, this will use the NSFW classifier
    res = False                     # to scan the new image
    #name = secure_filename(image.filename)
    #path = os.path.join(current_app.config['UPLOAD_FOLDER'], name).replace("\\","/")
    #image.save(path)
    classifier = NudeClassifierLite()
    if classifier.classify(path)[path]['safe'] > 0.50:
        res = True
    else:
        os.remove(path)

    return res

@community.route('/<uuid:id>/', methods=['GET', 'POST'])
@community.route('/<uuid:id>', methods=['GET', 'POST'])
def displayCommunity(id):
    community = get_community(id)

    if community:
        creator = user_by_id(community.id_creator)
        posts_list = community_posts(community.id)
        pic = os.path.join('/static/community_pic', community.picture).replace("\\","/")

        post = PostForm()                                      # form for adding a new post
        if post.post.data and post.validate_on_submit():       # user must be logged in to create a new post
            if current_user.is_authenticated:
                new_post = Post(title=post.title.data, content=post.content.data, id_author=current_user.id, community_id=community.id)
                db.session.add(new_post)
                db.session.commit()
            else:
                flash('You have to be logged in to create posts!')
            
            return redirect(url_for('community.displayCommunity', id=id))

        update_post = UpdatePostForm()                        # form for updating a post, this form is inside the post options modal
        if update_post.send.data and update_post.validate_on_submit():  
            if current_user.is_authenticated:
                updatePost(post_id=update_post.idPost.data, content=update_post.content.data)
                flash('Your post has been updated', 'info')
                return redirect(url_for('community.displayCommunity', id=id))

        update_community = UpdateCommunityForm()
        if update_community.update.data and update_community.validate_on_submit():
            description = update_community.description.data
            facebook = update_community.facebook.data
            discord = update_community.discord.data
            image = update_community.image.data
            filename = secure_filename(image.filename)
            pic_name = None
            if filename != '' and allowed_file(filename): 
                file_ext = os.path.splitext(filename)[1]
                if file_ext != validate_image(image.stream):
                    flash('Please upload an image file', 'info')
                    return redirect(url_for('community.displayCommunity', id=id))

                pic_name = uuid4().hex
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
                image.save(path)                                                    # if the uploaded image is classified as safe, the actual community image is removed
                if scan_image(path):                                                # the scan_image function has already stored the new image in the same path as the actual image.
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], community.picture).replace("\\","/"))
                else:
                    flash('Please try to upload a different image', 'warning')
                    return redirect(url_for('community.displayCommunity', id=id))

            updateCommunity(id, description, facebook, discord, pic_name)
            flash('The community page has ben updated, gg!', 'info')
            return redirect(url_for('community.displayCommunity', id=id))

        return render_template('community.html', community=community, creator=creator, pic=pic, posts_list=posts_list, post_form=post,
                             update_post=update_post, update_community=update_community)
    else:
        return abort(404)

@community.route('/<uuid:id>/post/<uuid:post_id>/delete', methods=['POST'])
def deletePost(id, post_id):
    post = Post.query.get_or_404(post_id)
    if post.postAuthor != current_user:   # in case a user tries to access this route to delete a post from another user
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('community.displayCommunity', id=id))

@community.route('<uuid:id>/post/<uuid:post_id>', methods=['GET', 'POST'])
def showPost(id, post_id):
    community = Community.query.get_or_404(id)
    creator = user_by_id(community.id_creator)
    creator_info = {'id': creator.id, 'username': creator.username}
    pic = os.path.join('/static/community_pic', community.picture).replace("\\","/")
    post = Post.query.get_or_404(post_id)

    update_post = UpdatePostForm()      # form for updating a post, this form is inside the post options modal
    if update_post.validate_on_submit():  
        if current_user.is_authenticated:
            updatePost(update_post.idPost.data, update_post.content.data)
            return redirect(url_for('community.showPost', id=id, post_id=post_id))

    return render_template('post.html', community=community, post=post, update_post=update_post, pic=pic, creator_info=creator_info)



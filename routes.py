from app import app, db
from flask import render_template, request, redirect, url_for, Blueprint, jsonify, session
from models import User, Post, Notification, Comment, Protocol
#from sqlalchemy import and_, or_
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy import desc, asc
from language_select import t, av_languages
from datacommunication import event, note_event, write_protocol, create_notification

import random
from datetime import timedelta
bp = Blueprint('likes', __name__)
app.permanent_session_lifetime = timedelta(days=30)

# user roles
admin = 5
account_moderator = 4
content_moderator = 3
overseer = 2
regular_user = 1
suspended_user = 0


# language functionality
@app.context_processor
def inject_translator():
    lang = getattr(current_user, 'app_lang', 'eng')
    return dict(t=lambda key: t(key, lang))



##########################################
# for development ONLY ###################
##########################################
# clear everything from database #########
##########################################
@app.route('/clear-all')
def clear_all():
    db.drop_all()
    db.create_all()
    return redirect(url_for('login'))




# routes
##############
### routes ###
##############
##################################################################################################################################################################################
###### over primary main pages ###################################################################################################################################################
##################################################################################################################################################################################
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    posts = Post.query.order_by(Post.timestamp).all()
    posts.reverse()
    return render_template('index.html', posts=posts)

@app.route('/following')
def sec_home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    posts = Post.query.order_by(Post.timestamp).all()
    posts.reverse()
    return render_template('sec-index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    if request.method == 'POST':
        ID = 'P-' + str(random.randint(100000, 999999))
        content = request.form.get('post-content').strip()
        user_id = current_user.id
        post = Post(id=ID, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/#{ID}')
    return render_template('main/create.html')

@app.route('/user/<username>', methods=['POST', 'GET'])
def user(username):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    this_user = User.query.filter_by(username=username).first()
    if current_user in this_user.blocked_users:
        message = "There's nothing here"
        return render_template('error/error.html', message=message)
    this_user_posts = Post.query.filter_by(user_id=this_user.id).order_by(Post.timestamp).all()
    this_user_posts.reverse()
    return render_template('user/user.html', user=this_user, posts=this_user_posts)

@app.route('/edit-profile-data/<id>', methods=['GET', 'POST']) # changing username event id: CXXNK
def edit_profile_data(id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    this_user = User.query.filter_by(id=id).first()
    if this_user != current_user and not current_user.role >= account_moderator:
        message = "You can't edit someone else's profile!"
        return render_template('error/error.html', message=message)
    if request.method == 'POST':
        fullname = request.form.get('fullname').strip()
        username = request.form.get('username').strip()
        role = ''
        if current_user.role >= account_moderator and this_user != current_user:
            role = int(request.form.get('role').strip())
        if not username.startswith('@'):
            message = "Username has to start with '@'!"
            return render_template('user/edit-profile-data.html', user=this_user, message=message)
        if '"' in username or '/' in username or '(' in username or ')' in username or '[' in username or ']' in username:
            message = "Username contains invalid characters!"
            return render_template('user/edit-profile-data.html', user=this_user, message=message)
        pronouns = request.form.get('pronouns').strip()
        if (' ' in pronouns or '/' not in pronouns) and not pronouns == '':
            message = "Pronouns have to be separated by '/'!"
            return render_template('user/edit-profile-data.html', user=this_user, message=message)
        # write protocol
        event_id = 'CXXNK'
        change_username_protocol = write_protocol(this_user, event_id)
        db.session.add(change_username_protocol)
        db.session.commit()
        # end protocol
        email = request.form.get('email').strip()
        bio = request.form.get('bio').strip()
        this_user.fullname = fullname
        this_user.username = username
        this_user.pronouns = pronouns
        this_user.email = email
        this_user.bio = bio
        if role != '':
            this_user.role = role
        db.session.commit()
        return redirect(url_for('user', username=this_user.username))
    return render_template('user/edit-profile-data.html', user=this_user)

# over secondary main pages
@app.route('/search', methods=['GET', 'POST'])
def search():
    users = ''
    searchterm = ''
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        searchterm = '@' + request.form.get('searchterm').strip()
        users = User.query.filter(User.username.startswith(searchterm)).all()
    return render_template('main/search.html', users=users, searchterm=searchterm)

@app.route('/notifications')
def notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    my_notifications = Notification.query.filter_by(receiving_user_id=current_user.id).all()
    my_notifications.reverse()
    return render_template('main/notifications.html', note_event=note_event, notifications=my_notifications)

@app.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('user/settings.html')

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################














##################################################################################################################################################################################
###### authentication pages ######################################################################################################################################################
##################################################################################################################################################################################
@app.route('/register', methods=['GET', 'POST']) # register event id: RXXLK
def register():
    all_users = User.query.all()
    message = None
    if request.method == 'POST':
        ID = 'U-' + str(random.randint(100000, 999999))
        fullname = request.form.get('fullname').strip()
        username = request.form.get('username').strip()
        if '@' in username:
            username.replace('@', '')
        username = '@' + username
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        repeat_password = request.form.get('repeat-password').strip()
        for user in all_users:
            if user.username == username:
                return render_template('user/register.html', message='username already exists', fullname=fullname, email=email)
        if password == repeat_password:
            if username == '@worldlyemo':
                this_user = User(id=ID, fullname=fullname, username=username, email=email, password=password, role=admin)
            else:
                this_user = User(id=ID, fullname=fullname, username=username, email=email, password=password)
            print(f"Created User {username}!")
            db.session.add(this_user)
            db.session.commit()
            # write protocol
            event_id = 'RXXLK'
            register_protocol = write_protocol(this_user, event_id)
            db.session.add(register_protocol)
            db.session.commit()
            # end protocol
            log_user = User.query.filter_by(id=ID).first()
            login_user(log_user)
            # create cookie
            session.permanent = True
            session['user_id'] = this_user.id
            # write protocol
            event_id = 'LXXOK'
            login_protocol = write_protocol(log_user, event_id)
            db.session.add(login_protocol)
            db.session.commit()
            # end protocol
            return redirect(url_for('home'))
        else:
            message = 'Passwords have to match!'
            print("Passwords have to match!")
            return render_template('user/register.html', message=message, fullname=fullname, username=username, email=email)
    return render_template('user/register.html')

@app.route('/login', methods=['GET', 'POST']) # login event id: LXXOK
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if username.startswith('@'):
            username = username.replace('@', '')
        username = '@' + username
        this_user = User.query.filter_by(username=username).first()
        if this_user and this_user.password == password:
            login_user(this_user)
            # create cookie with login info
            session.permanent = True
            session['user_id'] = this_user.id
            # write protocol
            event_id = 'LXXOK'
            login_protocol = write_protocol(this_user, event_id)
            db.session.add(login_protocol)
            db.session.commit()
            # end protocol
            print(f"logged in {username}!")
            return redirect(url_for('home'))
        else:
            message = 'Check your entries!'
            print("Something went wrong! Check your entries")
            return render_template('user/login.html', message=message)
    return render_template('user/login.html')

@app.route('/logout') # logout event id: LXXIK
@login_required
def logout():
    # write protocol
    event_id = 'LXXIK'
    logout_protocol = write_protocol(current_user, event_id)
    db.session.add(logout_protocol)
    db.session.commit()
    # end protocol
    print(f"Logged out {current_user.username}")
    session.clear()
    logout_user()
    return redirect(url_for('home'))

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################



















##################################################################################################################################################################################
###### the post pages ############################################################################################################################################################
##################################################################################################################################################################################
@app.route('/post/<id>', methods=['GET', 'POST']) # add a comment to the post. (Not to a comment)
def post(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    this_post = Post.query.filter_by(id=id).first()
    if current_user in this_post.author.blocked_users:
        message = "There's nothing here!"
        return render_template('error/error.html', message=message)
    comments = Comment.query.filter_by(original_post_id=this_post.id).all()
    comments.reverse()
    if request.method == 'POST':
        if current_user.role == suspended_user:
            message = "Your account is suspended"
            return render_template('error/error.html', message=message)
        ID = 'C-' + str(random.randint(100000, 999999))
        content = request.form.get('comment-content').strip()
        user_id = current_user.id
        original_post_id = this_post.id
        # parent_id remains empty because Post object is the parent
        comment = Comment(id=ID, content=content, user_id=user_id, original_post_id=original_post_id)
        db.session.add(comment)
        db.session.commit()
        # write a notification for target user
        if current_user != this_post.author:
            note = create_notification(this_post.author, current_user, 'CYYTR', post_id=this_post.id, comment_id=ID)
            db.session.add(note)
            db.session.commit()
        return redirect(url_for('post', id=this_post.id))
    return render_template('post/post.html', post=this_post, comments=comments)


@app.route('/delete-comment/<id>')
@login_required
def delete_comment(id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    comment = Comment.query.filter_by(id=id).first()
    author = comment.author
    if author != current_user:
        message = "You can't delete someone else's comments!"
        return render_template('error/error.html', message=message)
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################






















##################################################################################################################################################################################
###### post functions ############################################################################################################################################################
##################################################################################################################################################################################
@app.route('/delete-post/<id>')
@login_required
def delete_post(id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    post = Post.query.filter_by(id=id).first()
    author = post.author
    if author != current_user and current_user.role < content_moderator:
        message = "You can't delete someone else's posts!"
        return render_template('error/error.html', message=message)
    author.likes_total -= post.like_count
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))


@bp.route('/api/like', methods=['POST']) # like event id: LYYTR   # like posts
@login_required
def toggle_like():
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    data = request.get_json()
    post_id = data.get('post_id')
    user = current_user

    if not post_id or not user.is_authenticated:
        return jsonify({"error": "Invalid request"}), 400

    post = Post.query.filter_by(id=post_id).first()
    author = User.query.filter_by(id=post.user_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    if post in user.liked_posts:
        user.liked_posts.remove(post)
        if post.like_count > 0:
            post.like_count -= 1
        if author.likes_total > 0:
            author.likes_total -= 1
        db.session.commit()
        return jsonify({"message": "Unliked", "liked": False, "like_count": post.liked_by.count()})
    else:
        user.liked_posts.append(post)
        post.like_count += 1
        author.likes_total += 1
        # create notification if author != current_user
        if author != current_user:
            note = create_notification(author, current_user, 'LYYTR')
            db.session.add(note)
            db.session.commit()
        # end notification
        db.session.commit()
        return jsonify({"message": "Liked", "liked": True, "like_count": post.liked_by.count()})
    
app.register_blueprint(bp)



@app.route('/follow/<user_id>', methods=['GET', 'POST']) # follow event id: FYYTR
@login_required
def follow(user_id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    target_user = User.query.filter_by(id=user_id).first()
    if target_user not in current_user.following:
        current_user.following.append(target_user)
        db.session.commit()
        print(f"{current_user.username} is now following {target_user.username}")
        # write notification
        note = create_notification(target_user, current_user, 'FYYTR')
        db.session.add(note)
        db.session.commit()
        # end notification
        return redirect(url_for('user', username=target_user.username))
    else:
        print(f"{current_user.username} already follows {target_user.username}! Please revise")
        return redirect(request.referrer)
    
@app.route('/unfollow/<user_id>', methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    target_user = User.query.filter_by(id=user_id).first()
    if target_user in current_user.following:
        current_user.following.remove(target_user)
        db.session.commit()
        print(f"{current_user.username} is not following {target_user.username} anymore")
    else:
        print(f"{current_user.username} already unfollowed {target_user.username}! Please revise")
        return redirect(url_for('user', username=target_user.username))
    return redirect(request.referrer)


@app.route('/block-user/<id>')
@login_required
def block_user(id):
    if current_user.role == suspended_user:
        message = "Your account is suspended"
        return render_template('error/error.html', message=message)
    user = User.query.filter_by(id=id).first()
    if user in current_user.blocked_users:
        current_user.blocked_users.remove(user)
    else:
        if user.role <= 2:
            current_user.blocked_users.append(user)
            if current_user in user.followed_by:
                user.followed_by.remove(current_user)
            if user in current_user.followed_by:
                current_user.followed_by.remove(user)
    db.session.commit()
    return redirect(url_for('user', username=user.username))
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################

















##################################################################################################################################################################################
###### handling settings #########################################################################################################################################################
##################################################################################################################################################################################
@app.route('/change_language/<lang>')
@login_required
def change_language(lang):
    current_user.app_lang = lang
    # check if language exists
    if lang not in av_languages:
        message = 'The selected language does not exist!'
        return render_template('user/settings.html', message=message)
    db.session.commit()
    return redirect(url_for('settings'))
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################

















##################################################################################################################################################################################
###### Protocol Stream and User Management System ################# suspend and delete Account ###################################################################################
##################################################################################################################################################################################
@app.route('/protocol-stream')
def protocol_stream():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role <= account_moderator:
        message = "You don't have the necessary permissions to do that!"
        return render_template('error/error.html', message=message)
    protocols = Protocol.query.all()
    protocols.reverse()
    return render_template('admin/protocol-stream.html', protocols=protocols, event=event)



@app.route('/ums')
def ums():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role <= overseer:
        message = "You don't have the necessary permissions to do that!"
        return render_template('error/error.html', message=message)
    users = User.query.all()
    return render_template('admin/ums.html', users=users)



@app.route('/code-page-tyni')
def code_page_tyni():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role < overseer:
        message = "You don't have the necessary permissions to do that!"
        return render_template('error/error.html', message=message)
    return render_template('admin/code-page.html')



@app.route('/suspend-user/<id>')
def suspend_user(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not (current_user.role <= account_moderator or current_user.role != overseer):
        message = "You don't have the necessary permissions to do that!"
        return render_template('error/error.html', message=message)
    user = User.query.filter_by(id=id).first()
    if user.role >= current_user.role:
        message = "You can't operate on users with higher permission level"
        return render_template('error/error.html', message=message)
    if user.role != 0:
        user.role = 0
        db.session.commit()
        # write a note
        note = create_notification(user, current_user, 'SYYTR')
        db.session.add(note)
        db.session.commit()
    else:
        user.role = 1
        db.session.commit()
        # write a note
        note = create_notification(user, current_user, 'SYYUR')
        db.session.add(note)
        db.session.commit()
    return redirect(url_for('user', username=user.username))
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################


















##################################################################################################################################################################################
###### error handling ############################################################################################################################################################
##################################################################################################################################################################################
@app.route('/error')
def error():
    return render_template('error/error.html')
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
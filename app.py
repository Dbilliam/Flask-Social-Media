from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager
from forms import UserForm, PostForm, LoginForm, RepostForm
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from sqlalchemy.sql import func 
from datetime import timedelta




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SECRET_KEY'] = "memydark"

db=SQLAlchemy()

migrate=Migrate(app, db)

db.init_app(app)

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    comments = db.relationship(
        'Comment', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='posts', lazy=True, passive_deletes=True)
    star = db.relationship('Star', cascade='all, delete, delete-orphan',
                            backref='posts', lazy=True, passive_deletes=True)
    repost = db.relationship('Repost', cascade='all, delete, delete-orphan',
                            backref='posts',lazy=True,passive_deletes=True)                           


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    name = db.Column(db.String(20), nullable=True)
    work = db.Column(db.String(20), nullable=True)
    education = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(50), nullable=True)
    language = db.Column(db.String(), nullable=True)
    interests = db.Column(db.String(), nullable=True)
    url = db.Column(db.String(), nullable=True)
    profile_picture = db.Column(db.String(), nullable=True)
    cover_picture = db.Column(db.String(), nullable=True)
    about_info = db.Column(db.Text(120), nullable=True)
    password_hash = db.Column(db.String(128))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Posts', cascade='all, delete, delete-orphan',
                            backref='users', lazy=True, passive_deletes=True)
    comments = db.relationship('Comment', cascade='all, delete, delete-orphan', 
                            backref='user', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='users', lazy=True, passive_deletes=True)
    star = db.relationship('Star', cascade='all, delete, delete-orphan',
                            backref='users', lazy=True, passive_deletes=True)
    repost = db.relationship('Repost', cascade='all, delete, delete-orphan',
                             backref='users',lazy=True,passive_deletes=True)                                                
    
    # Create aString
    def __repr__(self):
        return '<Name %r>' % self.name

    #hash property
    @property
    def password(self):
        raise AttributeError('password is not a readable attibute!')
    # set-up the password 
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)   
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(380), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)


class Repost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)

with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'registration'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
                                                    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    author = current_user.id
    if form.validate_on_submit():
        post = Posts(content=form.content.data, author=author)
        form.content.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Post Submitted Successfully!")
        our_users = Users.query.order_by(Users.date)
        posts = Posts.query.order_by(Posts.date)
        return render_template('index.html', posts=posts,author=author, user=current_user, form=form, our_users=our_users)
    our_users = Users.query.order_by(Users.date)     
    posts = Posts.query.order_by(Posts.date)    
    return render_template("index.html", posts=posts,author=author, user=current_user, form=form , our_users=our_users)



@app.route('/registration', methods=['GET','POST'])
def registration():
    form = LoginForm()
    name = None
    form = UserForm()
    if request.method == "POST":
        email = request.form["email"]
        user = Users.query.filter_by(email=email).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, request.form["password"]):
                login_user(user)
                flash("Login Succesfull!!!")
                return redirect(url_for('index'))
            else:
                flash("Wrong Password - Try Again!") 
        else:
            flash("That User Doesn't Exist! Try Again....") 
            
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        username = request.form['username']
        password_hash = request.form['password_hash']
        user = Users.query.filter_by(email=email).first()
        if user is None:
            hashed_pw = generate_password_hash(password_hash, "sha256")
            user = Users(email=email, username=username, name=name, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        form.username.data = ''
        form.email.data = ''
        form.name.data = ''
        form.password_hash = ''
        flash("User Added Successfully!")
    # our_users = Users.query.limit(3).all()
    # our_users = Users.query.order_by(Users.date_added)
    return render_template("registration.html" ,name=name, form=form)  
    
@app.route('/signout', methods=['GET','POST'])
@login_required
def signout():
    logout_user()
    flash("You have been logged out! Thanks You")
    return redirect(url_for('registration'))

@app.route('/profile', methods=['GET','POST']) 
@login_required
def profile():
    our_users = Users.query.order_by(Users.date)
    return render_template("profile.html", our_users=our_users)   

# @app.route('/registration', methods=['GET','POST'])
# def registration():
#     form = LoginForm()
#     name = None
#     form1 = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user:
#             # Check the hash
#             if check_password_hash(user.password_hash, form.password.data):
#                 login_user(user)
#                 flash("Login Succesfull!!!")
#                 return redirect(url_for('index'))
#             else:
#                 flash("Wrong Password - Try Again!") 
#         else:
#             flash("That User Doesn't Exist! Try Again....") 
            
#     if form1.validate_on_submit():
#         user = Users.query.filter_by(email=form1.username.data).first()
#         if user is None:
#             hashed_pw = generate_password_hash(form1.password_hash.data, "sha256")
#             user = Users(email=form1.email.data, username=form1.username.data, name=form1.name.data, password_hash=hashed_pw)
#             db.session.add(user)
#             db.session.commit()
#         name = form1.name.data 
#         form1.username.data = ''
#         form1.email.data = ''
#         form1.name.data = ''
#         form1.password_hash = ''
#         flash("User Added Successfully!")
#     # our_users = Users.query.limit(3).all()
#     # our_users = Users.query.order_by(Users.date_added)
#     return render_template("registraion.html" ,name=name, form1=form1, form=form)                 


# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user:
#             # Check the hash
#             if check_password_hash(user.password_hash, form.password.data):
#                 login_user(user)
#                 flash("Login Succesfull!!!")
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("Wrong Password - Try Again!") 
#         else:
#             flash("That User Doesn't Exist! Try Again....")           
#     return render_template('login.html',form=form)


# @app.route('/signup', methods=['GET','POST'])
# def signup():
#     name = None
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.username.data).first()
#         if user is None:
#             hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
#             user = Users(username=form.username.data, name=form.name.data, password_hash=hashed_pw)
#             db.session.add(user)
#             db.session.commit()
#         name = form.name.data 
#         form.username.data = ''
#         form.name.data = ''
#         form.password_hash = ''
#         flash("User Added Successfully!")
#     # our_users = Users.query.limit(3).all()
#     # our_users = Users.query.order_by(Users.date_added)
#     return render_template("signup.html" ,name = name, form=form)


# @app.route('/logout', methods=['GET','POST'])
# @login_required
# def logout():
#     logout_user()
#     flash("You Have Been Logged Out! Thanks ")
#     return redirect(url_for('login'))


# @app.route('/profile/<username>', methods=['GET', 'POST'])
# @login_required
# def profile(username):
#     user = Users.query.filter_by(username=username).first()
#     if not user:
#         flash('Hey! that user does not exist', category='error')
#     users_posts = user.posts
#     correct_time = timedelta(hours=4)
#     username = user.username
#     return render_template('profile.html', user=current_user, users_posts=users_posts,
#                            correct_time=correct_time, username=username)



# @app.route('/posts/edit/<int:id>', methods=['GET','POST'])
# @login_required
# def edit_post(id):
#     post = Posts.query.get_or_404(id)
#     form= PostForm()
#     if form.validate_on_submit():
#         post.content = form.content.data
#         # Update database
#         db.session.add(post)
#         db.session.commit()
#         flash("Post Has Been Updated!")
#         return redirect(url_for('blogs',id=post.id))
#     if current_user.id == post.poster_id or current_user.id == 1:    
#         form.content.data = post.content
#         return render_template('edit_post.html', form=form)   
#     else:
#         flash("You Aren't Authorized to Edit This Post...")
#         posts = Posts.query.order_by(Posts.date_posted)
#         return render_template("blog.html", posts=posts)

# @app.route('/post/delete/<int:id>')
# @login_required
# def delete_post(id):
#     post_to_delete = Posts.query.get_or_404(id)
#     id= current_user.id
#     if id == post_to_delete.poster.id or id == 1:
#         try:
#             db.session.delete(post_to_delete)
#             db.session.commit()
#             flash("Blog Post Was Deleted!")
#             posts = Posts.query.order_by(Posts.date_posted)
#             return render_template("blog.html", posts=posts)    
#         except:
#             flash("Whoops! There was a problem deleting post, try again...")
#             posts = Posts.query.order_by(Posts.date_posted)
#             return render_template("blog.html", posts=posts)    
#     else:
#         flash("You Aren't Authorized to Delete That Post!")   
#         posts = Posts.query.order_by(Posts.date_posted)
#         return render_template("blog.html", posts=posts) 



# Update Database Record
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    if id == current_user.id or current_user.id == 1:
        name_to_update = Users.query.get_or_404(id)
        if request.method == "POST":
            name_to_update.name = request.form["name"]
            name_to_update.username = request.form["username"]
            name_to_update.email = request.form["email"]
            name_to_update.location = request.form["location"]
            name_to_update.phone = request.form["phone"]
            name_to_update.about_info = request.form["about_info"]
            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template("update.html", form=form, name_to_update=name_to_update)
            except:
                flash("Error! Looks like there was a problem try again")
                return render_template("update.html", form=form, name_to_update=name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update,  id=id)
    else:
        flash("Sorry, You can't delete that user! ")
        return redirect(url_for('profile'))        



@app.route('/userinterests/<int:id>', methods=['GET','POST'])
@login_required
def userinterests(id):
    form = UserForm()
    if id == current_user.id or current_user.id == 1:
        name_to_update = Users.query.get_or_404(id)
        if request.method == "POST":
            # name_to_update.interests = request.form("interests")
            name_to_update = request.form.getlist('interests')
            for interests in name_to_update:
                # name_to_update = Users(interests=interests)
                try:
                    # db.seesion.add(name_to_update)
                    db.session.commit()
                    flash("User Interest Updated Successfully!")
                    return render_template("interest.html", form=form, name_to_update=name_to_update, id=id)
                except:
                    flash("Error! Looks like there was a problem try again")
                    return render_template("profile.html", form=form, name_to_update=name_to_update, id=id )
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("interest.html", form=form, name_to_update=name_to_update,  id=id)
    else:
        flash("Sorry, You can't delete that user! ")
        return redirect(url_for('profile'))     

# @app.route('/user_update/<int:id>', methods=['GET','POST'])
# @login_required
# def update(id):
#     form = UserForm()
#     id = current_user.id or current_user.id == 1
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == "POST":
#         name_to_update.name = request.form["name"]
#         name_to_update.username = request.form["username"]
#         name_to_update.email = request.form["email"]
#         name_to_update.location = request.form["location"]
#         name_to_update.phone = request.form["Phone"]
#         name_to_update.about_info = request.form["about_info"]
#         # if request.files['cover_picture']:
#         #     name_to_update.cover_picture = request.files["cover_picture"]
#         #     pic_filename = secure_filename(name_to_update.cover_picture.filename)
#         #     pic_name = str(uuid.uuid1()) + "_" + pic_filename
#         #     saver = request.files['cover_picture']
#         #     name_to_update.cover_picture = pic_name
#         #     try:
#         #         db.session.commit()
#         #         saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
#         #         flash("User Cover Picture Updated Successfully!")
#         #         return render_template("profile.html")
#         #     except:
#         #         flash("Error! Looks like there was a problem try again") 
#         #         return render_template("update.html", form=form, name_to_update=name_to_update)      
#         if request.files['profile_picture']:
#             name_to_update.profile_picture = request.files["profile_picture"]
#             pic_filename = secure_filename(name_to_update.profile_picture.filename)
#             pic_name = str(uuid.uuid1()) + "_" + pic_filename
#             saver = request.files['profile_picture']
#             name_to_update.profile_picture = pic_name 
#             try:
#                 db.session.commit()
#                 saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
#                 flash("User Profile Picture Updated Successfully!")
#                 return render_template("profile.html", form=form, name_to_update=name_to_update)
#             except:
#                 flash("Error! Looks like there was a problem try again")
#                 return render_template("update.html", form=form, name_to_update=name_to_update)
#         else:
#             db.session.commit()
#             flash("User Updated Successfully!")
#             return render_template("profile.html", form=form, name_to_update=name_to_update)
#     else:
#         return render_template("update.html", form=form, name_to_update=name_to_update, id=id)


# @app.route('/user_delete/<int:id>', methods=['GET','POST'])
# @login_required
# def delete(id):
#     if id  == current_user.id or current_user.id == 1:
#         user_to_delete = Users.query.get_or_404(id)
#         name = None
#         form = UserForm()
#         try:
#             db.session.delete(user_to_delete)
#             db.session.commit()
#             flash("User Deleted Successfully")
#             our_users = Users.query.order_by(Users.date_added)
#             return render_template("signup.html", name=name, form=form, our_users=our_users)
#         except:
#             flash("Whoops! There was a problem deleting user try again.....")    
#             return render_template("signup.html", name=name, form=form, our_users=our_users)
#     else:
#         flash("Sorry, You can't delete that user! ")
#         return redirect(url_for('dashboard'))


# @app.route('/repost/<post_id>', methods=['GET','POST'])
# @login_required
# def repost(post_id):
#     post = Posts.query.get_or_404(id)
#     form= RepostForm()
#     if form.validate_on_submit():
#         post.content = form.content.data
#     else:
#         post = Posts.query.filter_by(id=post_id).first()
#         if post:
#             new_repost = Repost(form=form,author=current_user.id, post_id=post_id)
#             db.session.add(new_repost)
#             db.session.commit()
#             flash('Successfully posted comment!', category='success')
#             return render_template("index.html", form=form, post_id=post_id)





@app.route('/add-comment/<post_id>', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
    if request.method == 'POST':
        comment = request.form.get('comment')
        if not comment:
            return jsonify({'error': 'No comment to add'}, 400)
        else:
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                new_comment = Comment(text=comment,
                                      author=current_user.id, post_id=post_id)
                db.session.add(new_comment)
                db.session.commit()
                flash('Successfully posted comment!', category='success')

            else:
                flash('No post available', category='error')
    post = Posts.query.filter_by(id=post_id).first()
    postId = post.id
    return jsonify({'success': 'facts', 'postId': postId})


@app.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return jsonify({'error': 'Comment doesn\'t exist'}, 400)
        # flash('Comment doesn\'t exist', category='error')

    elif current_user.id != comment.user.id and current_user.id != comment.post.author:
        flash('You are not authorized to delete this post', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment successfully deleted', category='success')
    postId = comment.post_id
    post = Posts.query.filter_by(id=postId).first()
    print(postId)
    return jsonify({'success': 'facts',
                    'postId': postId,
                    'commentLen': len(post.comments)})


@app.route('/like-post/<post_id>', methods=['GET', 'POST'])
@login_required
def like_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes': len(post.likes),
                    'liked': current_user.id in map(lambda n: n.author, post.likes)})















    
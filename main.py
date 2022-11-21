from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask_login import (
    LoginManager,
    logout_user,
    login_required,
    current_user,
    login_user,
)
from app import create_app
from app.forms import LoginForm, PostForm, CommentForm
from app.db import db

from app.models.usuarios import AnonymousUser, User
from app.models.posts import Post
from app.models.roles import Role
from app.utils.utils import Permission
from app.utils.decorator import admin_required, permission_required, permission_required_rest
import json
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = create_app()
login = LoginManager(app)
login.login_view = "login.login_p"
login.anonymous_user = AnonymousUser

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    print(user.email)
    g.current_user = user
    print(g.current_user)
    return user.check_password(password)

@app.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "Para administradores!"


@app.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para moderadores!"


@app.route("/insert")
def insert():
    u = User(username="linder2", email="linder02@gmail.com")
    u.set_password("linder340")

    role = Role(name="User", users=[u])
    role.add_permission(Permission.WRITE)

    db.session.add(u)
    db.session.commit()

    return "Insertado"


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    post_form = PostForm()

    if current_user.can(Permission.WRITE) and post_form.validate_on_submit():

        new_post = Post(body=post_form.body.data, author=current_user._get_current_object())
        db.session.add(new_post)
        db.session.commit()
        print(request.headers)
        return redirect(url_for("index.index"))

    return render_template("post.html", post_form=post_form)

@app.route('/postJson/', methods=['POST'])
@auth.login_required
@permission_required_rest(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('post_detail', id=post.id)}



@app.route("/post/<id>")
def post_detail(id):
    comment_form = CommentForm()
    
    post = Post.query.filter_by(id=id).first()

    context = {
        "comment_form": comment_form,
        "post": post
    }

    return render_template("post-detail.html", **context)


@app.route("/profile")
def profile():
    posts_by_current_user = Post.query.filter_by(user_id=current_user.id).count()
    # posts_by_user = User.query.filter_by(id=current_user.id).first()
    # print(posts_by_user.posts)
    return render_template("profile.html", post_count=posts_by_current_user)


db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()

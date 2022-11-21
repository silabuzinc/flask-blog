from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import (
    LoginManager,
    logout_user,
    login_required,
    current_user,
    login_user,
)
from app.models.usuarios import AnonymousUser, User
from werkzeug.urls import url_parse

login_page = Blueprint('login', __name__)


@login_page.route("/login", methods=["GET", "POST"])
def login_p():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login.no_existe"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        print(type(next_page))
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@login_page.route("/no-existe")
def no_existe():
    return render_template("nouser.html")
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from flask_app import db
from flask_app.forms import SignUpForm, LoginForm
from flask_app.models import User

main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# メインの地図のページ
@main.route("/")
# @login_required # 開発時には面倒だからコメントアウトしておく
def maps():
    return render_template("maps.html")

# サインアップページ
@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("main.signup"))

        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)

    return render_template("signup.html", form=form)

# ログインページ
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.users"))
        
        flash("メールアドレスかパスワードが不正です")
    return render_template("login.html", form=form)

# ログアウトする時に用いる
@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# ユーザ一覧 開発用
@main.route("/users")
@login_required
def users():
    users = db.session.query(User).all()
    return render_template("users.html", users=users)

# ユーザ情報編集
@main.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = SignUpForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for("main.users"))
    return render_template("edit_user.html", user=user, form=form)

# ユーザ削除
@main.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("main.users"))

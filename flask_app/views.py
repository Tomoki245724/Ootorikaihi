from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_app import db, auth
from flask_app.forms import SignUpForm, LoginForm, CreateGenreForm, CreateSiteForm, PostCommentForm
from flask_app.models import User, Genre, Sitedata, Comment, Picture

main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# メインの地図のページ
@main.route("/")
@login_required
@auth.login_required
def maps():
    genres = Genre.query.all()
    Users = User.query.all()
    return render_template("maps.html", genres=genres)

@main.route("/data")
@auth.login_required
def get_data():
    sites = Sitedata.query.all()
    data = []
    for site in sites:
        category_id = site.category
        data.append({
            "siteid": site.siteid,
            "sitename": site.sitename,
            "coordinates": site.coordinates,
            "categoryid": category_id,
            "categoryname": Genre.query.filter_by(genid=category_id).one().genname,
        })
    json_data = jsonify(data)
    return json_data

@main.route("/data/<int:site_id>")
@auth.login_required
def get_sitedata(site_id):
    site = Sitedata.query.filter_by(siteid=site_id).first()
    category_id = site.category
    data = [{
        "siteid": site.siteid,
        "sitename": site.sitename,
        "coordinates": site.coordinates,
        "categoryid": category_id,
        "categoryname": Genre.query.filter_by(genid=category_id).one().genname,
    }]
    json_data = jsonify(data)
    return json_data

@main.route("/genres_data")
@auth.login_required
def get_genre_data():
    genres = Genre.query.all()
    data = []
    for genre in genres:
        data.append({
            "genid": genre.genid,
            "genname": genre.genname,
        })
    json_data = jsonify(data)
    return json_data

# サインアップページ
@main.route("/signup", methods=["GET", "POST"])
@auth.login_required
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
            next_ = url_for("main.maps")
        return redirect(next_)

    return render_template("signup.html", form=form)

# ログインページ
@main.route("/login", methods=["GET", "POST"])
@auth.login_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.maps"))
        
        flash("メールアドレスかパスワードが不正です")
    return render_template("login.html", form=form)

# ログアウトする時に用いる
@main.route("/logout")
@auth.login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# ユーザ一覧 開発用
@main.route("/users")
@login_required
@auth.login_required
def users():
    users = db.session.query(User).all()
    return render_template("users.html", users=users)

# ユーザ情報編集
@main.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
@auth.login_required
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
@main.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@auth.login_required
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("main.users"))

# ジャンル一覧 開発用？
@main.route("/genres")
@login_required
@auth.login_required
def genres():
    genres = db.session.query(Genre).all()
    return render_template("genre/genres.html", genres=genres)

# ジャンル作成ページ
@main.route("/create_genre", methods=["GET", "POST"])
@login_required
@auth.login_required
def create_genre():
    form = CreateGenreForm()
    if form.validate_on_submit():
        genre = Genre(
            genname=form.genname.data,
            caption=form.caption.data,
            pins=0,
            creator=current_user.get_id()
        )
        db.session.add(genre)
        db.session.commit()

        return redirect(url_for("main.genres"))

    return render_template("genre/create_genre.html", form=form)

# ジャンル情報
@main.route("/genre/<int:genre_id>", methods=["GET"])
@login_required
@auth.login_required
def genre_info(genre_id):
    genre = Genre.query.filter_by(genid=genre_id).first()
    sites = Sitedata.query.filter_by(category=genre_id).all()
    creator = User.query.filter_by(id=genre.creator).first()
    return render_template("genre/genre_info.html", genre=genre, sites=sites, creator=creator)

# ジャンル情報（開発用）
@main.route("/genre/dev", methods=["GET"])
@auth.login_required
def dev_genre_info():
    return render_template("genre/dev_genre_info.html")

# ジャンル情報編集
@main.route("/edit_genre/<int:genre_id>", methods=["GET", "POST"])
@login_required
@auth.login_required
def edit_genre(genre_id):
    form = CreateGenreForm()
    genre = Genre.query.filter_by(genid=genre_id).first()
    current = int(current_user.get_id())
    if form.validate_on_submit():
        genre.genname = form.genname.data
        db.session.commit()
        return redirect(url_for("main.genres"))
    return render_template("genre/edit_genre.html", genre=genre, form=form, current=current)

# ジャンル削除
@main.route("/genre/<int:genre_id>/delete", methods=["POST"])
@login_required
@auth.login_required
def delete_genre(genre_id):
    genre = db.session.query(Genre).filter_by(genid=genre_id).first()
    sites = db.session.query(Sitedata).filter_by(category=genre_id).all()
    db.session.delete(genre)
    for site in sites:
        db.session.delete(site)
    db.session.commit()
    return redirect(url_for("main.genres"))

# サイト作成ページ
@main.route("/create_site/<int:genre_id>", methods=["GET", "POST"])
@login_required
@auth.login_required
def create_site(genre_id):
    genre = db.session.query(Genre).filter_by(genid=genre_id).first()
    form = CreateSiteForm()
    if form.validate_on_submit():
        site = Sitedata(
            sitename=form.sitename.data,
            category=genre_id,
            content=form.content.data,
            coordinates=str(form.latitude.data) + "," + str(form.longitude.data),
            creator=current_user.get_id()
        )
        genre.pins += 1
        db.session.add(site)
        db.session.commit()

        return redirect(url_for("main.genre_info", genre_id=genre.genid))

    return render_template("site/create_site.html", genre=genre, form=form)

# サイト情報
@main.route("/site/<int:site_id>", methods=["GET"])
@login_required
@auth.login_required
def site_info(site_id):
    site = Sitedata.query.filter_by(siteid=site_id).first()
    genre = Genre.query.filter_by(genid=site.category).first()
    creator = User.query.filter_by(id=genre.creator).first()
    comments = Comment.query.filter_by(siteid=site_id).all()
    posters = User.query.all()
    form = PostCommentForm()
    return render_template("site/site_info.html",  site=site, genre=genre, creator=creator, comments=comments, form=form)

# サイト情報編集
@main.route("/edit_site/<int:site_id>", methods=["GET", "POST"])
@login_required
@auth.login_required
def edit_site(site_id):
    form = CreateSiteForm()
    site = Sitedata.query.filter_by(siteid=site_id).first()
    genre = Genre.query.filter_by(genid=site.category).first()
    current = int(current_user.get_id())
    if form.validate_on_submit():
        site.sitename = form.sitename.data
        site.content = form.content.data
        site.coordinates = str(form.latitude.data) + "," + str(form.longitude.data)
        db.session.commit()
        return redirect(url_for("main.site_info", site_id=site_id))
    return render_template("site/edit_site.html", form=form, genre=genre, site=site, current=current)

# サイト削除
@main.route("/site/<int:site_id>/delete", methods=["POST"])
@login_required
@auth.login_required
def delete_site(site_id):
    site = db.session.query(Sitedata).filter_by(siteid=site_id).first()
    genre = db.session.query(Genre).filter_by(genid=site.category).first()
    db.session.delete(site)
    genre.pins += -1
    db.session.commit()
    return redirect(url_for("main.genre_info", genre_id=site.category))

# コメント投稿
@main.route("/site/<int:site_id>/comment", methods=["POST"])
@login_required
@auth.login_required
def post_comment(site_id):
    site = Sitedata.query.filter_by(siteid=site_id).first()
    genre = Genre.query.filter_by(genid=site.category).first()
    creator = User.query.filter_by(id=genre.creator).first()
    comments = Comment.query.filter_by(siteid=site_id).all()
    user = User.query.filter_by(id=current_user.get_id()).first()
    form = PostCommentForm()
    if form.validate_on_submit():
        comment = Comment(
            poster=user.username,
            siteid=site_id,
            content=form.comment.data
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("main.site_info", site_id=site.siteid))

    return render_template("site/site_info.html",  site=site, genre=genre, creator=creator, comments=comments)

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")]
    )
    submit = SubmitField("新規登録")

class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")]
    )
    submit = SubmitField("ログイン")

class CreateGenreForm(FlaskForm):
    genname = StringField(
        "ジャンル名",
        validators=[DataRequired("ジャンル名は必須です。")],
    )
    caption = StringField("説明")
    submit = SubmitField("新規登録")

class CreateSiteForm(FlaskForm):
    sitename = StringField(
        "サイト名",
        validators=[DataRequired("サイト名は必須です。")],
    )
    content = TextAreaField(
        "概要",
    )
    # coordinates = StringField("座標")
    latitude = FloatField("緯度")
    longitude = FloatField("経度")
    image = FileField(
        "写真",
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], '画像ファイル（JPG、JPEG、PNG）のみアップロード可能です。')
        ]
    )
    submit = SubmitField("新規登録")


class PostCommentForm(FlaskForm):
    comment = StringField(
        "新規コメント",
        validators=[DataRequired("テキストは必須です。")],
    )
    submit = SubmitField("投稿")
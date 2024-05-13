from flask import Blueprint, render_template, redirect, url_for
# from apps.app import db

maps = Blueprint(
    "maps",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@maps.route("/")
def canvas():
    return render_template("maps/canvas.html")

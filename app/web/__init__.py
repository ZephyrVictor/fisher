# encoding=utf-8
__author__ = 'Zephyr369'
from flask import Blueprint,render_template
from flask_mail import Mail
mail = Mail()

web = Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_fount(e):
    return render_template('404.html'),404
from app.web import book
from app.web import auth

from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
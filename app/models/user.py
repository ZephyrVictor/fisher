# encoding=utf-8
__author__ = 'Zephyr369'
from flask import current_app
from flask_login import UserMixin
from app import login_manager
# from app.libs.enums import PendingStatus
from math import floor

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.helper import is_isbn_or_key
from app.models.base import db, Base
# from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
# from app.models.wish import Wish
from app.spider.ocean import Ocean
class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    status = db.Column(db.String(10))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return check_password_hash(self._password, raw)

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True
    # def get_id(self):
    #     return self.id

    # def can_send_drift(self):
    #     if self.beans < 1:
    #         return False
    #     if self.send_counter > 3:
    #         success_gifts_count = Gift.query.filter_by(
    #             uid=self.id, launched=True).count()
    #         success_receive_count = Drift.query.filter_by(
    #             requester_id=self.id, pending=PendingStatus.Success).count()
    #         if floor(success_receive_count / 2) <= floor(success_gifts_count):
    #             return True
    #         else:
    #             return False

    def can_save_to_list(self, isbn):
        # isbn,鱼书,礼物清单，心愿
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = Ocean()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送者和索要者

        # 既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, launched=False,
                                       isbn=isbn).first()
        wishing = Wish.query.filter_by(uid=self.id, launched=False,
                                       isbn=isbn).first()
        if not gifting and not wishing:
            return True
        else:
            return False

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
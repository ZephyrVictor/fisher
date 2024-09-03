# encoding=utf-8
__author__ = 'Zephyr369'
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func, and_
from sqlalchemy.orm import relationship
from app.models.base import db, Base
from app.spider.ocean import Ocean


# from collections import namedtuple
# EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_count(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn，到Wish表中计算出某个礼物的wish心愿数量
        # filter()接收条件表达式
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        ocean = Ocean()
        ocean.search_by_isbn(self.isbn)
        return ocean.first

    # 对象代表一个礼物
    # 类代表礼物这个事物
    @classmethod
    def recent(cls):
        from sqlalchemy import desc, func

        # Subquery
        sub_query = db.session.query(
            Gift.isbn,
            func.max(Gift.create_time).label('max_create_time')
        ).filter_by(launched=False, status=1).group_by(Gift.isbn).subquery()

        # Main query using the subquery
        recent_gift = db.session.query(Gift).join(
            sub_query, and_(
                Gift.isbn == sub_query.c.isbn,
                Gift.create_time == sub_query.c.max_create_time
            )
        ).order_by(desc(sub_query.c.max_create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).all()

        return recent_gift


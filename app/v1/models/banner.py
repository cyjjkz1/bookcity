#!/usr/bin/env python
# -*- coding:utf8 -*-

from app import db
from datetime import datetime


class Banner(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(10), nullable=False, unique=True)
    validate = db.Column(db.Integer, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __init__(self, title, validate, book_id, create_time=datetime.now()):
        self.title = title
        self.validate = validate
        self.book_id = book_id
        self.create_time = create_time

    def __str__(self):
        return '<Banner: {} {} {} {}>'.format(self.title, self.validate, self.book_id, self.create_time)

    def model_to_dict(self):
        banner_dict = {
            'id': self.id,
            'title': self.title,
            'validate': self.validate,
            'book_id': self.book_id,
            'create_time': self.create_time
        }
        return banner_dict

    def save(self):
        db.session.add(self)
        db.session.commit()
#!/usr/bin/en python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class Image(db.Model):
    __talbename__ = 'image'
    """
    书籍相关示例图片
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __init__(self, name, book_id, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time
        self.book_id = book_id

    def __str__(self):
        return "<Image: {} {}>".format(self.name, self.create_time.strformat('%Y-%m-%d %H:%M:%S'))

    def model_to_dict(self):
        img_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time,
            'book_id': self.book_id
        }
        return img_dict

    def save(self):
        db.session.add(self)
        db.session.commit()
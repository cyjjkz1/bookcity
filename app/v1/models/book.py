#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime
from supply import Supply
from category import AgeGroup
from flask import current_app as app


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    postage = db.Column(db.String(30), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    choicest = db.Column(db.Integer, nullable=False, default=1)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    age_group_id = db.Column(db.Integer, db.ForeignKey('age_group.id'))
    function_id = db.Column(db.Integer, db.ForeignKey('function.id'))

    images = db.relationship('Image', backref='book_set', lazy='dynamic')
    banner = db.relationship('Banner', backref='book_info', lazy='dynamic')

    def __init__(self, name, price, details,
                 stock, choicest, supply_id, age_group_id,
                 function_id, create_time=datetime.now()):
        self.name = name
        self.price = price
        self.details = details
        self.stock = stock
        self.choicest = choicest
        self.create_time = create_time
        self.supply_id = supply_id
        self.age_group_id = age_group_id
        self.function_id = function_id

    def __str__(self):
        return "<Book: {} {} {} {} {} {}>".format(self.name, self.price, self.details,
                                                  self.stock, self.choicest, self.create_time,
                                                  self.supply_id, self.age_group_id, self.function_id
                                                  )

    def model_to_dict(self, query_img=False, query_supply=False, query_category=False):
        book_dict = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'details': self.details,
            'stock': self.stock,
            'choicest': self.choicest,
            'create_time': self.create_time,
            'supply_id': self.supply_id,
            'age_group_id': self.age_group_id,
            'function_id': self.function_id
        }
        if query_img:
            imgs = []
            if self.images is not None:
                for img in self.images:
                    imgs.append(img.model_to_dict())
            book_dict['images'] = imgs

        if query_supply:
            # 使用一对多的反向查询
            supply = self.supply_set.first()
            if supply is not None:
                book_dict['supply'] = supply.model_to_dict(query_relation=True)
            else:
                book_dict['supply'] = {}

        if query_category:
            age = self.function_set.first()
            if age is not None:
                book_dict['category'] = age.model_to_dict(query_relation=True)
            else:
                book_dict['category'] = {}
        return book_dict

    def save(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

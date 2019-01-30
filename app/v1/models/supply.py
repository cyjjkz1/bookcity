#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db

supply_post = db.Table('supply_post',
                       db.Column('sup_id', db.Integer, db.ForeignKey('supply.id'), primary_key=True),
                       db.Column('post_id', db.Integer, db.ForeignKey('post_company.id'), primary_key=True)
                       )


class Supply(db.Model):
    __tablename__ = 'supply'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    books = db.relationship('Book', backref='supply_set', lazy='dynamic')
    posts = db.relationship('PostCompany', secondary=supply_post,
                           backref=db.backref('supply_set', lazy='dynamic'))


    def __init__(self, name, mobile, address):
        self.name = name
        self.mobile = mobile
        self.address = address

    def __str__(self):
        return '<Supply: {} {} {}>'.format(self.name, self.mobile, self.address)

    def model_to_dict(self):
        sup_dict = {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'address': self.address
        }

        posts = []
        if(self.posts is not None):
            for post in self.posts:
                posts.append(post.model_to_dict())

        sup_dict['posts'] = posts
        return sup_dict


class PostCompany(db.Model):
    __tablename__ = 'post_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    supplys = db.relationship('Supply', secondary=supply_post,
                              backref=db.backref('post_set', lazy='dynamic'))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return '<PostCompany: {} {}>'.format(self.name, self.price)


    def model_to_dict(self):
        post_dict = {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

        supplys = []

        if self.supplys is not None:
            for supply in self.supplys:
                supplys.append(supply.model_to_dict())

        post_dict['supplys'] = supplys
        return post_dict

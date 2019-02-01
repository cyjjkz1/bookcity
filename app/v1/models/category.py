#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db


age_func = db.Table('age_func',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('age_id', db.Integer, db.ForeignKey('age_group.id'), nullable=False),
                    db.Column('func_id', db.Integer, db.ForeignKey('function.id'), nullable=False)
                    )


class AgeGroup(db.Model):
    __tablename__ = 'age_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

    functions = db.relationship('Function',
                                secondary=age_func,
                                backref=db.backref('age_set', lazy='dynamic')
                                )
    books = db.relationship('Book', backref='age_set', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<AgeGroup: {}>'.format(self.name)

    def model_to_dict(self, query_relation=False):
        ag_dict = {
            'id': self.id,
            'name': self.name
        }
        if query_relation:
            funcs = []
            if self.functions is not None:
                for func in self.functions:
                    funcs.append(func.model_to_dict())
            ag_dict['functions'] = funcs
        return ag_dict

    def save(self):
        db.session.add(self)
        db.session.commit()


class Function(db.Model):
    __tablename__ = 'function'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

    books = db.relationship('Book', backref='function_set', lazy='dynamic')

    age_groups = db.relationship('AgeGroup',
                                 secondary=age_func,
                                 backref=db.backref('function_set', lazy='dynamic')
                                 )

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Function: {}>'.format(self.name)

    def model_to_dict(self, query_relation=False):
        fun_dict = {
            'id': self.id,
            'name': self.name
        }
        if query_relation:
            ags = []
            if self.age_groups is not None:
                for ag in self.age_groups:
                    ags.append(ag.model_to_dict())

            fun_dict['age_groups'] = ags
        return fun_dict
    
    def save(self):
        db.session.add(self)
        db.session.commit()
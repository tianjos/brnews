from typing import Dict, Any
from datetime import datetime
from flask import url_for
from werkzeug.datastructures import MultiDict
from app import db


class PaginateMixin:
    @staticmethod
    def to_paginate_collection(query: db.Model, page: int, per_page: int, endpoint: str, **kwargs) -> Dict[str, Any]:
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_json() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class SearchMixin:
    @staticmethod
    def search(model: db.Model, fields: MultiDict) -> Dict[str, db.Model] :
        filtered = {}
        for field in fields:
            key, value = field
            try:
                model_field = getattr(model, key)
            except AttributeError:
                continue
            news = model.query.filter(model_field.like(f'%{value}%')).all()
            filtered.update({new.link: new for new in news})
        return filtered


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    news = db.relationship('News', backref='source', lazy=True)

    def  __repr__(self):
        return f"<Source: {self.name}>"

    def from_json(self, name):
        setattr(self, 'name', name)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'news': self.news
        }

    @classmethod
    def to_collection_json(cls) -> list:
        sources = cls.query.filter_by().all()
        return [source.to_json() for source in sources]

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    news = db.relationship('News', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category: {self.name}>"
    
    def from_json(self, name):
        setattr(self, 'name', name)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'news': self.news
        }
    
    @classmethod
    def to_collection_json(cls) -> list:
        categories = cls.query.filter_by().all()
        return [category.to_json() for category in categories]


class News(db.Model, PaginateMixin, SearchMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    summary = db.Column(db.Text)
    publication_date = db.Column(db.String(64), nullable=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<NEWS: {self.title}>'

    def from_json(self, **data: dict) -> None:
        for item in data:
            try:
                setattr(self, item, data[item])
            except AttributeError:
                pass

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'publication_date': self.publication_date,
            'source': Source.query.filter_by(id=self.source_id).first().to_json(),
            'category': Category.query.filter_by(id=self.category_id).first().to_json()
        }
    
    @classmethod
    def to_collection_json(cls) -> list:
        news = cls.query.filter_by().all()
        return [new.to_json() for new in news]
    
    def add_source(self, source: Source) -> None:
        self.source_id = source.id

    def add_category(self, category: Category) -> None:
        self.category_id = category.id



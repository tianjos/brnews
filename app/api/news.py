from flask import jsonify, request
from app import db
from app import models
from . import api


@api.route('/news/<int:news_id>', methods=['GET'])
def get_news(news_id):
    return jsonify(models.News.query.get_or_404(news_id).to_json())
    
@api.route('/news/', methods=['GET'])
def get_all_news():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = models.News.to_paginate_collection(models.News.query, page, per_page, 'api.get_all_news')
    return jsonify(data)


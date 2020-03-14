from flask import jsonify, request, current_app
from app import db
from app import models
from . import api


@api.route('/news/<int:news_id>', methods=['GET'])
def get_news(news_id):
    return jsonify(models.News.query.get_or_404(news_id).to_json())

@api.route('/news/', methods=['GET'])
def get_all_news():
    return jsonify({'news': models.News.to_collection_json()})


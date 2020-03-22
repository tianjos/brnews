from flask import jsonify
from app import db
from app import models
from . import api


@api.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return jsonify(models.Category.query.get_or_404(category_id).to_json())

@api.route('/categories/', methods=['GET'])
def get_all_categories():
    return jsonify({'categories': models.Category.to_collection_json()})

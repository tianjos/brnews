from flask import jsonify
from app import db
from app import models
from . import api


@api.route('/sources/<int:source_id>', methods=['GET'])
def get_source(source_id):
    return jsonify(models.Source.query.get_or_404(source_id).to_json())

@api.route('/sources/', methods=['GET'])
def get_all_sources():
    return jsonify({'sources': models.Source.to_collection_json()})
    

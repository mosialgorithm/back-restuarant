from app import ma
from marshmallow import fields, ValidationError, validates


class CategorySchema(ma.Schema):
    id = fields.Integer(load_only=True)
    title = fields.String()
    description = fields.String()
    manager_id = fields.Integer()
    image = fields.Raw()
    
category_schema = CategorySchema()

    
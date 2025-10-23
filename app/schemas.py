from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

class ProductCreateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

class SaleSchema(Schema):
    id = fields.Int(dump_only=True)
    sale_date = fields.DateTime(dump_only=True)
    quantity = fields.Int(required=True)
    product = fields.Nested(ProductSchema)

class SaleCreateSchema(Schema):
    quantity = fields.Int(required=True)
    product_id = fields.Int(required=True)
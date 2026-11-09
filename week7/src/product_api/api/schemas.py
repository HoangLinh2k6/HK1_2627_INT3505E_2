from marshmallow import Schema, fields, validate, validates, ValidationError

class ProductIn(Schema):
    sku = fields.Str(required=True, validate=validate.Length(min=1, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))

    @validates("name")
    def validate_name(self, value, **kwargs):
        if value.strip() == "":
            raise ValidationError("Name cannot be blank.")
        
class ProductOut(Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class ProductPatch(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    price_cents = fields.Int(validate=validate.Range(min=0))

class ReserveIn(Schema):
    qty = fields.Int(required=True, validate=validate.Range(min=1))

class OrderItemIn(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

class OrderIn(Schema):
    customer_email = fields.Email(required=True)
    items = fields.List(fields.Nested(OrderItemIn), required=True, validate=validate.Length(min=1))

class OrderItemOut(Schema):
    id = fields.Int()
    product_id = fields.Int()
    quantity = fields.Int()
    price_cents = fields.Int()

class OrderOut(Schema):
    id = fields.Int()
    customer_email = fields.Str()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))
from marshmallow import Schema, fields


class ConversionRequestSchema(Schema):
    from_ = fields.Str(required=True, data_key='from')
    to = fields.Str(required=True, data_key='to')
    amount = fields.Float(required=True, data_key='amount')

    class Meta:
        strict = True

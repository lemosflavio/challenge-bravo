from marshmallow import Schema, fields


class ExchangeRateRequestSchema(Schema):
    exchange_from = fields.Str(required=True, data_key='exchange_from')
    exchange_to = fields.Str(required=True, data_key='exchange_to')
    exchange_tax = fields.Float(required=True, data_key='exchange_tax')

    class Meta:
        strict = True

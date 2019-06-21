"""
Provide forms for block producer investments payback calculator.
"""
from marshmallow import (
    fields,
    Schema,
)


class CalculateInvestmentsPaybackPerMonth(Schema):
    """
    Calculate investments payback per month form.
    """

    money_per_month = fields.Integer()
    token_price = fields.Float()
    active_block_producers_votes = fields.Integer()
    active_block_producers_stakes = fields.Integer()
    stake = fields.Integer()
    votes = fields.Integer()

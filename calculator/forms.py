"""
Provide forms for block producer investments payback calculator.
"""
from marshmallow import (
    fields,
    Schema,
)


class CalculateInvestmentsPaybackPerMonthForm(Schema):
    """
    Calculate investments payback per month form.
    """

    money_per_month = fields.Integer()
    token_price = fields.Float()
    all_block_producers_stakes = fields.Integer()
    active_block_producers_votes = fields.Integer()
    stake = fields.Integer()
    votes = fields.Integer()


class CalculateRoiForm(Schema):
    """
    Calculate returning on investments.
    """

    months = fields.Integer()
    money_per_month = fields.Integer()
    token_price = fields.Float()
    token_price_growth_percent = fields.Integer()
    all_block_producers_stakes = fields.Integer()
    active_block_producers_votes = fields.Integer()
    stake = fields.Integer()
    votes = fields.Integer()

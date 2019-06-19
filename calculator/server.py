"""
Provide endpoints and entrypoints for block producer investments payback calculator.
"""
from http import HTTPStatus

from flask import (
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS

from calculator.domain.block import (
    BlockCost,
    BlockProducer,
)
from calculator.domain.economy import Economy
from calculator.domain.reward import (
    ActiveBlockProducerReward,
    BlockProducerReward,
)
from calculator.forms import CalculateInvestmentsPaybackPerMonth

server = Flask(__name__)
CORS(server)


@server.route('/investments-payback/month', methods=['POST'])
def calculate_investments_payback():
    """
    Calculate investments payback per month.
    """
    request_parameters = request.get_json()

    arguments, errors = CalculateInvestmentsPaybackPerMonth().load({
        'money_per_month': request_parameters.get('economy').get('money_per_month'),
        'token_price': request_parameters.get('economy').get('token_price'),
        'active_block_producers_votes': request_parameters.get('economy').get('active_block_producers_votes'),
        'active_block_producers_stakes': request_parameters.get('economy').get('active_block_producers_stakes'),
        'stake': request_parameters.get('block_producer').get('stake'),
        'votes': request_parameters.get('block_producer').get('votes'),
    })

    if errors:
        return jsonify({'errors': errors}), HTTPStatus.BAD_REQUEST

    money_per_month = arguments.get('money_per_month')
    token_price = arguments.get('token_price')
    active_block_producers_votes = arguments.get('active_block_producers_votes')
    active_block_producers_stakes = arguments.get('active_block_producers_stakes')
    stake = arguments.get('stake')
    votes = arguments.get('votes')

    economy = Economy(
        money_per_month=money_per_month,
        token_price=token_price,
        active_block_producers_votes=active_block_producers_votes,
        active_block_producers_stakes=active_block_producers_stakes,
    )
    block_cost = BlockCost(economy=economy)
    block_producer = BlockProducer(stake=stake, votes=votes)

    block_producer_reward = BlockProducerReward(economy=economy, block_cost=block_cost, block_producer=block_producer)

    active_block_producer_reward = ActiveBlockProducerReward(
        economy=economy, block_cost=block_cost, block_producer=block_producer,
    )

    result = (block_producer_reward.get() + active_block_producer_reward.get()) * economy.blocks_per_month

    return jsonify({'payback': result}), HTTPStatus.OK


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8000)

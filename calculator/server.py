"""
Provide endpoints and entrypoints for block producer investments payback calculator.
"""
import os
from http import HTTPStatus

import requests
from flask import (
    Flask,
    jsonify,
    request,
)
from flask_caching import Cache
from flask_cors import CORS

from calculator.constants import (
    HOUR_IN_SECONDS,
    REMME_TOKEN_PRICE_IN_USD_COIN_MARKET_CAP_API_URL,
)
from calculator.domain.block import (
    BlockProducer,
    BlockReward,
)
from calculator.domain.economy import Economy
from calculator.domain.reward import (
    ActiveBlockProducerReward,
    BlockProducerReward,
)
from calculator.domain.roi import Roi
from calculator.forms import (
    CalculateInvestmentsPaybackPerMonthForm,
    CalculateRoiForm,
)

server = Flask(__name__)
CORS(server)

cache = Cache(server, config={'CACHE_TYPE': 'simple'})


@server.route('/token/price/usd', methods=['GET'])
@cache.cached(timeout=HOUR_IN_SECONDS)
def get_token_price_in_usd():
    """
    Get Remme token price in dollars (USD).
    """
    get_token_price_response = requests.get(REMME_TOKEN_PRICE_IN_USD_COIN_MARKET_CAP_API_URL, headers={
        'X-CMC_PRO_API_KEY': os.environ.get('COIN_MARKET_CAP_API_KEY'),
    }).json()

    try:
        result = get_token_price_response['data']['REM']['quote']['USD']['price']
    except KeyError:
        return jsonify({'errors': 'Errors have been occurred during the request token price.'}), HTTPStatus.BAD_REQUEST

    return jsonify({'result': result}), HTTPStatus.OK


@server.route('/profit/month', methods=['POST'])
def calculate_profit_per_month():
    """
    Calculate investments payback per month.
    """
    request_parameters = request.get_json()

    arguments, errors = CalculateInvestmentsPaybackPerMonthForm().load({
        'money_per_month': request_parameters.get('economy').get('money_per_month'),
        'token_price': request_parameters.get('economy').get('token_price'),
        'all_block_producers_stakes': request_parameters.get('economy').get('all_block_producers_stakes'),
        'active_block_producers_votes': request_parameters.get('economy').get('active_block_producers_votes'),
        'stake': request_parameters.get('block_producer').get('stake'),
        'votes': request_parameters.get('block_producer').get('votes'),
    })

    if errors:
        return jsonify({'errors': errors}), HTTPStatus.BAD_REQUEST

    money_per_month = arguments.get('money_per_month')
    token_price = arguments.get('token_price')
    all_block_producers_stakes = arguments.get('all_block_producers_stakes')
    active_block_producers_votes = arguments.get('active_block_producers_votes')
    block_producer_stake = arguments.get('stake')
    block_producer_votes = arguments.get('votes')

    economy = Economy(
        money_per_month=money_per_month,
        token_price=token_price,
        all_block_producers_stakes=all_block_producers_stakes,
        active_block_producers_votes=active_block_producers_votes,
    )
    block_reward = BlockReward(economy=economy)
    block_producer = BlockProducer(stake=block_producer_stake, votes=block_producer_votes)

    block_producer_reward = BlockProducerReward(
        economy=economy, block_reward=block_reward, block_producer=block_producer,
    )

    active_block_producer_reward = ActiveBlockProducerReward(
        economy=economy, block_reward=block_reward, block_producer=block_producer,
    )

    month_reward_in_tokens = \
        (block_producer_reward.get() + active_block_producer_reward.get()) * economy.blocks_per_month

    result = {
        'tokens': month_reward_in_tokens,
        'fiat': month_reward_in_tokens * economy.token_price,
    }

    return jsonify({'result': result}), HTTPStatus.OK


@server.route('/profit/roi', methods=['POST'])
def calculate_roi():
    """
    Calculate returning on investment for 4 years.
    """
    request_parameters = request.get_json()

    arguments, errors = CalculateRoiForm().load({
        'months': request_parameters.get('months'),
        'money_per_month': request_parameters.get('economy').get('money_per_month'),
        'token_price': request_parameters.get('economy').get('token_price'),
        'token_price_growth_percent': request_parameters.get('economy').get('token_price_growth_percent'),
        'all_block_producers_stakes': request_parameters.get('economy').get('all_block_producers_stakes'),
        'active_block_producers_votes': request_parameters.get('economy').get('active_block_producers_votes'),
        'stake': request_parameters.get('block_producer').get('stake'),
        'votes': request_parameters.get('block_producer').get('votes'),
    })

    if errors:
        return jsonify({'errors': errors}), HTTPStatus.BAD_REQUEST

    months = arguments.get('months')
    money_per_month = arguments.get('money_per_month')
    token_price = arguments.get('token_price')
    token_price_growth_percent = arguments.get('token_price_growth_percent')
    all_block_producers_stakes = arguments.get('all_block_producers_stakes')
    active_block_producers_votes = arguments.get('active_block_producers_votes')
    block_producer_stake = arguments.get('stake')
    block_producer_votes = arguments.get('votes')

    economy = Economy(
        money_per_month=money_per_month,
        token_price=token_price,
        token_price_growth_percent=token_price_growth_percent,
        all_block_producers_stakes=all_block_producers_stakes,
        active_block_producers_votes=active_block_producers_votes,
    )
    block_reward = BlockReward(economy=economy)
    block_producer = BlockProducer(stake=block_producer_stake, votes=block_producer_votes)

    roi = Roi(economy=economy, block_reward=block_reward, block_producer=block_producer)
    result = roi.calculate(months=months)

    return jsonify({'result': result}), HTTPStatus.OK


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8000)

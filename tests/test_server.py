"""
Provide tests for block producer investments payback calculator.
"""
from http import HTTPStatus


def test_get_token_price_in_usd(client, mocker):
    """
    Case: get token price in dollars (usd)
    Expect: price as float is returned.
    """
    class Response:
        """
        Fake response.
        """

        def json(self):
            """
            Fake json method.
            """
            return {
                'data': {
                    'REM': {
                        'quote': {
                            'USD': {
                                'price': 0.0071
                            }
                        }
                    }
                }
            }

    expected_response = {
        'result': 0.0071,
    }

    mock_token_price_in_usd = mocker.patch('requests.get')
    mock_token_price_in_usd.return_value = Response()

    response = client.get('/token/price/usd')

    assert expected_response == response.json
    assert HTTPStatus.OK == response.status_code


def test_calculate_profit_per_month(client):
    """
    Case: calculate investments payback per month.
    Expect: payback is returned.
    """
    expected_response = {
        'result': {
            'fiat': 39.964317726236075,
            'tokens': 5628.777144540292,
        },
    }

    response = client.post('/profit/month', json={
        'economy': {
            'money_per_month': 50_000,
            'token_price': 0.0071,
            'all_block_producers_stakes': 350_000_000,
            'active_block_producers_votes': 300_000_000,
        },
        'block_producer': {
            'stake': 300_000,
            'votes': 300_000,
        },
    })

    assert expected_response == response.json
    assert HTTPStatus.OK == response.status_code


def test_calculate_profit_per_month_with_invalid_arguments(client):
    """
    Case: calculate investments payback per month with invalid arguments.
    Expect: not a valid integer or number error message.
    """
    response = client.post('/profit/month', json={
        'economy': {
            'money_per_month': 'invalid_argument',
            'token_price': 'invalid_argument',
            'all_block_producers_stakes': 'invalid_argument',
            'active_block_producers_votes': 'invalid_argument',
        },
        'block_producer': {
            'stake': 'invalid_argument',
            'votes': 'invalid_argument',
        },
    })

    expected_error = {
        'errors': {
            'money_per_month':  ['Not a valid integer.'],
            'token_price':  ['Not a valid number.'],
            'all_block_producers_stakes':  ['Not a valid integer.'],
            'active_block_producers_votes':  ['Not a valid integer.'],
            'stake':  ['Not a valid integer.'],
            'votes':  ['Not a valid integer.'],
        }
    }

    assert expected_error == response.json
    assert HTTPStatus.BAD_REQUEST == response.status_code


def test_calculate_roi_with_invalid_arguments(client):
    """
    Case: calculate returning on investment for 4 years with invalid arguments.
    Expect: not a valid integer or number error message.
    """
    response = client.post('/profit/month', json={
        'economy': {
            'money_per_month': 'invalid_argument',
            'token_price': 'invalid_argument',
            'all_block_producers_stakes': 'invalid_argument',
            'active_block_producers_votes': 'invalid_argument',
        },
        'block_producer': {
            'stake': 'invalid_argument',
            'votes': 'invalid_argument',
        },
    })

    expected_error = {
        'errors': {
            'money_per_month':  ['Not a valid integer.'],
            'token_price':  ['Not a valid number.'],
            'all_block_producers_stakes':  ['Not a valid integer.'],
            'active_block_producers_votes':  ['Not a valid integer.'],
            'stake':  ['Not a valid integer.'],
            'votes':  ['Not a valid integer.'],
        }
    }

    assert expected_error == response.json
    assert HTTPStatus.BAD_REQUEST == response.status_code


def test_calculate_roi(client):
    """
    Case: calculate returning on investment for the year.
    Expect: data per month and ROI percents for tokens and fiat are returned.
    """
    expected_response = {
        'result': {
            'percents': {
                'fiat': 64.73746422445299,
                'tokens': 19.00984920867224
            },
            'statistics_per_month': [
                {
                    'block_producer_stake_in_fiat': 2130.0,
                    'block_producer_stake_in_tokens': 300000,
                    'month': 1,
                    'month_reward_in_fiat': 39.964317726236075,
                    'month_reward_in_tokens': 5628.777144540292,
                    'token_price': 0.0071
                },
                {
                    'block_producer_stake_in_fiat': 2235.0632472580232,
                    'block_producer_stake_in_tokens': 305628.7771445403,
                    'month': 2,
                    'month_reward_in_fiat': 40.52622271773658,
                    'month_reward_in_tokens': 5541.668633630053,
                    'token_price': 0.007313000000000001
                },
                {
                    'block_producer_stake_in_fiat': 2343.8571540750327,
                    'block_producer_stake_in_tokens': 311170.4457781703,
                    'month': 3,
                    'month_reward_in_fiat': 41.07941427128649,
                    'month_reward_in_tokens': 5453.7025129190715,
                    'token_price': 0.007532390000000001
                },
                {
                    'block_producer_stake_in_fiat': 2456.484665396709,
                    'block_producer_stake_in_tokens': 316624.1482910894,
                    'month': 4,
                    'month_reward_in_fiat': 41.62380760703977,
                    'month_reward_in_tokens': 5365.025403113104,
                    'token_price': 0.007758361700000001
                },
                {
                    'block_producer_stake_in_fiat': 2573.051727193861,
                    'block_producer_stake_in_tokens': 321989.1736942025,
                    'month': 5,
                    'month_reward_in_fiat': 42.15933257772076,
                    'month_reward_in_tokens': 5275.777597757021,
                    'token_price': 0.007991112551
                },
                {
                    'block_producer_stake_in_fiat': 2693.667391564729,
                    'block_producer_stake_in_tokens': 327264.9512919595,
                    'month': 6,
                    'month_reward_in_fiat': 42.685933034455694,
                    'month_reward_in_tokens': 5186.093071148683,
                    'token_price': 0.008230845927530001
                },
                {
                    'block_producer_stake_in_fiat': 2818.44392433716,
                    'block_producer_stake_in_tokens': 332451.0443631082,
                    'month': 7,
                    'month_reward_in_fiat': 43.203566193615366,
                    'month_reward_in_tokens': 5096.0995098229605,
                    'token_price': 0.0084777713053559
                },
                {
                    'block_producer_stake_in_fiat': 2947.4969152466983,
                    'block_producer_stake_in_tokens': 337547.14387293113,
                    'month': 8,
                    'month_reward_in_fiat': 43.71220200701603,
                    'month_reward_in_tokens': 5005.918365356429,
                    'token_price': 0.008732104444516577
                },
                {
                    'block_producer_stake_in_fiat': 3080.9453907713264,
                    'block_producer_stake_in_tokens': 342553.0622382876,
                    'month': 9,
                    'month_reward_in_fiat': 44.21182253760011,
                    'month_reward_in_tokens': 4915.664926342325,
                    'token_price': 0.008994067577852075
                },
                {
                    'block_producer_stake_in_fiat': 3218.9119297081943,
                    'block_producer_stake_in_tokens': 347468.7271646299,
                    'month': 10,
                    'month_reward_in_fiat': 44.70242134250308,
                    'month_reward_in_tokens': 4825.448407488621,
                    'token_price': 0.009263889605187637
                },
                {
                    'block_producer_stake_in_fiat': 3361.522781582218,
                    'block_producer_stake_in_tokens': 352294.17557211855,
                    'month': 11,
                    'month_reward_in_fiat': 45.18400286520739,
                    'month_reward_in_tokens': 4735.372053898171,
                    'token_price': 0.009541806293343266
                },
                {
                    'block_producer_stake_in_fiat': 3508.9079879808487,
                    'block_producer_stake_in_tokens': 357029.5476260167,
                    'month': 12,
                    'month_reward_in_fiat': 45.65658183829063,
                    'month_reward_in_tokens': 4645.533258697715,
                    'token_price': 0.009828060482143564
                }
            ]
        }
    }

    response = client.post('/profit/roi', json={
        'months': 12,
        'economy': {
            'money_per_month': 50_000,
            'token_price': 0.0071,
            'token_price_growth_percent': 3,
            'all_block_producers_stakes': 350_000_000,
            'active_block_producers_votes': 300_000_000,
        },
        'block_producer': {
            'stake': 300_000,
            'votes': 300_000,
        },
    })

    assert expected_response == response.json
    assert HTTPStatus.OK == response.status_code

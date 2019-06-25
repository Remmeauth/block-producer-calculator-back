"""
Provide tests for block producer investments payback calculator.
"""
from http import HTTPStatus


def test_get_token_price_in_usd(client, mocker):
    """
    Case: get Remme token price in dollars (usd)
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
        'price': 0.0071,
    }

    mock_token_price_in_usd = mocker.patch('requests.get')
    mock_token_price_in_usd.return_value = Response()

    response = client.get('/token/price/usd')

    assert expected_response == response.json
    assert HTTPStatus.OK == response.status_code


def test_calculate_investments_payback(client):
    """
    Case: calculate investments payback per month.
    Expect: payback is returned.
    """
    expected_response = {
        'payback': 5_628.777_144_540_292
    }

    response = client.post('/investments-payback/month', json={
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


def test_calculate_investments_payback_with_invalid_arguments(client):
    """
    Case: calculate investments payback per month with invalid arguments.
    Expect: not a valid integer or number error message.
    """
    response = client.post('/investments-payback/month', json={
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

"""
Provide tests for block producer investments payback calculator.
"""
from http import HTTPStatus


def test_calculate_investments_payback(client):
    """
    Case: calculate investments payback per month.
    Expect: payback is returned.
    """
    expected_response = {
        'payback': 144691.22426868905,
    }

    response = client.post('/investments-payback/month', json={
        'economy': {
            'money_per_month': 50000,
            'token_price': 0.0071,
            'active_block_producers_stakes': 300000000,
            'active_block_producers_votes': 10000000,
        },
        'block_producer': {
            'stake': 300000,
            'votes': 1000000,
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
            'active_block_producers_stakes': 'invalid_argument',
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
            'active_block_producers_stakes':  ['Not a valid integer.'],
            'active_block_producers_votes':  ['Not a valid integer.'],
            'stake':  ['Not a valid integer.'],
            'votes':  ['Not a valid integer.'],
        }
    }

    assert expected_error == response.json
    assert HTTPStatus.BAD_REQUEST == response.status_code

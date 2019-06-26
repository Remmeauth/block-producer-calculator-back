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


def test_calculate_roi_with_invalid_arguments(client):
    """
    Case: calculate returning on investment for 4 years with invalid arguments.
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


def test_calculate_roi(client):
    """
    Case: calculate returning on investment for 4 years.
    Expect: data per month and ROI percent are returned.
    """
    expected_response = {
        'result': {
            'percent': 26.220804592280146,
            'statistics_per_month': [
                {
                    'block_producer_stake': 300000,
                    'month': 1,
                    'month_reward': 5628.777144540292,
                    'token_price': 0.0071,
                    'token_price_growth_percent': 10
                },
                {
                    'block_producer_stake': 305628.7771445403,
                    'month': 2,
                    'month_reward': 5189.0169933081415,
                    'token_price': 0.00781,
                    'token_price_growth_percent': 9.8
                },
                {
                    'block_producer_stake': 310817.7941378484,
                    'month': 3,
                    'month_reward': 4786.2848869524105,
                    'token_price': 0.00857538,
                    'token_price_growth_percent': 9.604000000000001
                },
                {
                    'block_producer_stake': 315604.07902480086,
                    'month': 4,
                    'month_reward': 4417.721420564035,
                    'token_price': 0.0093989594952,
                    'token_price_growth_percent': 9.41192
                },
                {
                    'block_producer_stake': 320021.8004453649,
                    'month': 5,
                    'month_reward': 4080.577706989182,
                    'token_price': 0.010283582043720627,
                    'token_price_growth_percent': 9.2236816
                },
                {
                    'block_producer_stake': 324102.3781523541,
                    'month': 6,
                    'month_reward': 3772.245386875073,
                    'token_price': 0.011232106908508191,
                    'token_price_growth_percent': 9.039207968000001
                },
                {
                    'block_producer_stake': 327874.62353922916,
                    'month': 7,
                    'month_reward': 3490.2742511900797,
                    'token_price': 0.012247400411156342,
                    'token_price_growth_percent': 8.858423808640001
                },
                {
                    'block_producer_stake': 331364.8977904192,
                    'month': 8,
                    'month_reward': 3232.3807463058647,
                    'token_price': 0.013332327045117689,
                    'token_price_growth_percent': 8.6812553324672
                },
                {
                    'block_producer_stake': 334597.2785367251,
                    'month': 9,
                    'month_reward': 2996.4498992245963,
                    'token_price': 0.014489740397663936,
                    'token_price_growth_percent': 8.507630225817856
                },
                {
                    'block_producer_stake': 337593.7284359497,
                    'month': 10,
                    'month_reward': 2780.5326109024695,
                    'token_price': 0.01572247393137813,
                    'token_price_growth_percent': 8.337477621301499
                },
                {
                    'block_producer_stake': 340374.26104685216,
                    'month': 11,
                    'month_reward': 2582.839796924306,
                    'token_price': 0.017033331676921747,
                    'token_price_growth_percent': 8.17072806887547
                },
                {
                    'block_producer_stake': 342957.1008437765,
                    'month': 12,
                    'month_reward': 2401.734486189414,
                    'token_price': 0.01842507888931265,
                    'token_price_growth_percent': 8.00731350749796
                },
                {
                    'block_producer_stake': 345358.8353299659,
                    'month': 13,
                    'month_reward': 2235.72270113225,
                    'token_price': 0.019900432719983735,
                    'token_price_growth_percent': 7.847167237348001
                },
                {
                    'block_producer_stake': 347594.55803109816,
                    'month': 14,
                    'month_reward': 2083.443721265036,
                    'token_price': 0.021462052956476782,
                    'token_price_growth_percent': 7.690223892601041
                },
                {
                    'block_producer_stake': 349678.00175236317,
                    'month': 15,
                    'month_reward': 1943.6601620277243,
                    'token_price': 0.02311253288077845,
                    'token_price_growth_percent': 7.5364194147490196
                },
                {
                    'block_producer_stake': 351621.6619143909,
                    'month': 16,
                    'month_reward': 1815.2481719905718,
                    'token_price': 0.024854390296045685,
                    'token_price_growth_percent': 7.385691026454039
                },
                {
                    'block_producer_stake': 353436.9100863815,
                    'month': 17,
                    'month_reward': 1697.1879544066862,
                    'token_price': 0.0266900587698206,
                    'token_price_growth_percent': 7.237977205924959
                },
                {
                    'block_producer_stake': 355134.09804078814,
                    'month': 18,
                    'month_reward': 1588.5547467758959,
                    'token_price': 0.028621879139828194,
                    'token_price_growth_percent': 7.0932176618064595
                },
                {
                    'block_producer_stake': 356722.65278756403,
                    'month': 19,
                    'month_reward': 1488.5103387643794,
                    'token_price': 0.030652091326115384,
                    'token_price_growth_percent': 6.95135330857033
                },
                {
                    'block_producer_stake': 358211.16312632844,
                    'month': 20,
                    'month_reward': 1396.2951700494195,
                    'token_price': 0.032782826490659306,
                    'token_price_growth_percent': 6.812326242398924
                },
                {
                    'block_producer_stake': 359607.45829637785,
                    'month': 21,
                    'month_reward': 1311.2210219281899,
                    'token_price': 0.0350160995826826,
                    'token_price_growth_percent': 6.676079717550945
                },
                {
                    'block_producer_stake': 360918.67931830604,
                    'month': 22,
                    'month_reward': 1232.6642971288313,
                    'token_price': 0.03735380230479951,
                    'token_price_growth_percent': 6.542558123199926
                },
                {
                    'block_producer_stake': 362151.3436154349,
                    'month': 23,
                    'month_reward': 1160.0598690953557,
                    'token_price': 0.039797696531816217,
                    'token_price_growth_percent': 6.411706960735928
                },
                {
                    'block_producer_stake': 363311.4034845302,
                    'month': 24,
                    'month_reward': 1092.895473475707,
                    'token_price': 0.042349408210559235,
                    'token_price_growth_percent': 6.283472821521209
                },
                {
                    'block_producer_stake': 364404.2989580059,
                    'month': 25,
                    'month_reward': 1030.7066093952164,
                    'token_price': 0.045010421765544796,
                    'token_price_growth_percent': 6.157803365090785
                },
                {
                    'block_producer_stake': 365435.0055674011,
                    'month': 26,
                    'month_reward': 973.071915411431,
                    'token_price': 0.04778207503166507,
                    'token_price_growth_percent': 6.034647297788969
                },
                {
                    'block_producer_stake': 366408.0774828126,
                    'month': 27,
                    'month_reward': 919.6089841151005,
                    'token_price': 0.050665554731390935,
                    'token_price_growth_percent': 5.91395435183319
                },
                {
                    'block_producer_stake': 367327.6864669277,
                    'month': 28,
                    'month_reward': 869.9705796358895,
                    'token_price': 0.05366189251030845,
                    'token_price_growth_percent': 5.795675264796526
                },
                {
                    'block_producer_stake': 368197.6570465636,
                    'month': 29,
                    'month_reward': 823.8412234349661,
                    'token_price': 0.0567719615411501,
                    'token_price_growth_percent': 5.679761759500596
                },
                {
                    'block_producer_stake': 369021.4982699985,
                    'month': 30,
                    'month_reward': 780.9341154277948,
                    'token_price': 0.059996473702882726,
                    'token_price_growth_percent': 5.566166524310584
                },
                {
                    'block_producer_stake': 369802.4323854263,
                    'month': 31,
                    'month_reward': 740.9883594652329,
                    'token_price': 0.06333597733789939,
                    'token_price_growth_percent': 5.454843193824373
                },
                {
                    'block_producer_stake': 370543.4207448915,
                    'month': 32,
                    'month_reward': 703.7664643547548,
                    'token_price': 0.06679085558695794,
                    'token_price_growth_percent': 5.345746329947885
                },
                {
                    'block_producer_stake': 371247.1872092463,
                    'month': 33,
                    'month_reward': 669.0520938161885,
                    'token_price': 0.07036132529823853,
                    'token_price_growth_percent': 5.238831403348928
                },
                {
                    'block_producer_stake': 371916.23930306244,
                    'month': 34,
                    'month_reward': 636.6480409611055,
                    'token_price': 0.07404743650377514,
                    'token_price_growth_percent': 5.13405477528195
                },
                {
                    'block_producer_stake': 372552.88734402356,
                    'month': 35,
                    'month_reward': 606.3744050101346,
                    'token_price': 0.07784907245357109,
                    'token_price_growth_percent': 5.03137367977631
                },
                {
                    'block_producer_stake': 373159.2617490337,
                    'month': 36,
                    'month_reward': 578.0669499844734,
                    'token_price': 0.08176595019495006,
                    'token_price_growth_percent': 4.930746206180784
                },
                {
                    'block_producer_stake': 373737.32869901817,
                    'month': 37,
                    'month_reward': 551.5756270066857,
                    'token_price': 0.08579762168213524,
                    'token_price_growth_percent': 4.832131282057168
                },
                {
                    'block_producer_stake': 374288.9043260249,
                    'month': 38,
                    'month_reward': 526.7632436110597,
                    'token_price': 0.08994347539869876,
                    'token_price_growth_percent': 4.735488656416025
                },
                {
                    'block_producer_stake': 374815.66756963596,
                    'month': 39,
                    'month_reward': 503.5042650917909,
                    'token_price': 0.09420273847339049,
                    'token_price_growth_percent': 4.640778883287704
                },
                {
                    'block_producer_stake': 375319.17183472775,
                    'month': 40,
                    'month_reward': 481.6837344092995,
                    'token_price': 0.09857447926794234,
                    'token_price_growth_percent': 4.54796330562195
                },
                {
                    'block_producer_stake': 375800.855569137,
                    'month': 41,
                    'month_reward': 461.19629853546036,
                    'token_price': 0.10305761041375627,
                    'token_price_growth_percent': 4.457004039509511
                },
                {
                    'block_producer_stake': 376262.0518676725,
                    'month': 42,
                    'month_reward': 441.9453303539791,
                    'token_price': 0.10765089227291937,
                    'token_price_growth_percent': 4.367863958719321
                },
                {
                    'block_producer_stake': 376703.99719802645,
                    'month': 43,
                    'month_reward': 423.8421363502697,
                    'token_price': 0.112352936797748,
                    'token_price_growth_percent': 4.280506679544934
                },
                {
                    'block_producer_stake': 377127.83933437674,
                    'month': 44,
                    'month_reward': 406.80524133438826,
                    'token_price': 0.1171622117620405,
                    'token_price_growth_percent': 4.194896545954036
                },
                {
                    'block_producer_stake': 377534.6445757111,
                    'month': 45,
                    'month_reward': 390.75974234939537,
                    'token_price': 0.12207704533640969,
                    'token_price_growth_percent': 4.110998615034955
                },
                {
                    'block_producer_stake': 377925.4043180605,
                    'month': 46,
                    'month_reward': 375.63672473447616,
                    'token_price': 0.12709563097946508,
                    'token_price_growth_percent': 4.028778642734256
                },
                {
                    'block_producer_stake': 378301.041042795,
                    'month': 47,
                    'month_reward': 361.37273404540684,
                    'token_price': 0.13221603261621412,
                    'token_price_growth_percent': 3.948203069879571
                },
                {
                    'block_producer_stake': 378662.41377684043,
                    'month': 48,
                    'month_reward': 347.90929819234447,
                    'token_price': 0.13743619007484045,
                    'token_price_growth_percent': 3.8692390084819794
                }
            ]
        }
    }

    response = client.post('/roi', json={
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

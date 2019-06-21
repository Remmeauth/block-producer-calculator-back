"""
Provide tests for block.
"""
from calculator.domain.block import BlockCost
from calculator.domain.economy import Economy


def test_get_block_cost():
    """
    Case: get a block cost.
    Expect: block cost is returned.
    """
    expected_result = 1.3584593983655016

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )
    block_cost = BlockCost(economy=economy)

    assert expected_result == block_cost.get()

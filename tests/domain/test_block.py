"""
Provide tests for block.
"""
from calculator.domain.block import BlockReward
from calculator.domain.economy import Economy


def test_get_block_reward():
    """
    Case: get a block reward.
    Expect: block reward is returned.
    """
    expected_result = 1.3584593983655016

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        all_block_producers_stakes=350_000_000,
        active_block_producers_votes=300_000_000,
    )
    block_reward = BlockReward(economy=economy)

    assert expected_result == block_reward.get()

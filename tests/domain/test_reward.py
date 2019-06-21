"""
Provide tests for reward.
"""
from calculator.domain.block import (
    BlockCost,
    BlockProducer,
)
from calculator.domain.economy import Economy
from calculator.domain.reward import (
    ActiveBlockProducerReward,
    BlockProducerReward,
)


def test_get_block_producer_reward():
    """
    Case: get block producer reward.
    Expect: reward is returned.
    """
    expected_result = 0.0007419278252611585

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )
    block_cost = BlockCost(economy=economy)
    block_producer = BlockProducer(stake=300_000, votes=1_000_000)

    block_producer_reward = BlockProducerReward(economy=economy, block_cost=block_cost, block_producer=block_producer)

    assert expected_result == block_producer_reward.get()


def test_get_active_block_producer_reward():
    """
    Case: get an active block producer reward.
    Expect: reward is returned.
    """
    expected_result = 0.027169187967310035

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )
    block_cost = BlockCost(economy=economy)
    block_producer = BlockProducer(stake=300_000, votes=1_000_000)

    active_block_producer_reward = ActiveBlockProducerReward(
        economy=economy,
        block_cost=block_cost,
        block_producer=block_producer,
    )

    assert expected_result == active_block_producer_reward.get()


def test_get_active_block_producer_reward_for_non_active_block_producer():
    """
    Case: get active block producer reward for non active block producer.
    Expect: zero as reward is returned.
    """
    expected_result = 0

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )
    block_cost = BlockCost(economy=economy)
    block_producer = BlockProducer(stake=300_000, votes=0)

    active_block_producer_reward = ActiveBlockProducerReward(
        economy=economy,
        block_cost=block_cost,
        block_producer=block_producer,
    )

    assert expected_result == active_block_producer_reward.get()

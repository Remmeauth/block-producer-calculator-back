"""
Provide implementation of the reward.
"""
from calculator.domain.block import (
    BlockCost,
    BlockProducer,
)
from calculator.domain.economy import Economy


class BlockProducerReward:
    """
    Implements block producer reward.
    """

    def __init__(self, economy: Economy, block_cost: BlockCost, block_producer: BlockProducer):
        """
        Constructor.
        """
        self.economy = economy
        self.block_cost = block_cost
        self.block_producer = block_producer

    def get(self):
        """
        Get a block producer reward.
        """
        all_block_producers_stakes = self.economy.block_producers_stakes + self.economy.active_block_producers_stakes

        return (self.block_producer.stake * self.block_cost.get() / all_block_producers_stakes) * \
            self.economy.block_producers_reward_coefficient


class ActiveBlockProducerReward:
    """
    Implements an active block producer reward.
    """

    def __init__(self, economy: Economy, block_cost: BlockCost, block_producer: BlockProducer):
        """
        Constructor.
        """
        self.economy = economy
        self.block_cost = block_cost
        self.block_producer = block_producer

    def get(self):
        """
        Get an active block producer reward.
        """
        return (self.block_producer.votes * self.block_cost.get() / self.economy.active_block_producers_votes) * \
            self.economy.active_block_producers_reward_coefficient

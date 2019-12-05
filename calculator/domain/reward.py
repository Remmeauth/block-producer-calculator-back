"""
Provide implementation of the reward.
"""
from calculator.domain.block import (
    BlockProducer,
    BlockReward,
)
from calculator.domain.economy import Economy


class BlockProducerReward:
    """
    Implements block producer reward.
    """

    def __init__(self, economy: Economy, block_reward: BlockReward, block_producer: BlockProducer):
        """
        Constructor.
        """
        self.economy = economy
        self.block_reward = block_reward
        self.block_producer = block_producer

    def get(self):
        """
        Get a block producer reward.
        """
        sum_of_stakes = self.economy.all_block_producers_stakes + self.block_producer.stake

        return (self.block_producer.stake * (self.block_reward.get() +
                                             self.economy.to_rewards_pool/12/self.economy.blocks_per_month)
                / sum_of_stakes) * \
            self.economy.block_producers_reward_coefficient


class ActiveBlockProducerReward:
    """
    Implements an active block producer reward.
    """

    def __init__(self, economy: Economy, block_reward: BlockReward, block_producer: BlockProducer):
        """
        Constructor.
        """
        self.economy = economy
        self.block_reward = block_reward
        self.block_producer = block_producer

    def get(self):
        """
        Get an active block producer reward.
        """
        sum_of_votes = self.economy.active_block_producers_votes + self.block_producer.votes

        return (self.block_producer.votes * (self.block_reward.get() +
                                             self.economy.to_rewards_pool/12/self.economy.blocks_per_month)
                / sum_of_votes) * \
            self.economy.active_block_producers_reward_coefficient

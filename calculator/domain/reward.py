"""
Docs.
"""
from calculator.economy import Economy
from calculator.block_producer import BlockProducer


class BlockProducerReward:
    """
    Docs.
    """

    def __init__(self, economy: Economy, block_producer: BlockProducer):
        """
        Docs.
        """
        self.economy = economy
        self.block_producer = block_producer

    def get(self):
        """
        Docs.
        """
        return (self.block_producer.stake * self.economy.block_reward / self.economy.stakes) * \
            self.economy.block_producers_reward_coefficient


class ActiveBlockProducerReward:
    """
    Docs.
    """

    def __init__(self, economy: Economy, block_producer: BlockProducer):
        """
        Docs.
        """
        self.economy = economy
        self.block_producer = block_producer

    def get(self):
        """
        Docs.
        """
        return (self.block_producer.votes * self.economy.block_reward / self.economy.votes) * \
            self.economy.active_block_producers_reward_coefficient

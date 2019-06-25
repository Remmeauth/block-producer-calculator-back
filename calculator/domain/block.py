"""
Provide implementation of the block.
"""
from calculator.domain.economy import Economy


class BlockReward:
    """
    Implements block reward.
    """

    def __init__(self, economy: Economy):
        """
        Constructor.
        """
        self.economy = economy

    def get(self):
        """
        Get a block reward.
        """
        return self.economy.money_per_month / self.economy.token_price / self.economy.blocks_per_month


class BlockProducer:
    """
    Implements block producer.
    """

    def __init__(self, stake: int, votes: int):
        """
        Constructor.
        """
        self.stake = stake
        self.votes = votes

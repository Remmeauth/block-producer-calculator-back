"""
Provide implementation of the block.
"""
from calculator.domain.economy import Economy


class BlockCost:
    """
    Implements block cost.
    """

    def __init__(self, economy: Economy):
        """
        Constructor.
        """
        self.economy = economy

    def get(self):
        """
        Get a block cost.
        """
        return self.economy.block_producers_stakes / (self.economy.blocks_per_month * 12)


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

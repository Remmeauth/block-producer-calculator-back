"""
Provide implementation of the economy.
"""


class Economy:
    """
    Implements economy.
    """

    def __init__(
            self,
            money_per_month: int,
            token_price: float,
            active_block_producers_stakes: int,
            active_block_producers_votes: int,
    ):
        """
        Constructor.
        """
        self._money_per_month = money_per_month
        self._token_price = token_price
        self._active_block_producers_stakes = active_block_producers_stakes
        self._active_block_producers_votes = active_block_producers_votes

    @property
    def money_per_month(self):
        """
        Get money per month.
        """
        return self._money_per_month

    @property
    def blocks_per_month(self):
        """
        Get blocks per month.
        """
        return 60 * 60 * 24 * 30 * 2

    @property
    def block_reward(self):
        """
        Get block reward.
        """
        return self.money_per_month / (self.blocks_per_month * 12)

    @property
    def block_producers_stakes(self):
        """
        Get block producers stakes.
        """
        return self.money_per_month / self._token_price * 12

    @property
    def active_block_producers_stakes(self):
        """
        Get an active block producers stakes.
        """
        return self._active_block_producers_stakes

    @property
    def active_block_producers_votes(self):
        """
        Get an active block producers votes.
        """
        return self._active_block_producers_votes

    @property
    def block_producers_reward_coefficient(self):
        """
        Get block producers reward coefficient.
        """
        return 0.7

    @property
    def active_block_producers_reward_coefficient(self):
        """
        Get an active block producers reward coefficient.
        """
        return 0.2

    @property
    def tax_reward_coefficient(self):
        """
        Get tax reward coefficient.
        """
        return 0.1

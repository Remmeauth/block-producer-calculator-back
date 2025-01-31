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
            all_block_producers_stakes: int,
            active_block_producers_votes: int,
            token_price_growth_percent: int = None,
            to_rewards_pool: int = None,
    ):
        """
        Constructor.
        """
        self._money_per_month = money_per_month
        self._token_price = token_price
        self._all_block_producers_stakes = all_block_producers_stakes
        self._active_block_producers_votes = active_block_producers_votes
        self._token_price_growth_percent = token_price_growth_percent
        self._to_rewards_pool = to_rewards_pool

    @property
    def token_price(self):
        """
        Get token price.
        """
        return self._token_price

    @token_price.setter
    def token_price(self, new_token_price):
        """
        Set token price.
        """
        self._token_price = new_token_price

    @property
    def token_price_growth_percent(self):
        """
        Get token price growth percent.
        """
        return self._token_price_growth_percent

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

        The number is 5 184 000. One block is produced in 0.5 seconds (2 blocks per second).
        """
        return 60 * 60 * 24 * 30 * 2

    @property
    def all_block_producers_stakes(self):
        """
        Get all block producers stakes.
        """
        return self._all_block_producers_stakes

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
        return 0.6

    @property
    def active_block_producers_reward_coefficient(self):
        """
        Get an active block producers reward coefficient.
        """
        return 0.3

    @property
    def to_rewards_pool(self):
        """
        Get rewards pool.
        """
        return self._to_rewards_pool

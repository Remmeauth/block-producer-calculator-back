"""
Provide implementation of the returning on investment.
"""
from calculator.domain.block import (
    BlockProducer,
    BlockReward,
)
from calculator.domain.reward import (
    ActiveBlockProducerReward,
    BlockProducerReward,
)
from calculator.domain.economy import Economy


class Roi:
    """
    Implements returning on investment.
    """

    def __init__(self, economy: Economy, block_reward: BlockReward, block_producer: BlockProducer):
        """
        Constructor.
        """
        self.economy = economy
        self.block_reward = block_reward
        self.block_producer = block_producer

    @staticmethod
    def _get_percent_in_tokens(statistics_per_month):
        """
        Get percent of returning on investment in tokens.
        """
        first_month_statistics, *_, last_month_statistics = statistics_per_month

        first_month_block_producer_stake_in_tokens = first_month_statistics.get('block_producer_stake_in_tokens')
        last_month_block_producer_stake_in_tokens = last_month_statistics.get('block_producer_stake_in_tokens') +\
            last_month_statistics.get('month_reward_from_node') + last_month_statistics.get('month_reward_from_pool')

        profit_in_tokens = last_month_block_producer_stake_in_tokens - first_month_block_producer_stake_in_tokens
        roi_percent_in_tokens = profit_in_tokens * 100 / first_month_block_producer_stake_in_tokens

        return roi_percent_in_tokens

    @staticmethod
    def _get_percent_in_fiat(statistics_per_month):
        """
        Get percent of returning on investment in fiat.
        """
        first_month_statistics, *_, last_month_statistics = statistics_per_month

        first_month_block_producer_stake_in_fiat = first_month_statistics.get('block_producer_stake_in_fiat')
        last_month_block_producer_stake_in_fiat = last_month_statistics.get('block_producer_stake_in_fiat') +\
            last_month_statistics.get('month_reward_in_fiat')

        profit_in_fiat = last_month_block_producer_stake_in_fiat - first_month_block_producer_stake_in_fiat
        roi_percent_in_fiat = profit_in_fiat * 100 / first_month_block_producer_stake_in_fiat

        return roi_percent_in_fiat

    def calculate(self, months):
        """
        Calculate returning on investment for 4 years.
        """
        month = 1

        roi = {
            'statistics_per_month': [],
            'percents': {},
        }

        while month != months + 1:

            block_producer_reward = BlockProducerReward(
                economy=self.economy, block_reward=self.block_reward, block_producer=self.block_producer,
            )

            active_block_producer_reward = ActiveBlockProducerReward(
                economy=self.economy, block_reward=self.block_reward, block_producer=self.block_producer,
            )

            reward_from_pool = \
                (block_producer_reward.get_from_pool() + active_block_producer_reward.get_from_pool()) \
                * self.economy.blocks_per_month
            reward_from_node = \
                (block_producer_reward.get() + active_block_producer_reward.get()) * self.economy.blocks_per_month
            month_reward_in_tokens = reward_from_pool + reward_from_node

            roi['statistics_per_month'].append({
                'month': month,
                'block_producer_stake_in_tokens': self.block_producer.stake,
                'block_producer_stake_in_fiat': self.block_producer.stake * self.economy.token_price,
                'month_reward_from_pool': reward_from_pool,
                'month_reward_from_node': reward_from_node,
                'month_reward_in_fiat': month_reward_in_tokens * self.economy.token_price,
                'token_price': self.economy.token_price,
            })

            self.block_producer.stake += month_reward_in_tokens
            self.economy.token_price = self.economy.token_price * (100 + self.economy.token_price_growth_percent) / 100

            month += 1

        statistics_per_month = roi.get('statistics_per_month')

        roi.update({
          'percents': {
              'tokens': self._get_percent_in_tokens(statistics_per_month=statistics_per_month),
              'fiat': self._get_percent_in_fiat(statistics_per_month=statistics_per_month),
          },
        })

        return roi

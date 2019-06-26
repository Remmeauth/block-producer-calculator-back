"""
Provide implementation of the returning on investment.
"""
from calculator.constants import FOUR_YEARS_IN_MONTHS
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

    def calculate(self):
        """
        Calculate returning on investment for 4 years.
        """
        token_percent_growth = 10
        token_percent_growth_decrease_percent = 2

        month = 1

        roi = {
            'statistics_per_month': [],
            'percent': 0,
        }

        while month != FOUR_YEARS_IN_MONTHS + 1:

            block_producer_reward = BlockProducerReward(
                economy=self.economy, block_reward=self.block_reward, block_producer=self.block_producer,
            )

            active_block_producer_reward = ActiveBlockProducerReward(
                economy=self.economy, block_reward=self.block_reward, block_producer=self.block_producer,
            )

            month_reward_in_tokens = \
                (block_producer_reward.get() + active_block_producer_reward.get()) * self.economy.blocks_per_month

            roi['statistics_per_month'].append({
                'month': month,
                'month_reward_in_tokens': month_reward_in_tokens,
                'month_reward_in_fiat': month_reward_in_tokens * self.economy.token_price,
                'token_price': self.economy.token_price,
                'token_price_growth_percent': token_percent_growth,
                'block_producer_stake': self.block_producer.stake,
            })

            self.block_producer.stake += month_reward_in_tokens
            self.economy.token_price = self.economy.token_price * (100 + token_percent_growth) / 100

            month += 1
            token_percent_growth -= (token_percent_growth * token_percent_growth_decrease_percent / 100)

        first_month_statistics, *_, last_month_statistics = roi.get('statistics_per_month')
        first_month_block_producer_stake = first_month_statistics.get('block_producer_stake')
        last_month_block_producer_stake = last_month_statistics.get('block_producer_stake')

        profit = last_month_block_producer_stake - first_month_block_producer_stake
        roi_percent = profit * 100 / first_month_block_producer_stake

        roi.update({
          'percent': roi_percent,
        })

        return roi

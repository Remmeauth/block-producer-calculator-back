from calculator.domain.block_producer import BlockProducer
from calculator.domain.economy import Economy
from calculator.domain.block import BlockCost





def test_block_producers_stakes():

    expected_result = 84_507_042.3

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )

    assert expected_result == economy.block_producers_stakes

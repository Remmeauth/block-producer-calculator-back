"""
Provide tests for block producers.
"""
from calculator.domain.economy import Economy


def test_get_block_producers_stakes():
    """
    Case: get block producers stakes.
    Expect: stakes are returned.
    """
    expected_result = 84_507_042.25352111

    economy = Economy(
        money_per_month=50_000,
        token_price=0.0071,
        active_block_producers_votes=10_000_000,
        active_block_producers_stakes=300_000_000,
    )

    assert expected_result == economy.block_producers_stakes

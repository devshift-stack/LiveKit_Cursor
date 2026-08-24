from amina.policy import (
    contains_croatian_lock_word,
    may_mention_price,
    should_end_after_second_no,
)


def test_language_lock_flags_croatian_words() -> None:
    assert contains_croatian_lock_word("To je vrč za vodu.")
    assert contains_croatian_lock_word("sljedeći tjedan")
    assert not contains_croatian_lock_word("To je bokal za vodu ove sedmice.")


def test_price_only_when_customer_asked() -> None:
    assert may_mention_price("Koliko košta?")
    assert may_mention_price("Koja je cijena?")
    assert not may_mention_price("Recite mi više o bokalu.")


def test_second_clear_no_ends_call() -> None:
    assert not should_end_after_second_no(no_count=1)
    assert should_end_after_second_no(no_count=2)

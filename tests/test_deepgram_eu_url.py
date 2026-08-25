from amina.agent import DEEPGRAM_EU_LISTEN_URL, resolve_deepgram_eu_base_url


def test_defaults_to_eu_listen_url() -> None:
    assert resolve_deepgram_eu_base_url("") == DEEPGRAM_EU_LISTEN_URL
    assert resolve_deepgram_eu_base_url(None) == DEEPGRAM_EU_LISTEN_URL


def test_rejects_us_host() -> None:
    assert resolve_deepgram_eu_base_url("https://api.deepgram.com/v1/listen") == DEEPGRAM_EU_LISTEN_URL


def test_accepts_eu_host_only() -> None:
    assert resolve_deepgram_eu_base_url("https://api.eu.deepgram.com") == DEEPGRAM_EU_LISTEN_URL


def test_accepts_eu_full_url() -> None:
    url = "https://api.eu.deepgram.com/v1/listen"
    assert resolve_deepgram_eu_base_url(url) == url

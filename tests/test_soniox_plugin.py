def test_soniox_plugin_exports_stt_and_tts() -> None:
    from livekit.plugins import soniox

    assert hasattr(soniox, "STT")
    assert hasattr(soniox, "TTS")
    assert hasattr(soniox, "STTOptions")

def test_import() -> None:
    """
    Platzhalter-Smoke-Test.

    Prüft, ob das Paket importiert werden kann.
    """

    import pylactate

    assert pylactate is not None

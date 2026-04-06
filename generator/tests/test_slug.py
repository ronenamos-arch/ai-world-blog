from src.slug import make_slug


def test_hebrew_transliteration():
    result = make_slug("מה זה Claude Projects")
    assert isinstance(result, str)
    assert len(result) > 0
    assert " " not in result
    assert result == result.lower()


def test_mixed_content():
    result = make_slug("10 כלים ל-AI")
    assert "10" in result
    assert " " not in result


def test_latin_passthrough():
    result = make_slug("Claude AI Tools")
    assert result == "claude-ai-tools"


def test_special_chars_stripped():
    result = make_slug("כלי: AI מהפכני!")
    assert ":" not in result
    assert "!" not in result

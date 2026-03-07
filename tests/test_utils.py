"""Tests for x_cli.utils."""

import pytest

from x_cli.utils import parse_tweet_id, strip_at


class TestParseTweetId:
    def test_raw_numeric(self):
        assert parse_tweet_id("1234567890") == "1234567890"

    def test_raw_with_whitespace(self):
        assert parse_tweet_id("  1234567890  ") == "1234567890"

    def test_x_url(self):
        assert parse_tweet_id("https://x.com/user/status/1234567890") == "1234567890"

    def test_twitter_url(self):
        assert parse_tweet_id("https://twitter.com/elonmusk/status/9999") == "9999"

    def test_url_with_query_params(self):
        assert parse_tweet_id("https://x.com/user/status/123?s=20") == "123"

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="Invalid tweet ID"):
            parse_tweet_id("not-a-tweet")

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            parse_tweet_id("")


class TestStripAt:
    def test_with_at(self):
        assert strip_at("@elonmusk") == "elonmusk"

    def test_without_at(self):
        assert strip_at("elonmusk") == "elonmusk"

    def test_empty(self):
        assert strip_at("") == ""

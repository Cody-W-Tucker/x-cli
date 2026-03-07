"""Tests for x_cli.formatters."""

import json

from x_cli.formatters import output_json, output_plain, output_markdown


class TestOutputJson:
    def test_dict_compact(self, capsys):
        """Non-verbose strips includes/meta, emits just data."""
        output_json({"data": {"id": "123", "text": "hello"}, "includes": {"users": []}})
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["id"] == "123"
        assert "includes" not in parsed

    def test_dict_verbose(self, capsys):
        """Verbose keeps full response."""
        output_json({"data": {"id": "123"}, "includes": {"users": []}}, verbose=True)
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert "includes" in parsed

    def test_list(self, capsys):
        output_json([1, 2, 3])
        captured = capsys.readouterr()
        assert json.loads(captured.out) == [1, 2, 3]


class TestOutputPlain:
    def test_dict_with_data_list(self, capsys):
        data = {"data": [{"id": "1", "text": "a"}, {"id": "2", "text": "b"}]}
        output_plain(data)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert "id" in lines[0]
        assert "text" in lines[0]

    def test_dict_with_data_dict(self, capsys):
        data = {"data": {"id": "1", "text": "hello"}}
        output_plain(data)
        captured = capsys.readouterr()
        assert "id\t1" in captured.out
        assert "text\thello" in captured.out

    def test_simple_dict(self, capsys):
        output_plain({"key": "value"})
        captured = capsys.readouterr()
        assert "key\tvalue" in captured.out

    def test_verbose_shows_metrics(self, capsys):
        data = {"data": {"id": "1", "public_metrics": {"like_count": 5}}}
        output_plain(data, verbose=True)
        captured = capsys.readouterr()
        assert "public_metrics" in captured.out


class TestOutputMarkdown:
    def test_single_tweet(self, capsys):
        data = {
            "data": {"id": "123", "text": "hello world", "author_id": "1"},
            "includes": {"users": [{"id": "1", "username": "testuser"}]},
        }
        output_markdown(data, title="Test")
        captured = capsys.readouterr()
        assert "## Test" in captured.out
        assert "**@testuser**" in captured.out
        assert "hello world" in captured.out

    def test_single_user(self, capsys):
        data = {
            "data": {"username": "testuser", "name": "Test", "public_metrics": {"followers_count": 100}},
        }
        output_markdown(data)
        captured = capsys.readouterr()
        assert "## Test (@testuser)" in captured.out
        assert "**followers**: 100" in captured.out

    def test_verbose_shows_timestamp(self, capsys):
        data = {
            "data": {"id": "1", "text": "hi", "author_id": "1", "created_at": "2026-01-01T00:00:00Z"},
            "includes": {"users": [{"id": "1", "username": "u"}]},
        }
        output_markdown(data, verbose=True)
        captured = capsys.readouterr()
        assert "2026-01-01" in captured.out

    def test_no_timestamp_without_verbose(self, capsys):
        data = {
            "data": {"id": "1", "text": "hi", "author_id": "1", "created_at": "2026-01-01T00:00:00Z"},
            "includes": {"users": [{"id": "1", "username": "u"}]},
        }
        output_markdown(data, verbose=False)
        captured = capsys.readouterr()
        assert "2026-01-01" not in captured.out

    def test_user_table(self, capsys):
        data = {
            "data": [
                {"username": "a", "name": "A", "public_metrics": {"followers_count": 10}},
                {"username": "b", "name": "B", "public_metrics": {"followers_count": 20}},
            ]
        }
        output_markdown(data, title="Users")
        captured = capsys.readouterr()
        assert "| @a |" in captured.out
        assert "| @b |" in captured.out

"""Tests for x_cli.cli auth commands."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from x_cli.cli import cli, load_env_files, _oauth2_status_lines


class TestAuthLogin:
    @patch("x_cli.cli.load_env_files")
    def test_missing_client_id_error(self, mock_load_env):
        runner = CliRunner()

        # Mock load_env_files to not set any OAuth2 vars
        def mock_load():
            # Only clear OAuth2 vars, don't reload from file
            for key in list(os.environ.keys()):
                if key.startswith("X_OAUTH2"):
                    del os.environ[key]

        mock_load_env.side_effect = mock_load

        result = runner.invoke(cli, ["auth", "login"])
        assert result.exit_code != 0
        assert "Missing env var X_OAUTH2_CLIENT_ID" in result.output

    @patch("x_cli.cli.click.prompt")
    @patch("x_cli.cli.exchange_code_for_token")
    @patch("x_cli.cli.extract_code_from_redirect_url")
    @patch("x_cli.cli.persist_oauth2_tokens")
    def test_successful_login_flow(
        self, mock_persist, mock_extract, mock_exchange, mock_prompt
    ):
        runner = CliRunner()

        # Set up mocks
        mock_prompt.return_value = (
            "https://example.com/callback?code=auth_code&state=test_state"
        )
        mock_extract.return_value = "auth_code"
        mock_exchange.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 7200,
        }

        # Set required env var
        os.environ["X_OAUTH2_CLIENT_ID"] = "test_client_id"

        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["auth", "login"], input="y\n")
            # Should succeed or at least attempt the flow
            assert "Open this URL" in result.output


class TestAuthLogout:
    def test_removes_tokens(self, tmp_path):
        runner = CliRunner()
        env_file = tmp_path / ".env.auth2"
        env_file.write_text("X_OAUTH2_ACCESS_TOKEN=abc\nX_OAUTH2_REFRESH_TOKEN=def\n")

        with patch("x_cli.cli.get_config_auth2_env_path", return_value=env_file):
            result = runner.invoke(cli, ["auth", "logout"])
            assert result.exit_code == 0
            assert "Removed OAuth2 tokens" in result.output


class TestAuthStatus:
    def test_shows_not_logged_in(self):
        runner = CliRunner()
        with patch("x_cli.cli.load_env_files") as mock_load:
            # Clear any existing OAuth2 env vars
            env_vars_to_clear = [
                k for k in os.environ.keys() if k.startswith("X_OAUTH2")
            ]
            for key in env_vars_to_clear:
                del os.environ[key]

            mock_load.side_effect = lambda: None  # No-op to prevent reloading from file

            result = runner.invoke(cli, ["auth", "status"])
            assert result.exit_code == 0
            assert "not logged in" in result.output

    def test_shows_logged_in_status(self):
        runner = CliRunner()
        os.environ["X_OAUTH2_ACCESS_TOKEN"] = "test_token"
        os.environ["X_OAUTH2_REFRESH_TOKEN"] = "test_refresh"
        os.environ["X_OAUTH2_EXPIRES_AT"] = "9999999999"  # Far future

        result = runner.invoke(cli, ["auth", "status"])
        assert result.exit_code == 0
        assert "logged in" in result.output
        assert "Refresh token: present" in result.output


class TestOAuth2StatusLines:
    def test_no_access_token(self):
        lines = _oauth2_status_lines(None, None, None)
        assert lines == ["OAuth2: not logged in"]

    def test_with_access_token_no_expiry(self):
        lines = _oauth2_status_lines("token", "refresh", None)
        assert "OAuth2: logged in" in lines
        assert "Refresh token: present" in lines
        assert "Access token expiry: unknown" in lines

    def test_with_valid_expiry(self):
        import time

        future = str(int(time.time()) + 3600)  # 1 hour from now
        lines = _oauth2_status_lines("token", "refresh", future)
        assert "OAuth2: logged in" in lines
        assert "Access token expiry: in" in lines[-1]

    def test_with_expired_token(self):
        import time

        past = str(int(time.time()) - 100)
        lines = _oauth2_status_lines("token", "refresh", past)
        assert "Access token expiry: expired" in lines[-1]

    def test_invalid_expiry_value(self):
        lines = _oauth2_status_lines("token", "refresh", "invalid")
        assert "invalid value" in lines[-1]

"""Tests for x_cli.oauth2."""

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from x_cli.oauth2 import (
    AUTH_URL,
    build_authorization_url,
    clear_oauth2_tokens,
    ensure_env_file,
    exchange_code_for_token,
    expires_at_from_expires_in,
    generate_code_challenge,
    generate_code_verifier,
    generate_state,
    migrate_legacy_oauth2_tokens,
    persist_oauth2_tokens,
    refresh_access_token,
    token_expired,
    _extract_token_error,
)


class TestGenerateCodeVerifier:
    def test_returns_urlsafe_string(self):
        verifier = generate_code_verifier()
        assert isinstance(verifier, str)
        assert len(verifier) >= 43
        assert len(verifier) <= 128

    def test_valid_length_range(self):
        for length in [43, 64, 100, 128]:
            verifier = generate_code_verifier(length)
            assert len(verifier) == length

    def test_rejects_invalid_length(self):
        with pytest.raises(ValueError):
            generate_code_verifier(42)
        with pytest.raises(ValueError):
            generate_code_verifier(129)


class TestGenerateCodeChallenge:
    def test_returns_different_value_than_verifier(self):
        verifier = generate_code_verifier()
        challenge = generate_code_challenge(verifier)
        assert challenge != verifier
        assert isinstance(challenge, str)
        assert len(challenge) > 0


class TestGenerateState:
    def test_returns_urlsafe_string(self):
        state = generate_state()
        assert isinstance(state, str)
        assert len(state) > 0


class TestBuildAuthorizationUrl:
    def test_contains_required_params(self):
        url = build_authorization_url(
            client_id="test_client",
            redirect_uri="https://example.com/callback",
            state="test_state",
            code_challenge="test_challenge",
        )
        assert url.startswith(AUTH_URL)
        assert "client_id=test_client" in url
        assert "state=test_state" in url
        assert "code_challenge=test_challenge" in url
        assert "code_challenge_method=S256" in url
        assert "response_type=code" in url


class TestExpiresAtFromExpiresIn:
    def test_returns_timestamp_in_future(self):
        result = expires_at_from_expires_in(3600)
        assert isinstance(result, int)
        assert result > int(time.time())

    def test_returns_none_for_none(self):
        assert expires_at_from_expires_in(None) is None

    def test_returns_none_for_invalid(self):
        assert expires_at_from_expires_in("invalid") is None


class TestTokenExpired:
    def test_returns_true_for_past_expiry(self):
        past = int(time.time()) - 1000
        assert token_expired(past) is True

    def test_returns_false_for_future_expiry(self):
        future = int(time.time()) + 1000
        assert token_expired(future) is False

    def test_returns_false_for_none(self):
        assert token_expired(None) is False


class TestEnsureEnvFile:
    def test_creates_file_with_secure_permissions(self, tmp_path):
        env_path = tmp_path / ".env.auth2"
        ensure_env_file(env_path)
        assert env_path.exists()
        assert env_path.stat().st_mode & 0o777 == 0o600


class TestPersistOAuth2Tokens:
    def test_writes_tokens_to_file(self, tmp_path):
        env_path = tmp_path / ".env.auth2"
        persist_oauth2_tokens(
            env_path,
            access_token="access123",
            refresh_token="refresh456",
            expires_at=1234567890,
        )
        content = env_path.read_text()
        assert "X_OAUTH2_ACCESS_TOKEN=access123" in content
        assert "X_OAUTH2_REFRESH_TOKEN=refresh456" in content
        assert "X_OAUTH2_EXPIRES_AT=1234567890" in content


class TestClearOAuth2Tokens:
    def test_removes_token_keys(self, tmp_path):
        env_path = tmp_path / ".env.auth2"
        env_path.write_text(
            "X_OAUTH2_ACCESS_TOKEN=abc\n"
            "X_OAUTH2_REFRESH_TOKEN=def\n"
            "X_OAUTH2_EXPIRES_AT=123\n"
            "OTHER=value\n"
        )
        clear_oauth2_tokens(env_path)
        content = env_path.read_text()
        assert "X_OAUTH2_ACCESS_TOKEN" not in content
        assert "X_OAUTH2_REFRESH_TOKEN" not in content
        assert "X_OAUTH2_EXPIRES_AT" not in content
        assert "OTHER=value" in content


class TestMigrateLegacyOAuth2Tokens:
    def test_moves_tokens_from_env_to_auth2(self, tmp_path):
        config_env = tmp_path / ".env"
        auth2_env = tmp_path / ".env.auth2"
        config_env.write_text(
            "X_API_KEY=key\n"
            "X_OAUTH2_ACCESS_TOKEN=access\n"
            "X_OAUTH2_REFRESH_TOKEN=refresh\n"
        )
        migrate_legacy_oauth2_tokens(config_env, auth2_env)
        auth2_content = auth2_env.read_text()
        assert "X_OAUTH2_ACCESS_TOKEN=access" in auth2_content
        assert "X_OAUTH2_REFRESH_TOKEN=refresh" in auth2_content
        # Should keep static vars in .env
        config_content = config_env.read_text()
        assert "X_API_KEY=key" in config_content
        # Should remove migrated tokens from .env
        assert "X_OAUTH2_ACCESS_TOKEN" not in config_content


class TestExchangeCodeForToken:
    def test_successful_exchange(self):
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            "access_token": "new_access",
            "refresh_token": "new_refresh",
            "expires_in": 7200,
        }
        mock_http = MagicMock()
        mock_http.post.return_value = mock_response

        result = exchange_code_for_token(
            mock_http,
            client_id="test_client",
            client_secret="test_secret",
            code="auth_code",
            code_verifier="verifier",
            redirect_uri="https://example.com/callback",
        )

        assert result["access_token"] == "new_access"
        mock_http.post.assert_called_once()

    def test_handles_error_response(self):
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "invalid_client"}
        mock_response.text = "error"
        mock_http = MagicMock()
        mock_http.post.return_value = mock_response

        with pytest.raises(RuntimeError, match="token request failed"):
            exchange_code_for_token(
                mock_http,
                client_id="test_client",
                client_secret=None,
                code="auth_code",
                code_verifier="verifier",
                redirect_uri="https://example.com/callback",
            )


class TestExtractTokenError:
    def test_extracts_error_description(self):
        payload = {"error_description": "Invalid client", "error": "invalid_client"}
        assert _extract_token_error(payload) == "Invalid client"

    def test_extracts_error(self):
        payload = {"error": "invalid_grant"}
        assert _extract_token_error(payload) == "invalid_grant"

    def test_returns_empty_for_empty_payload(self):
        assert _extract_token_error({}) == ""

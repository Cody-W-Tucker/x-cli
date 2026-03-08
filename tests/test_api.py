"""Tests for x_cli.api auth routing and error handling."""

import httpx
import pytest

from x_cli.api import XApiClient
from x_cli.auth import Credentials


@pytest.fixture
def client():
    creds = Credentials(
        api_key="test_key",
        api_secret="test_secret",
        access_token="test_token",
        access_token_secret="test_token_secret",
        bearer_token="test_bearer",
    )
    c = XApiClient(creds)
    yield c
    c.close()


def _set_transport(client: XApiClient, handler) -> None:
    client._http.close()
    client._http = httpx.Client(transport=httpx.MockTransport(handler))


def test_bookmarks_require_oauth2_login(client):
    with pytest.raises(RuntimeError, match="Missing OAuth2 user token"):
        client.get_bookmarks()


def test_bookmarks_use_oauth2_bearer_token(client):
    client.creds.oauth2_access_token = "oauth2_user_token"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer oauth2_user_token"
        if request.url.path == "/2/users/me":
            return httpx.Response(200, request=request, json={"data": {"id": "42"}})
        if request.url.path == "/2/users/42/bookmarks":
            return httpx.Response(200, request=request, json={"data": []})
        return httpx.Response(404, request=request)

    _set_transport(client, handler)
    result = client.get_bookmarks()
    assert "data" in result


def test_bookmarks_refresh_on_401(client):
    client.creds.oauth2_access_token = "expired_token"
    client.creds.oauth2_refresh_token = "refresh_token"
    client.creds.oauth2_client_id = "client_id"
    client.creds.oauth2_expires_at = 1

    request_count = {"value": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        request_count["value"] += 1
        if request.url.path == "/2/oauth2/token":
            return httpx.Response(
                200,
                request=request,
                json={
                    "access_token": "new_token",
                    "refresh_token": "new_refresh",
                    "expires_in": 7200,
                },
            )
        if request.url.path == "/2/users/me":
            auth = request.headers.get("Authorization", "")
            if "new_token" in auth:
                return httpx.Response(200, request=request, json={"data": {"id": "42"}})
            return httpx.Response(401, request=request)
        if request.url.path == "/2/users/42/bookmarks":
            auth = request.headers.get("Authorization", "")
            if "new_token" in auth:
                return httpx.Response(200, request=request, json={"data": []})
            return httpx.Response(401, request=request)
        return httpx.Response(404, request=request)

    _set_transport(client, handler)
    result = client.get_bookmarks()
    assert "data" in result
    assert request_count["value"] >= 2  # At least refresh token + retry


def test_bookmarks_error_on_app_only_token(client):
    client.creds.oauth2_access_token = "app_only_token"

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/2/users/me":
            return httpx.Response(200, request=request, json={"data": {"id": "42"}})
        if request.url.path == "/2/users/42/bookmarks":
            return httpx.Response(
                403,
                request=request,
                json={
                    "detail": "OAuth 2.0 Application-Only authentication is not permitted"
                },
            )
        return httpx.Response(404, request=request)

    _set_transport(client, handler)
    with pytest.raises(RuntimeError, match="not a user-context token"):
        client.get_bookmarks()


def test_oauth2_request_extracts_errors(client):
    client.creds.oauth2_access_token = "valid_token"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            request=request,
            json={"error": "invalid_request", "error_description": "Missing parameter"},
        )

    _set_transport(client, handler)
    with pytest.raises(RuntimeError, match="API error"):
        client._oauth2_user_request("GET", "https://api.x.com/2/test")


def test_extract_error_message_from_errors_array(client):
    data = {"errors": [{"detail": "Not found"}, {"message": "Bad request"}]}
    msg = client._extract_error_message(None, data)
    assert "Not found" in msg
    assert "Bad request" in msg


def test_extract_error_message_from_detail(client):
    data = {"detail": "Specific error"}
    msg = client._extract_error_message(None, data)
    assert msg == "Specific error"


def test_extract_error_message_from_title(client):
    data = {"title": "Error title"}
    msg = client._extract_error_message(None, data)
    assert msg == "Error title"


def test_extract_error_message_fallback_to_text(client):
    mock_response = type("obj", (object,), {"text": "Error text"})()
    msg = client._extract_error_message(mock_response, {})
    assert msg == "Error text"

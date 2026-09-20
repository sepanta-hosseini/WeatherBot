import pytest
import requests
from weather_app.api import make_request
from weather_app.exceptions import APIError


def test_make_request_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout()
    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(APIError, match="timed out"):
        make_request("https://example.com")


def test_make_request_connection_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError()
    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(APIError, match="Could not connect"):
        make_request("https://example.com")

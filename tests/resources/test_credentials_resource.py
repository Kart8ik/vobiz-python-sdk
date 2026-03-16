import json

import vobiz


def _capture(monkeypatch):
    captured = {}

    def capture_send(self, request, **kwargs):
        captured["request"] = request
        from requests import Response

        resp = Response()
        resp.status_code = 200
        resp._content = b"{}"
        resp.headers["Content-Type"] = "application/json"
        return resp

    monkeypatch.setattr("requests.sessions.Session.send", capture_send, raising=True)
    return captured


def test_create_credential(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.credentials.create(
        username="user1",
        password="secret",
        trunk_id="TRUNK_ID",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/credentials/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["username"] == "user1"
    assert body["password"] == "secret"
    assert body["trunk_id"] == "TRUNK_ID"


def test_list_credentials(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.credentials.list(page=2, size=50, trunk_id="TRUNK_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/credentials/"
    )
    assert "page=2" in (req.url or "")
    assert "size=50" in (req.url or "")
    assert "trunk_id=TRUNK_ID" in (req.url or "")


def test_get_credential(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.credentials.get("CRED_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/credentials/CRED_ID"
    )


def test_update_credential(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.credentials.update("CRED_ID", password="newpass")

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/credentials/CRED_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["password"] == "newpass"


def test_delete_credential(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.credentials.delete("CRED_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/credentials/CRED_ID"
    )


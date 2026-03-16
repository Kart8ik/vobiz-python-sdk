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


def test_create_origination_uri(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.origination_uris.create(
        uri="sip:carrier@example.com",
        trunk_id="TRUNK_ID",
        weight=10,
        priority=1,
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/origination-uris/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["uri"] == "sip:carrier@example.com"
    assert body["trunk_id"] == "TRUNK_ID"
    assert body["weight"] == 10
    assert body["priority"] == 1


def test_list_origination_uris(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.origination_uris.list(page=3, size=25, trunk_id="TRUNK_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/origination-uris/"
    )
    assert "page=3" in (req.url or "")
    assert "size=25" in (req.url or "")
    assert "trunk_id=TRUNK_ID" in (req.url or "")


def test_get_origination_uri(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.origination_uris.get("URI_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/origination-uris/URI_ID"
    )


def test_update_origination_uri(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.origination_uris.update("URI_ID", weight=20)

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/origination-uris/URI_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["weight"] == 20


def test_delete_origination_uri(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.origination_uris.delete("URI_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/origination-uris/URI_ID"
    )


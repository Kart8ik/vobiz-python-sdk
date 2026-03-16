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


def test_create_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.create(
        name="Office IPs",
        description="Corporate offices",
        ip_addresses=["203.0.113.1/32", "203.0.113.2/32"],
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/ip-access-control-lists/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "Office IPs"
    assert body["description"] == "Corporate offices"
    assert body["ip_addresses"] == ["203.0.113.1/32", "203.0.113.2/32"]


def test_list_ip_acls(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.list(page=1, size=10)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/ip-access-control-lists/"
    )
    assert "page=1" in (req.url or "")
    assert "size=10" in (req.url or "")


def test_get_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.get("ACL_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/ip-access-control-lists/ACL_ID"
    )


def test_update_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.update("ACL_ID", name="Updated Name")

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/ip-access-control-lists/ACL_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "Updated Name"


def test_delete_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.delete("ACL_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/ip-access-control-lists/ACL_ID"
    )


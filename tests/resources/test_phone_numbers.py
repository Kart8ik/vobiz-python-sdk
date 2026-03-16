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


def test_search_phone_numbers(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.search(
        country="US",
        type="local",
        pattern="415",
        region="CA",
        page=2,
        size=50,
    )

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/search"
    )
    assert "country=US" in (req.url or "")
    assert "type=local" in (req.url or "")
    assert "pattern=415" in (req.url or "")
    assert "region=CA" in (req.url or "")
    assert "page=2" in (req.url or "")
    assert "size=50" in (req.url or "")


def test_buy_phone_number(monkeypatch):
    import json

    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.buy(
        phone_number="+14155550100",
        application_id="APP_ID",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["phone_number"] == "+14155550100"
    assert body["application_id"] == "APP_ID"


def test_list_phone_numbers(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.list(page=1, size=20, application_id="APP_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/"
    )
    assert "page=1" in (req.url or "")
    assert "size=20" in (req.url or "")
    assert "application_id=APP_ID" in (req.url or "")


def test_get_phone_number(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.get("PN_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/PN_ID"
    )


def test_update_phone_number(monkeypatch):
    import json

    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.update("PN_ID", application_id="NEW_APP")

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/PN_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["application_id"] == "NEW_APP"


def test_delete_phone_number(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.delete("PN_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/phone-numbers/PN_ID"
    )


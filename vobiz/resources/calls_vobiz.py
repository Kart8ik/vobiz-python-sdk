from typing import Any, Dict, Optional


class Calls:
    """
    Vobiz Calls resource.

    Uses the `/api/v1/account/{auth_id}/call/` endpoints for call control and
    live/queued status listing, plus DTMF.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        return self.client.auth_id

    def create(self, from_: str, to_: str, answer_url: str, **params: Any):
        """
        POST /api/v1/Account/{auth_id}/Call/
        """
        body: Dict[str, Any] = {
            "from": from_,
            "to": to_,
            "answer_url": answer_url,
        }
        body.update(params)
        return self.client.request("POST", ("Call",), data=body)

    def transfer(self, call_uuid: str, **params: Any):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        return self.client.request("POST", ("Call", call_uuid), data=dict(params))

    def hangup(self, call_uuid: str):
        """
        DELETE /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        return self.client.request("DELETE", ("Call", call_uuid))

    def list(self, status: Optional[str] = None, **filters: Any):
        """
        GET /api/v1/Account/{auth_id}/Call/
        """
        params: Dict[str, Any] = dict(filters)
        if status is not None:
            params["status"] = status
        return self.client.request(
            "GET",
            ("Call",),
            data=params,
        )

    def get(self, call_uuid: str, status: Optional[str] = None):
        """
        GET /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        return self.client.request("GET", ("Call", call_uuid), data=params)

    def list_live(self):
        return self.list(status="live")

    def list_queued(self):
        return self.list(status="queued")

    def get_live(self, call_uuid: str):
        return self.get(call_uuid, status="live")

    def get_queued(self, call_uuid: str):
        return self.get(call_uuid, status="queued")

    def send_digits(self, call_uuid: str, digits: str, leg: str):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/DTMF/
        """
        body: Dict[str, Any] = {"digits": digits, "leg": leg}
        return self.client.request("POST", ("Call", call_uuid, "DTMF"), data=body)


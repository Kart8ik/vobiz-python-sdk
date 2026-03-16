from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class SipTrunks:
    """
    Vobiz SIP Trunks resource.

    All endpoints are scoped to the authenticated account.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def create(
        self,
        name: str,
        inbound_uri: Optional[str] = None,
        outbound_uri: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/accounts/{account_id}/sip-trunks/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sip-trunks/"
        body: Dict[str, Any] = {"name": name}
        if inbound_uri is not None:
            body["inbound_uri"] = inbound_uri
        if outbound_uri is not None:
            body["outbound_uri"] = outbound_uri
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/accounts/{account_id}/sip-trunks/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sip-trunks/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, trunk_id: str):
        """
        GET /api/v1/accounts/{account_id}/sip-trunks/{trunk_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sip-trunks/{trunk_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, trunk_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/sip-trunks/{trunk_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sip-trunks/{trunk_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, trunk_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/sip-trunks/{trunk_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sip-trunks/{trunk_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)


from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class Credentials:
    """
    Vobiz SIP Credentials resource.

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
        username: str,
        password: str,
        trunk_id: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/accounts/{account_id}/credentials/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/credentials/"
        body: Dict[str, Any] = {
            "username": username,
            "password": password,
        }
        if trunk_id is not None:
            body["trunk_id"] = trunk_id
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        trunk_id: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/accounts/{account_id}/credentials/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/credentials/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if trunk_id is not None:
            params["trunk_id"] = trunk_id
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, credential_id: str):
        """
        GET /api/v1/accounts/{account_id}/credentials/{credential_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/credentials/{credential_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, credential_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/credentials/{credential_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/credentials/{credential_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, credential_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/credentials/{credential_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/credentials/{credential_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)


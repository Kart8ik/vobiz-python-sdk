from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class IpAccessControlLists:
    """
    Vobiz IP Access Control Lists resource.

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
        description: Optional[str] = None,
        ip_addresses: Optional[list[str]] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/accounts/{account_id}/ip-access-control-lists/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/ip-access-control-lists/"
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if ip_addresses is not None:
            body["ip_addresses"] = ip_addresses
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
        GET /api/v1/accounts/{account_id}/ip-access-control-lists/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/ip-access-control-lists/"
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

    def get(self, acl_id: str):
        """
        GET /api/v1/accounts/{account_id}/ip-access-control-lists/{acl_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/ip-access-control-lists/{acl_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, acl_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/ip-access-control-lists/{acl_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/ip-access-control-lists/{acl_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, acl_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/ip-access-control-lists/{acl_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/ip-access-control-lists/{acl_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)


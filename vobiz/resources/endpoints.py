from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class Endpoints:
    """
    Vobiz Endpoints (SIP endpoints / devices) resource.

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
        alias: Optional[str] = None,
        application_id: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/accounts/{account_id}/endpoints/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/endpoints/"
        body: Dict[str, Any] = {
            "username": username,
            "password": password,
        }
        if alias is not None:
            body["alias"] = alias
        if application_id is not None:
            body["application_id"] = application_id
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        application_id: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/accounts/{account_id}/endpoints/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/endpoints/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if application_id is not None:
            params["application_id"] = application_id
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, endpoint_id: str):
        """
        GET /api/v1/accounts/{account_id}/endpoints/{endpoint_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/endpoints/{endpoint_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, endpoint_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/endpoints/{endpoint_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/endpoints/{endpoint_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, endpoint_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/endpoints/{endpoint_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/endpoints/{endpoint_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

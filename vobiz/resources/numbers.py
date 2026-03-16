from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class PhoneNumbers:
    """
    Vobiz Phone Numbers resource.

    All endpoints are scoped to the authenticated account.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def search(
        self,
        country: str,
        type: Optional[str] = None,
        pattern: Optional[str] = None,
        region: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/accounts/{account_id}/phone-numbers/search
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/search"
        params: Dict[str, Any] = {"country": country}
        if type is not None:
            params["type"] = type
        if pattern is not None:
            params["pattern"] = pattern
        if region is not None:
            params["region"] = region
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def buy(self, phone_number: str, application_id: Optional[str] = None, **extra: Any):
        """
        POST /api/v1/accounts/{account_id}/phone-numbers/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/"
        body: Dict[str, Any] = {"phone_number": phone_number}
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
        GET /api/v1/accounts/{account_id}/phone-numbers/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/"
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

    def get(self, phone_number_id: str):
        """
        GET /api/v1/accounts/{account_id}/phone-numbers/{phone_number_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/{phone_number_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, phone_number_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/phone-numbers/{phone_number_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/{phone_number_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, phone_number_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/phone-numbers/{phone_number_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/phone-numbers/{phone_number_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

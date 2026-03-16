from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class CDRs:
    """
    Vobiz Call Detail Records (CDRs) resource.

    All endpoints are scoped to the authenticated account.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None,
        direction: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/accounts/{account_id}/cdrs/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/cdrs/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if from_number is not None:
            params["from"] = from_number
        if to_number is not None:
            params["to"] = to_number
        if direction is not None:
            params["direction"] = direction
        # allow arbitrary extra server-side filters
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, cdr_id: str):
        """
        GET /api/v1/accounts/{account_id}/cdrs/{cdr_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/cdrs/{cdr_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)


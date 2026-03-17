from typing import Any, Dict, Optional


class Recordings:
    """
    Vobiz Recordings resource.

    Endpoint: https://api.vobiz.ai/api/v1/Account/{auth_id}/Recording/
    """

    def __init__(self, client):
        self.client = client

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        call_uuid: Optional[str] = None,
        recording_type: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/Account/{auth_id}/Recording/
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if call_uuid is not None:
            params["call_uuid"] = call_uuid
        if recording_type is not None:
            params["recording_type"] = recording_type
        params.update(filters)

        return self.client.request("GET", ("Recording",), data=params)

    def get(self, recording_id: str):
        """
        GET /api/v1/Account/{auth_id}/Recording/{recording_id}/
        """
        return self.client.request("GET", ("Recording", recording_id))

    def delete(self, recording_id: str):
        """
        DELETE /api/v1/Account/{auth_id}/Recording/{recording_id}/
        """
        return self.client.request("DELETE", ("Recording", recording_id))

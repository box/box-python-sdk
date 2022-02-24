from datetime import datetime
from typing import Optional

from boxsdk.auth.server_auth import ServerAuth


class CCGAuth(ServerAuth):
    _GRANT_TYPE = 'client_credentials'

    def _fetch_access_token(self, sub: str, sub_type: str, now_time: Optional[datetime] = None) -> str:
        data = {
            'grant_type': self._GRANT_TYPE,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'box_subject_id': sub,
            'box_subject_type': sub_type,
        }

        return self.send_token_request(data, access_token=None, expect_refresh_token=False)[0]

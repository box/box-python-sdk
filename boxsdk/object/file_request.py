import json
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from boxsdk.util.datetime_formatter import normalize_date_to_rfc3339_format
from boxsdk.util.text_enum import TextEnum

from ..util.api_call_decorator import api_call
from .base_object import BaseObject

if TYPE_CHECKING:
    from boxsdk.object.folder import Folder


class StatusState(TextEnum):
    """An enum of possible status states"""
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class FileRequest(BaseObject):
    """Represents the file request."""
    _item_type = 'file_request'

    @api_call
    def copy(
            self,
            *,
            description: Optional[str] = None,
            expire_time: Union[datetime, str] = None,
            folder: 'Folder' = None,
            require_description: Optional[bool] = None,
            require_email: Optional[bool] = None,
            status: Optional[str] = None,
            title: Optional[str] = None,
            **_kwargs
    ) -> 'FileRequest':
        # pylint: disable=arguments-differ
        """Copy an existing file request already present on one folder, and applies it to another folder.

        :param description:
            A new description for the file request.
        :param title:
            A new title for the file request.
        :param expire_time:
            A expiration time which after no longer allows the file request to be submitted.
        :param folder:
            The folder to which the file request will be saved.
        :param require_description:
            A flag indicating whether the file submitted must have a description.
        :param require_email:
            A flag indicating whether the file submitted must have sender email.
        :param status:
            The status of the file request.
        :returns:
            The copy of the file
        """
        # pylint: disable=arguments-differ
        url = self.get_url('copy')
        data = {
            'folder': {'id': folder.object_id, 'type': 'folder'},
        }
        if description is not None:
            data['description'] = description
        if title is not None:
            data['title'] = title
        if expire_time is not None:
            data['expires_at'] = normalize_date_to_rfc3339_format(expire_time)
        if require_description is not None:
            data['is_description_required'] = require_description
        if require_email is not None:
            data['is_email_required'] = require_email
        if status is not None:
            data['status'] = status
        print(data)
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

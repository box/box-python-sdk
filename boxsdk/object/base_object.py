# coding: utf-8

import json
from typing import TYPE_CHECKING, Any, Iterable, Optional, Union, List

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.session.session import Session


class BaseObject(BaseEndpoint, BaseAPIJSONObject):
    """A Box API endpoint for interacting with a Box object."""

    def __init__(self, session: 'Session', object_id: str, response_object: dict = None):
        """
        :param session:
            The Box session used to make requests.
        :param object_id:
            The Box ID for the object.
        :param response_object:
            A JSON object representing the object returned from a Box API request.
        """
        super().__init__(session=session, response_object=response_object)
        self._object_id = object_id

    @property
    def _description(self) -> str:
        """
        Base class override.  Return a description for the object.
        """
        if 'name' in self._response_object:
            return f'{self._object_id} ({self.name})'  # pylint:disable=no-member
        return self._object_id

    def get_url(self, *args: Any) -> str:
        """
        Base class override.
        Return the given object's URL, appending any optional parts as specified by args.
        """
        return super().get_url(f'{self._item_type}s', self._object_id, *args)

    def get_type_url(self) -> str:
        """
        Return the URL for type of the given resource.
        """
        return super().get_url(f'{self._item_type}s')

    @property
    def object_id(self) -> str:
        """
        Return the Box ID for the object.
        """
        return self._object_id

    @api_call
    def get(self, *, fields: Iterable[str] = None, headers: dict = None, **_kwargs) -> Any:
        """
        Get information about the object, specified by fields. If fields is None, return the default fields.

        :param fields:
            List of fields to request.
        :param headers:
            Additional headers to send with the request.
        :return:
            An object of the same type that has the requested information.
        """
        url = self.get_url()
        params = {'fields': ','.join(fields)} if fields else None
        box_response = self._session.get(url, params=params, headers=headers)
        return self.translator.translate(
            session=self._session,
            response_object=box_response.json(),
        )

    @api_call
    def update_info(
            self,
            *,
            data: Union[dict, List[dict]],
            params: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs: Any
    ) -> Any:
        """Update information about this object.

        Send a PUT to the object's base endpoint to modify the provided
        attributes.

        :param data:
            The updated information about this object.
            Must be JSON serializable.
            Update the object attributes in data.keys(). The semantics of the
            values depends on the the type and attributes of the object being
            updated. For details on particular semantics, refer to the Box
            developer API documentation <https://developer.box.com/>.
        :param params:
            (optional) Query string parameters for the request.
        :param headers:
            (optional) Extra HTTP headers for the request.
        :param kwargs:
            Optional arguments that ``put`` takes.
        :return:
            The updated object.
            Return a new object of the same type, without modifying the
            original object passed as self.
            Construct the new object with all the default attributes that are
            returned from the endpoint.
        """
        url = self.get_url()
        box_response = self._session.put(url, data=json.dumps(data), params=params, headers=headers, **kwargs)
        if 'expect_json_response' in kwargs and not kwargs['expect_json_response']:
            return box_response.ok

        return self.translator.translate(
            session=self._session,
            response_object=box_response.json(),
        )

    @api_call
    def delete(self, *, params: Optional[dict] = None, headers: Optional[dict] = None, **_kwargs) -> bool:
        """ Delete the object.

        :param params:
            Additional parameters to send with the request. Can be None
        :param headers:
            Any customer headers to send with the request. Can be None
        :returns:
            Whether or not the delete was successful.
        :raises:
            :class:`BoxAPIException` in case of unexpected errors.
        """
        url = self.get_url()

        box_response = self._session.delete(url, expect_json_response=False, params=params or {}, headers=headers)
        return box_response.ok

    def __eq__(self, other: Any) -> bool:
        """Equality as determined by object id and type"""
        if isinstance(other, BaseObject):
            # Two objects are considered the same if they have the same address in the API
            return self.get_url() == other.get_url()

        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        """Equality as determined by object id and type"""
        return not self == other

    def __hash__(self) -> int:
        return hash((self._object_id, self._item_type))

    def clone(self, session: 'Session' = None) -> 'BaseObject':
        """Base class override."""
        return self.__class__(
            session or self._session,
            self._object_id,
            self._response_object,
        )

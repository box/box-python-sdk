# coding: utf-8

import json
from typing import TYPE_CHECKING, Optional, Iterable, Any, Union

from boxsdk.util.text_enum import TextEnum
from .base_item import BaseItem
from ..exception import BoxAPIException
from .metadata import Metadata
from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET
from ..pagination.marker_based_dict_collection import MarkerBasedDictCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection

if TYPE_CHECKING:
    from boxsdk.object.watermark import Watermark
    from boxsdk.object.group import Group
    from boxsdk.object.user import User
    from boxsdk.object.collaboration import Collaboration
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class ClassificationType(TextEnum):
    """An enum of possible classification types"""
    PUBLIC = 'Public'
    INTERNAL = 'Internal'
    CONFIDENTIAL = 'Confidential'
    NONE = 'None'


class Item(BaseItem):
    """Box API endpoint for interacting with files and folders."""

    _classification_template_key = 'securityClassification-6VMVochwUWo'

    def _get_accelerator_upload_url(self, file_id: Optional[str] = None) -> Optional[str]:
        """
        Make an API call to get the Accelerator upload url for either upload a new file or updating an existing file.

        :param file_id:
            Box id of the file to be uploaded. Not required for new file uploads.
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        """
        if file_id:
            self.validate_item_id(file_id)
        endpoint = f'{file_id}/content' if file_id else 'content'
        url = f'{self._session.api_config.BASE_API_URL}/files/{endpoint}'
        try:
            response_json = self._session.options(
                url=url,
                expect_json_response=True,
            ).json()
            return response_json.get('upload_url', None)
        except BoxAPIException:
            return None

    def _preflight_check(
            self, size: int,
            name: str = None,
            file_id: str = None,
            parent_id: str = None
    ) -> Optional[str]:
        """
        Make an API call to check if certain file can be uploaded to Box or not.
        (https://developer.box.com/en/guides/uploads/check/)

        Returns an accelerator URL if available, which comes for free in the response.

        :param size:
            The size of the file to be uploaded in bytes. Specify 0 for unknown file sizes.
        :param name:
            The name of the file to be uploaded. This is optional if `file_id` is specified,
            but required for new file uploads.
        :param file_id:
            Box id of the file to be uploaded. Not required for new file uploads.
        :param parent_id:
            The ID of the parent folder. Required only for new file uploads.
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        if file_id:
            self.validate_item_id(file_id)
        endpoint = f'{file_id}/content' if file_id else 'content'
        url = f'{self._session.api_config.BASE_API_URL}/files/{endpoint}'
        data = {'size': size}
        if name:
            data['name'] = name
        if parent_id:
            data['parent'] = {'id': parent_id}

        response_json = self._session.options(
            url=url,
            expect_json_response=True,
            data=json.dumps(data),
        ).json()
        return response_json.get('upload_url', None)

    @api_call
    def update_info(self, *, data: dict, etag: Optional[str] = None, **kwargs: Any) -> 'Item':
        """
        Baseclass override.
        :param data:
            The updated information about this object.
            Must be JSON serializable.
            Update the object attributes in data.keys(). The semantics of the
            values depends on the the type and attributes of the object being
            updated. For details on particular semantics, refer to the Box
            developer API documentation <https://developer.box.com/>.
        :param etag:
            If specified, instruct the Box API to perform the update only if
            the current version's etag matches.
        :return:
            The updated object.
            Return a new object of the same type, without modifying the original object passed as self.
            Construct the new object with all the default attributes that are returned from the endpoint.
        """
        # pylint:disable=arguments-differ
        self.validate_item_id(self._object_id)
        headers = {'If-Match': etag} if etag is not None else None
        return super().update_info(data=data, headers=headers, **kwargs)

    @api_call
    def get(self, *, fields: Iterable[str] = None, etag: Optional[str] = None, **kwargs) -> 'Item':
        """
        Base class override.

        :param fields:
            List of fields to request.
        :param etag:
            If specified, instruct the Box API to get the info only if the current version's etag doesn't match.
        :returns:
            Information about the file or folder.
        :raises: :class:`BoxAPIException` if the specified etag matches the latest version of the item.
        """
        # pylint:disable=arguments-differ,arguments-renamed
        self.validate_item_id(self._object_id)
        headers = {'If-None-Match': etag} if etag is not None else None
        return super().get(fields=fields, headers=headers, **kwargs)

    @api_call
    def create_shared_link(
            self,
            *,
            access: Optional[str] = None,
            etag: Optional[str] = None,
            unshared_at: Optional[str] = SDK_VALUE_NOT_SET,
            allow_download: Optional[bool] = None,
            allow_preview: Optional[bool] = None,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> 'Item':
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.  Takes an RFC3339-formatted string, e.g.
            '2018-10-31T23:59:59-07:00' for 11:59:59 PM on October 31, 2018 in the America/Los_Angeles timezone.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :param allow_download:
            Whether or not the item being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param allow_preview:
            Whether or not the item being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :return:
            The updated object with shared link.
            Returns a new object of the same type, without modifying the original object passed as self.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        # pylint:disable=arguments-differ
        return super().create_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_download=allow_download,
            allow_preview=allow_preview,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def get_shared_link(
            self,
            *,
            access: Optional[str] = None,
            etag: Optional[str] = None,
            unshared_at: Optional[str] = SDK_VALUE_NOT_SET,
            allow_download: Optional[bool] = None,
            allow_preview: Optional[bool] = None,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> 'str':
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.
        :param allow_download:
            Whether or not the item being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param allow_preview:
            Whether or not the item being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :returns:
            The URL of the shared link.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        # pylint:disable=arguments-differ
        return super().get_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_download=allow_download,
            allow_preview=allow_preview,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def remove_shared_link(self, *, etag: Optional[str] = None, **kwargs: Any) -> bool:
        """
        Baseclass override.

        :param etag:
            If specified, instruct the Box API to delete the link only if the current version's etag matches.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :returns:
            Whether or not the update was successful.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        # pylint:disable=arguments-differ
        return super().remove_shared_link(etag=etag)

    @api_call
    def delete(self, *, params: dict = None, etag: Optional[str] = None, **kwargs) -> bool:
        """Delete the item.

        :param params:
            Additional parameters to send with the request.
        :param etag:
            If specified, instruct the Box API to delete the item only if the current version's etag matches.
        :returns:
            Whether or not the delete was successful.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        # pylint:disable=arguments-differ,arguments-renamed
        self.validate_item_id(self._object_id)
        headers = {'If-Match': etag} if etag is not None else None
        return super().delete(params=params, headers=headers, **kwargs)

    def metadata(self, scope: str = 'global', template: str = 'properties') -> Metadata:
        """
        Instantiate a :class:`Metadata` object associated with this item.

        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :param template:
            The name of the metadata template.
            See https://developer.box.com/en/reference/resources/metadata/ for more details.
        :return:
            A new metadata instance associated with this item.
        """
        self.validate_item_id(self._object_id)
        return Metadata(self._session, self, scope, template)

    def get_all_metadata(self) -> MarkerBasedDictCollection:
        """
        Get all metadata attached to the item.
        """
        self.validate_item_id(self._object_id)
        return MarkerBasedDictCollection(
            session=self._session,
            url=self.get_url('metadata'),
            limit=None,
            marker=None,
            return_full_pages=False,
        )

    @api_call
    def get_watermark(self) -> 'Watermark':
        """
        Return the watermark info for a Box file

        :return:
            Watermark object.
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        box_response = self._session.get(url)
        response = box_response.json()
        return self.translator.get('watermark')(response['watermark'])

    @api_call
    def apply_watermark(self) -> 'Watermark':
        """
        Apply watermark on a Box file

        :return:
            Watermark object.
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        body_attributes = {
            'watermark': {
                'imprint': 'default'
            }
        }
        box_response = self._session.put(url, data=json.dumps(body_attributes))
        response = box_response.json()
        return self.translator.get('watermark')(response['watermark'])

    @api_call
    def delete_watermark(self) -> bool:
        """
        Deletes the watermark info for a Box file

        :return:
            Whether or not the delete succeeded.
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        box_response = self._session.delete(url, expect_json_response=False)
        return box_response.ok

    @api_call
    def collaborate(
            self,
            accessible_by: Union['User', 'Group'],
            role: str,
            can_view_path: Optional[bool] = None,
            notify: Optional[bool] = None,
            fields: Iterable[str] = None
    ) -> 'Collaboration':
        """Collaborate user or group onto a Box item.

        :param accessible_by:
            An object containing the collaborator.
        :param role:
            The permission level to grant the collaborator.
        :param can_view_path:
            Indicates whether the user can view the path of the item collaborated into.  This can only be set for
            collaborations on folders.
        :param notify:
            Determines if the collaborator should receive a notification for the collaboration.
        :param fields:
            List of fields to request.
        :return:
            The new collaboration
        """
        self.validate_item_id(self._object_id)
        url = self._session.get_url('collaborations')
        body = {
            'item': {
                'type': self.object_type,
                'id': self.object_id,
            },
            'accessible_by': {
                'type': accessible_by.object_type,
                'id': accessible_by.object_id,
            },
            'role': role,
        }
        if can_view_path is not None:
            body['can_view_path'] = can_view_path
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        if notify is not None:
            params['notify'] = notify
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def collaborate_with_login(
            self,
            login: str,
            role: str,
            can_view_path: Optional[bool] = None,
            notify: Optional[bool] = None,
            fields: Iterable[str] = None
    ) -> 'Collaboration':
        """Collaborate user onto a Box item with the user login.

        :param login:
            The email address of the person to grant access to.
        :param role:
            The permission level to grant the collaborator.
        :param can_view_path:
            Indicates whether the user can view the path of the folder collaborated into.
        :param notify:
            Determines if the collaborator should receive a notification for the collaboration.
        :param fields:
            List of fields to request.
        :return:
            The new collaboration with the user login
        """
        self.validate_item_id(self._object_id)
        url = self._session.get_url('collaborations')
        body = {
            'item': {
                'type': self.object_type,
                'id': self.object_id,
            },
            'accessible_by': {
                'type': 'user',
                'login': login,
            },
            'role': role,
        }
        if can_view_path is not None:
            body['can_view_path'] = can_view_path
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        if notify is not None:
            params['notify'] = notify
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_collaborations(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the collaboration.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the collaboration.
        """
        self.validate_item_id(self._object_id)
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaborations'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def add_classification(self, classification: str) -> str:
        """
        Applies metadata classification for the specified :class:`File` or :class:`Folder` object.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :return:
            The classification added to the :class:`File` or :class:`Folder.
        """
        classification_metadata = {
            'Box__Security__Classification__Key': classification,
        }
        metadata_classification = self.metadata(
            scope='enterprise',
            template=self._classification_template_key
        ).create(classification_metadata)
        return metadata_classification['Box__Security__Classification__Key']

    def update_classification(self, classification: str) -> str:
        """
        Updates metadata classification for the specified :class:`File` or :class:`Folder` object.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :return:
            The classification updated on the :class:`File` or :class:`Folder.
        """
        classification_metadata = self.metadata('enterprise', self._classification_template_key)
        updates = classification_metadata.start_update()
        updates.add('/Box__Security__Classification__Key', classification)
        metadata_classification = classification_metadata.update(updates)
        return metadata_classification['Box__Security__Classification__Key']

    def set_classification(self, classification: str) -> str:
        """
        Attempts to add a metadata classification to a :class:`File` or :class:`Folder`, if classification exists, then
        do update.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :return:
            The classification set on the :class:`File` or :class:`Folder.
        """
        classification_metadata = {
            'Box__Security__Classification__Key': classification,
        }
        return self.metadata(
            scope='enterprise',
            template=self._classification_template_key
        ).set(metadata=classification_metadata)['Box__Security__Classification__Key']

    def get_classification(self) -> Optional[str]:
        """
        Retrieves the classification specified for the :class:`File` or :class:`Folder`

        :return:
            The classification on the :class:`File` or :class:`Folder.
        """
        try:
            classification = self.metadata('enterprise', self._classification_template_key).get()
        except BoxAPIException as err:
            if err.status == 404 and err.code == "instance_not_found":
                return None
            raise
        return classification.get('Box__Security__Classification__Key', None)

    def remove_classification(self) -> bool:
        """
        Removes a metadata classification from a :class:`File` or :class:`Folder`.

        :returns:
            Whether or not the delete was successful.
        """
        return self.metadata('enterprise', self._classification_template_key).delete()

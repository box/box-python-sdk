from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from typing import List

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.webhooks import Webhooks

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.webhook import Webhook

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import compute_webhook_signature

from box_sdk_gen.internal.utils import compare_signatures

from box_sdk_gen.internal.utils import date_time_from_string

from box_sdk_gen.internal.utils import get_epoch_time_in_seconds

from box_sdk_gen.internal.utils import date_time_to_epoch_seconds


class CreateWebhookTargetTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class CreateWebhookTarget(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CreateWebhookTargetTypeField] = None,
        **kwargs
    ):
        """
        :param id: The ID of the item to trigger a webhook., defaults to None
        :type id: Optional[str], optional
        :param type: The type of item to trigger a webhook., defaults to None
        :type type: Optional[CreateWebhookTargetTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateWebhookTriggers(str, Enum):
    FILE_UPLOADED = 'FILE.UPLOADED'
    FILE_PREVIEWED = 'FILE.PREVIEWED'
    FILE_DOWNLOADED = 'FILE.DOWNLOADED'
    FILE_TRASHED = 'FILE.TRASHED'
    FILE_DELETED = 'FILE.DELETED'
    FILE_RESTORED = 'FILE.RESTORED'
    FILE_COPIED = 'FILE.COPIED'
    FILE_MOVED = 'FILE.MOVED'
    FILE_LOCKED = 'FILE.LOCKED'
    FILE_UNLOCKED = 'FILE.UNLOCKED'
    FILE_RENAMED = 'FILE.RENAMED'
    COMMENT_CREATED = 'COMMENT.CREATED'
    COMMENT_UPDATED = 'COMMENT.UPDATED'
    COMMENT_DELETED = 'COMMENT.DELETED'
    TASK_ASSIGNMENT_CREATED = 'TASK_ASSIGNMENT.CREATED'
    TASK_ASSIGNMENT_UPDATED = 'TASK_ASSIGNMENT.UPDATED'
    METADATA_INSTANCE_CREATED = 'METADATA_INSTANCE.CREATED'
    METADATA_INSTANCE_UPDATED = 'METADATA_INSTANCE.UPDATED'
    METADATA_INSTANCE_DELETED = 'METADATA_INSTANCE.DELETED'
    FOLDER_CREATED = 'FOLDER.CREATED'
    FOLDER_RENAMED = 'FOLDER.RENAMED'
    FOLDER_DOWNLOADED = 'FOLDER.DOWNLOADED'
    FOLDER_RESTORED = 'FOLDER.RESTORED'
    FOLDER_DELETED = 'FOLDER.DELETED'
    FOLDER_COPIED = 'FOLDER.COPIED'
    FOLDER_MOVED = 'FOLDER.MOVED'
    FOLDER_TRASHED = 'FOLDER.TRASHED'
    WEBHOOK_DELETED = 'WEBHOOK.DELETED'
    COLLABORATION_CREATED = 'COLLABORATION.CREATED'
    COLLABORATION_ACCEPTED = 'COLLABORATION.ACCEPTED'
    COLLABORATION_REJECTED = 'COLLABORATION.REJECTED'
    COLLABORATION_REMOVED = 'COLLABORATION.REMOVED'
    COLLABORATION_UPDATED = 'COLLABORATION.UPDATED'
    SHARED_LINK_DELETED = 'SHARED_LINK.DELETED'
    SHARED_LINK_CREATED = 'SHARED_LINK.CREATED'
    SHARED_LINK_UPDATED = 'SHARED_LINK.UPDATED'
    SIGN_REQUEST_COMPLETED = 'SIGN_REQUEST.COMPLETED'
    SIGN_REQUEST_DECLINED = 'SIGN_REQUEST.DECLINED'
    SIGN_REQUEST_EXPIRED = 'SIGN_REQUEST.EXPIRED'
    SIGN_REQUEST_SIGNER_EMAIL_BOUNCED = 'SIGN_REQUEST.SIGNER_EMAIL_BOUNCED'
    SIGN_REQUEST_SIGN_SIGNER_SIGNED = 'SIGN_REQUEST.SIGN_SIGNER_SIGNED'
    SIGN_REQUEST_SIGN_DOCUMENT_CREATED = 'SIGN_REQUEST.SIGN_DOCUMENT_CREATED'
    SIGN_REQUEST_SIGN_ERROR_FINALIZING = 'SIGN_REQUEST.SIGN_ERROR_FINALIZING'


class UpdateWebhookByIdTargetTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class UpdateWebhookByIdTarget(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[UpdateWebhookByIdTargetTypeField] = None,
        **kwargs
    ):
        """
        :param id: The ID of the item to trigger a webhook., defaults to None
        :type id: Optional[str], optional
        :param type: The type of item to trigger a webhook., defaults to None
        :type type: Optional[UpdateWebhookByIdTargetTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class UpdateWebhookByIdTriggers(str, Enum):
    FILE_UPLOADED = 'FILE.UPLOADED'
    FILE_PREVIEWED = 'FILE.PREVIEWED'
    FILE_DOWNLOADED = 'FILE.DOWNLOADED'
    FILE_TRASHED = 'FILE.TRASHED'
    FILE_DELETED = 'FILE.DELETED'
    FILE_RESTORED = 'FILE.RESTORED'
    FILE_COPIED = 'FILE.COPIED'
    FILE_MOVED = 'FILE.MOVED'
    FILE_LOCKED = 'FILE.LOCKED'
    FILE_UNLOCKED = 'FILE.UNLOCKED'
    FILE_RENAMED = 'FILE.RENAMED'
    COMMENT_CREATED = 'COMMENT.CREATED'
    COMMENT_UPDATED = 'COMMENT.UPDATED'
    COMMENT_DELETED = 'COMMENT.DELETED'
    TASK_ASSIGNMENT_CREATED = 'TASK_ASSIGNMENT.CREATED'
    TASK_ASSIGNMENT_UPDATED = 'TASK_ASSIGNMENT.UPDATED'
    METADATA_INSTANCE_CREATED = 'METADATA_INSTANCE.CREATED'
    METADATA_INSTANCE_UPDATED = 'METADATA_INSTANCE.UPDATED'
    METADATA_INSTANCE_DELETED = 'METADATA_INSTANCE.DELETED'
    FOLDER_CREATED = 'FOLDER.CREATED'
    FOLDER_RENAMED = 'FOLDER.RENAMED'
    FOLDER_DOWNLOADED = 'FOLDER.DOWNLOADED'
    FOLDER_RESTORED = 'FOLDER.RESTORED'
    FOLDER_DELETED = 'FOLDER.DELETED'
    FOLDER_COPIED = 'FOLDER.COPIED'
    FOLDER_MOVED = 'FOLDER.MOVED'
    FOLDER_TRASHED = 'FOLDER.TRASHED'
    WEBHOOK_DELETED = 'WEBHOOK.DELETED'
    COLLABORATION_CREATED = 'COLLABORATION.CREATED'
    COLLABORATION_ACCEPTED = 'COLLABORATION.ACCEPTED'
    COLLABORATION_REJECTED = 'COLLABORATION.REJECTED'
    COLLABORATION_REMOVED = 'COLLABORATION.REMOVED'
    COLLABORATION_UPDATED = 'COLLABORATION.UPDATED'
    SHARED_LINK_DELETED = 'SHARED_LINK.DELETED'
    SHARED_LINK_CREATED = 'SHARED_LINK.CREATED'
    SHARED_LINK_UPDATED = 'SHARED_LINK.UPDATED'
    SIGN_REQUEST_COMPLETED = 'SIGN_REQUEST.COMPLETED'
    SIGN_REQUEST_DECLINED = 'SIGN_REQUEST.DECLINED'
    SIGN_REQUEST_EXPIRED = 'SIGN_REQUEST.EXPIRED'
    SIGN_REQUEST_SIGNER_EMAIL_BOUNCED = 'SIGN_REQUEST.SIGNER_EMAIL_BOUNCED'
    SIGN_REQUEST_SIGN_SIGNER_SIGNED = 'SIGN_REQUEST.SIGN_SIGNER_SIGNED'
    SIGN_REQUEST_SIGN_DOCUMENT_CREATED = 'SIGN_REQUEST.SIGN_DOCUMENT_CREATED'
    SIGN_REQUEST_SIGN_ERROR_FINALIZING = 'SIGN_REQUEST.SIGN_ERROR_FINALIZING'


class WebhooksManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_webhooks(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Webhooks:
        """
                Returns all defined webhooks for the requesting application.

                This API only returns webhooks that are applied to files or folders that are


                owned by the authenticated user. This means that an admin can not see webhooks


                created by a service account unless the admin has access to those folders, and


                vice versa.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/webhooks']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Webhooks)

    def create_webhook(
        self,
        target: CreateWebhookTarget,
        address: str,
        triggers: List[CreateWebhookTriggers],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Webhook:
        """
                Creates a webhook.
                :param target: The item that will trigger the webhook.
                :type target: CreateWebhookTarget
                :param address: The URL that is notified by this webhook.
                :type address: str
                :param triggers: An array of event names that this webhook is
        to be triggered for.
                :type triggers: List[CreateWebhookTriggers]
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'target': target,
            'address': address,
            'triggers': triggers,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/webhooks']),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Webhook)

    def get_webhook_by_id(
        self,
        webhook_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Webhook:
        """
                Retrieves a specific webhook.
                :param webhook_id: The ID of the webhook.
        Example: "3321123"
                :type webhook_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/webhooks/',
                        to_string(webhook_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Webhook)

    def update_webhook_by_id(
        self,
        webhook_id: str,
        *,
        target: Optional[UpdateWebhookByIdTarget] = None,
        address: Optional[str] = None,
        triggers: Optional[List[UpdateWebhookByIdTriggers]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Webhook:
        """
                Updates a webhook.
                :param webhook_id: The ID of the webhook.
        Example: "3321123"
                :type webhook_id: str
                :param target: The item that will trigger the webhook., defaults to None
                :type target: Optional[UpdateWebhookByIdTarget], optional
                :param address: The URL that is notified by this webhook., defaults to None
                :type address: Optional[str], optional
                :param triggers: An array of event names that this webhook is
        to be triggered for., defaults to None
                :type triggers: Optional[List[UpdateWebhookByIdTriggers]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'target': target,
            'address': address,
            'triggers': triggers,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/webhooks/',
                        to_string(webhook_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Webhook)

    def delete_webhook_by_id(
        self,
        webhook_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a webhook.
                :param webhook_id: The ID of the webhook.
        Example: "3321123"
                :type webhook_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/webhooks/',
                        to_string(webhook_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    @staticmethod
    def validate_message(
        body: str,
        headers: Dict[str, str],
        primary_key: str,
        *,
        secondary_key: Optional[str] = None,
        max_age: Optional[int] = 600
    ) -> bool:
        """
        Validate a webhook message by verifying the signature and the delivery timestamp
        :param body: The request body of the webhook message
        :type body: str
        :param headers: The headers of the webhook message
        :type headers: Dict[str, str]
        :param primary_key: The primary signature to verify the message with
        :type primary_key: str
        :param secondary_key: The secondary signature to verify the message with, defaults to None
        :type secondary_key: Optional[str], optional
        :param max_age: The maximum age of the message in seconds, defaults to 10 minutes, defaults to 600
        :type max_age: Optional[int], optional
        """
        delivery_timestamp: DateTime = date_time_from_string(
            headers.get('box-delivery-timestamp')
        )
        current_epoch: int = get_epoch_time_in_seconds()
        if (
            current_epoch - max_age > date_time_to_epoch_seconds(delivery_timestamp)
            or date_time_to_epoch_seconds(delivery_timestamp) > current_epoch
        ):
            return False
        if (
            not primary_key == None and not headers.get('box-signature-primary') == None
        ) and compare_signatures(
            expected_signature=compute_webhook_signature(
                body, headers, primary_key, escape_body=False
            ),
            received_signature=headers.get('box-signature-primary'),
        ):
            return True
        if (
            not primary_key == None and not headers.get('box-signature-primary') == None
        ) and compare_signatures(
            expected_signature=compute_webhook_signature(
                body, headers, primary_key, escape_body=True
            ),
            received_signature=headers.get('box-signature-primary'),
        ):
            return True
        if (
            not secondary_key == None
            and not headers.get('box-signature-secondary') == None
        ) and compare_signatures(
            expected_signature=compute_webhook_signature(
                body, headers, secondary_key, escape_body=False
            ),
            received_signature=headers.get('box-signature-secondary'),
        ):
            return True
        if (
            not secondary_key == None
            and not headers.get('box-signature-secondary') == None
        ) and compare_signatures(
            expected_signature=compute_webhook_signature(
                body, headers, secondary_key, escape_body=True
            ),
            received_signature=headers.get('box-signature-secondary'),
        ):
            return True
        return False

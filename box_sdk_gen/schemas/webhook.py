from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.schemas.webhook_mini import WebhookMiniTypeField

from box_sdk_gen.schemas.webhook_mini import WebhookMiniTargetField

from box_sdk_gen.schemas.webhook_mini import WebhookMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class WebhookTriggersField(str, Enum):
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


class Webhook(WebhookMini):
    def __init__(
        self,
        *,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        address: Optional[str] = None,
        triggers: Optional[List[WebhookTriggersField]] = None,
        id: Optional[str] = None,
        type: Optional[WebhookMiniTypeField] = None,
        target: Optional[WebhookMiniTargetField] = None,
        **kwargs
    ):
        """
                :param created_at: A timestamp identifying the time that
        the webhook was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param address: The URL that is notified by this webhook., defaults to None
                :type address: Optional[str], optional
                :param triggers: An array of event names that this webhook is
        to be triggered for., defaults to None
                :type triggers: Optional[List[WebhookTriggersField]], optional
                :param id: The unique identifier for this webhook., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `webhook`., defaults to None
                :type type: Optional[WebhookMiniTypeField], optional
                :param target: The item that will trigger the webhook., defaults to None
                :type target: Optional[WebhookMiniTargetField], optional
        """
        super().__init__(id=id, type=type, target=target, **kwargs)
        self.created_by = created_by
        self.created_at = created_at
        self.address = address
        self.triggers = triggers

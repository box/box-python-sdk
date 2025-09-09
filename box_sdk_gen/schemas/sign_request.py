from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.sign_request_prefill_tag import SignRequestPrefillTag

from box_sdk_gen.schemas.sign_request_base import SignRequestBase

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.sign_request_signer import SignRequestSigner

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class SignRequestTypeField(str, Enum):
    SIGN_REQUEST = 'sign-request'


class SignRequestStatusField(str, Enum):
    CONVERTING = 'converting'
    CREATED = 'created'
    SENT = 'sent'
    VIEWED = 'viewed'
    SIGNED = 'signed'
    CANCELLED = 'cancelled'
    DECLINED = 'declined'
    ERROR_CONVERTING = 'error_converting'
    ERROR_SENDING = 'error_sending'
    EXPIRED = 'expired'
    FINALIZING = 'finalizing'
    ERROR_FINALIZING = 'error_finalizing'


class SignRequestSignFilesField(BaseObject):
    def __init__(
        self,
        *,
        files: Optional[List[FileMini]] = None,
        is_ready_for_download: Optional[bool] = None,
        **kwargs
    ):
        """
                :param is_ready_for_download: Indicates whether the `sign_files` documents are processing
        and the PDFs may be out of date. A change to any document
        requires processing on all `sign_files`. We
        recommended waiting until processing is finished
        (and this value is true) before downloading the PDFs., defaults to None
                :type is_ready_for_download: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.files = files
        self.is_ready_for_download = is_ready_for_download


class SignRequest(SignRequestBase):
    def __init__(
        self,
        *,
        type: Optional[SignRequestTypeField] = None,
        source_files: Optional[List[FileBase]] = None,
        signers: Optional[List[SignRequestSigner]] = None,
        signature_color: Optional[str] = None,
        id: Optional[str] = None,
        prepare_url: Optional[str] = None,
        signing_log: Optional[FileMini] = None,
        status: Optional[SignRequestStatusField] = None,
        sign_files: Optional[SignRequestSignFilesField] = None,
        auto_expire_at: Optional[DateTime] = None,
        parent_folder: Optional[FolderMini] = None,
        collaborator_level: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_id: Optional[int] = None,
        is_document_preparation_needed: Optional[bool] = None,
        redirect_url: Optional[str] = None,
        declined_redirect_url: Optional[str] = None,
        are_text_signatures_enabled: Optional[bool] = None,
        email_subject: Optional[str] = None,
        email_message: Optional[str] = None,
        are_reminders_enabled: Optional[bool] = None,
        name: Optional[str] = None,
        prefill_tags: Optional[List[SignRequestPrefillTag]] = None,
        days_valid: Optional[int] = None,
        external_id: Optional[str] = None,
        template_id: Optional[str] = None,
        external_system_name: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `sign-request`., defaults to None
                :type type: Optional[SignRequestTypeField], optional
                :param source_files: List of files to create a signing document from. This is currently limited to ten files. Only the ID and type fields are required for each file., defaults to None
                :type source_files: Optional[List[FileBase]], optional
                :param signers: Array of signers for the signature request., defaults to None
                :type signers: Optional[List[SignRequestSigner]], optional
                :param signature_color: Force a specific color for the signature (blue, black, or red)., defaults to None
                :type signature_color: Optional[str], optional
                :param id: Box Sign request ID., defaults to None
                :type id: Optional[str], optional
                :param prepare_url: This URL is returned if `is_document_preparation_needed` is
        set to `true` in the request. The parameter is used to prepare
        the signature request
        using the UI. The signature request is not
        sent until the preparation
        phase is complete., defaults to None
                :type prepare_url: Optional[str], optional
                :param status: Describes the status of the signature request., defaults to None
                :type status: Optional[SignRequestStatusField], optional
                :param sign_files: List of files that will be signed, which are copies of the original
        source files. A new version of these files are created as signers sign
        and can be downloaded at any point in the signing process., defaults to None
                :type sign_files: Optional[SignRequestSignFilesField], optional
                :param auto_expire_at: Uses `days_valid` to calculate the date and time, in GMT, the sign request will expire if unsigned., defaults to None
                :type auto_expire_at: Optional[DateTime], optional
                :param collaborator_level: The collaborator level of the user to the sign request. Values can include "owner", "editor", and "viewer"., defaults to None
                :type collaborator_level: Optional[str], optional
                :param sender_email: The email address of the sender of the sign request., defaults to None
                :type sender_email: Optional[str], optional
                :param sender_id: The user ID of the sender of the sign request., defaults to None
                :type sender_id: Optional[int], optional
                :param is_document_preparation_needed: Indicates if the sender should receive a `prepare_url` in the response to complete document preparation using the UI., defaults to None
                :type is_document_preparation_needed: Optional[bool], optional
                :param redirect_url: When specified, the signature request will be redirected to this url when a document is signed., defaults to None
                :type redirect_url: Optional[str], optional
                :param declined_redirect_url: The uri that a signer will be redirected to after declining to sign a document., defaults to None
                :type declined_redirect_url: Optional[str], optional
                :param are_text_signatures_enabled: Disables the usage of signatures generated by typing (text)., defaults to None
                :type are_text_signatures_enabled: Optional[bool], optional
                :param email_subject: Subject of sign request email. This is cleaned by sign request. If this field is not passed, a default subject will be used., defaults to None
                :type email_subject: Optional[str], optional
                :param email_message: Message to include in sign request email. The field is cleaned through sanitization of specific characters. However, some html tags are allowed. Links included in the message are also converted to hyperlinks in the email. The message may contain the following html tags including `a`, `abbr`, `acronym`, `b`, `blockquote`, `code`, `em`, `i`, `ul`, `li`, `ol`, and `strong`. Be aware that when the text to html ratio is too high, the email may end up in spam filters. Custom styles on these tags are not allowed. If this field is not passed, a default message will be used., defaults to None
                :type email_message: Optional[str], optional
                :param are_reminders_enabled: Reminds signers to sign a document on day 3, 8, 13 and 18. Reminders are only sent to outstanding signers., defaults to None
                :type are_reminders_enabled: Optional[bool], optional
                :param name: Name of the signature request., defaults to None
                :type name: Optional[str], optional
                :param prefill_tags: When a document contains sign-related tags in the content, you can prefill them using this `prefill_tags` by referencing the 'id' of the tag as the `external_id` field of the prefill tag., defaults to None
                :type prefill_tags: Optional[List[SignRequestPrefillTag]], optional
                :param days_valid: Set the number of days after which the created signature request will automatically expire if not completed. By default, we do not apply any expiration date on signature requests, and the signature request does not expire., defaults to None
                :type days_valid: Optional[int], optional
                :param external_id: This can be used to reference an ID in an external system that the sign request is related to., defaults to None
                :type external_id: Optional[str], optional
                :param template_id: When a signature request is created from a template this field will indicate the id of that template., defaults to None
                :type template_id: Optional[str], optional
                :param external_system_name: Used as an optional system name to appear in the signature log next to the signers who have been assigned the `embed_url_external_id`., defaults to None
                :type external_system_name: Optional[str], optional
        """
        super().__init__(
            is_document_preparation_needed=is_document_preparation_needed,
            redirect_url=redirect_url,
            declined_redirect_url=declined_redirect_url,
            are_text_signatures_enabled=are_text_signatures_enabled,
            email_subject=email_subject,
            email_message=email_message,
            are_reminders_enabled=are_reminders_enabled,
            name=name,
            prefill_tags=prefill_tags,
            days_valid=days_valid,
            external_id=external_id,
            template_id=template_id,
            external_system_name=external_system_name,
            **kwargs
        )
        self.type = type
        self.source_files = source_files
        self.signers = signers
        self.signature_color = signature_color
        self.id = id
        self.prepare_url = prepare_url
        self.signing_log = signing_log
        self.status = status
        self.sign_files = sign_files
        self.auto_expire_at = auto_expire_at
        self.parent_folder = parent_folder
        self.collaborator_level = collaborator_level
        self.sender_email = sender_email
        self.sender_id = sender_id

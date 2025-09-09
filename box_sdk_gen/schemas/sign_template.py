from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.template_signer import TemplateSigner

from box_sdk_gen.box.errors import BoxSDKError


class SignTemplateTypeField(str, Enum):
    SIGN_TEMPLATE = 'sign-template'


class SignTemplateAdditionalInfoNonEditableField(str, Enum):
    EMAIL_SUBJECT = 'email_subject'
    EMAIL_MESSAGE = 'email_message'
    NAME = 'name'
    DAYS_VALID = 'days_valid'
    SIGNERS = 'signers'
    SOURCE_FILES = 'source_files'


class SignTemplateAdditionalInfoRequiredSignersField(str, Enum):
    EMAIL = 'email'


class SignTemplateAdditionalInfoRequiredField(BaseObject):
    def __init__(
        self,
        *,
        signers: Optional[
            List[List[SignTemplateAdditionalInfoRequiredSignersField]]
        ] = None,
        **kwargs
    ):
        """
        :param signers: Required signer fields., defaults to None
        :type signers: Optional[List[List[SignTemplateAdditionalInfoRequiredSignersField]]], optional
        """
        super().__init__(**kwargs)
        self.signers = signers


class SignTemplateAdditionalInfoField(BaseObject):
    def __init__(
        self,
        *,
        non_editable: Optional[List[SignTemplateAdditionalInfoNonEditableField]] = None,
        required: Optional[SignTemplateAdditionalInfoRequiredField] = None,
        **kwargs
    ):
        """
        :param non_editable: Non editable fields., defaults to None
        :type non_editable: Optional[List[SignTemplateAdditionalInfoNonEditableField]], optional
        :param required: Required fields., defaults to None
        :type required: Optional[SignTemplateAdditionalInfoRequiredField], optional
        """
        super().__init__(**kwargs)
        self.non_editable = non_editable
        self.required = required


class SignTemplateReadySignLinkField(BaseObject):
    def __init__(
        self,
        *,
        url: Optional[str] = None,
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        folder_id: Optional[str] = None,
        is_notification_disabled: Optional[bool] = None,
        is_active: Optional[bool] = None,
        **kwargs
    ):
        """
                :param url: The URL that can be sent to signers., defaults to None
                :type url: Optional[str], optional
                :param name: Request name., defaults to None
                :type name: Optional[str], optional
                :param instructions: Extra instructions for all signers., defaults to None
                :type instructions: Optional[str], optional
                :param folder_id: The destination folder to place final,
        signed document and signing
        log. Only `ID` and `type` fields are required.
        The root folder,
        folder ID `0`, cannot be used., defaults to None
                :type folder_id: Optional[str], optional
                :param is_notification_disabled: Whether to disable notifications when
        a signer has signed., defaults to None
                :type is_notification_disabled: Optional[bool], optional
                :param is_active: Whether the ready sign link is enabled or not., defaults to None
                :type is_active: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.url = url
        self.name = name
        self.instructions = instructions
        self.folder_id = folder_id
        self.is_notification_disabled = is_notification_disabled
        self.is_active = is_active


class SignTemplateCustomBrandingField(BaseObject):
    def __init__(
        self,
        *,
        company_name: Optional[str] = None,
        logo_uri: Optional[str] = None,
        branding_color: Optional[str] = None,
        email_footer_text: Optional[str] = None,
        **kwargs
    ):
        """
        :param company_name: Name of the company., defaults to None
        :type company_name: Optional[str], optional
        :param logo_uri: Custom branding logo URI in the form of a base64 image., defaults to None
        :type logo_uri: Optional[str], optional
        :param branding_color: Custom branding color in hex., defaults to None
        :type branding_color: Optional[str], optional
        :param email_footer_text: Content of the email footer., defaults to None
        :type email_footer_text: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.company_name = company_name
        self.logo_uri = logo_uri
        self.branding_color = branding_color
        self.email_footer_text = email_footer_text


class SignTemplate(BaseObject):
    _discriminator = 'type', {'sign-template'}

    def __init__(
        self,
        *,
        type: Optional[SignTemplateTypeField] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        email_subject: Optional[str] = None,
        email_message: Optional[str] = None,
        days_valid: Optional[int] = None,
        parent_folder: Optional[FolderMini] = None,
        source_files: Optional[List[FileMini]] = None,
        are_fields_locked: Optional[bool] = None,
        are_options_locked: Optional[bool] = None,
        are_recipients_locked: Optional[bool] = None,
        are_email_settings_locked: Optional[bool] = None,
        are_files_locked: Optional[bool] = None,
        signers: Optional[List[TemplateSigner]] = None,
        additional_info: Optional[SignTemplateAdditionalInfoField] = None,
        ready_sign_link: Optional[SignTemplateReadySignLinkField] = None,
        custom_branding: Optional[SignTemplateCustomBrandingField] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `sign-template`., defaults to None
                :type type: Optional[SignTemplateTypeField], optional
                :param id: Template identifier., defaults to None
                :type id: Optional[str], optional
                :param name: The name of the template., defaults to None
                :type name: Optional[str], optional
                :param email_subject: Subject of signature request email. This is cleaned by sign
        request. If this field is not passed, a default subject will be used., defaults to None
                :type email_subject: Optional[str], optional
                :param email_message: Message to include in signature request email. The field
        is cleaned through sanitization of specific characters. However,
        some html tags are allowed. Links included in the
        message are also converted to hyperlinks in the email. The
        message may contain the following html tags including `a`, `abbr`,
        `acronym`, `b`, `blockquote`, `code`, `em`, `i`, `ul`, `li`, `ol`, and
        `strong`. Be aware that when the text
        to html ratio is too high, the email
        may end up in spam filters. Custom styles on
        these tags are not allowed.
        If this field is not passed, a default message will be used., defaults to None
                :type email_message: Optional[str], optional
                :param days_valid: Set the number of days after which the
        created signature request will automatically
        expire if not completed. By default, we do
        not apply any expiration date on signature
        requests, and the signature request does not expire., defaults to None
                :type days_valid: Optional[int], optional
                :param source_files: List of files to create a signing document from.
        Only the ID and type fields are required
        for each file., defaults to None
                :type source_files: Optional[List[FileMini]], optional
                :param are_fields_locked: Indicates if the template input
        fields are editable or not., defaults to None
                :type are_fields_locked: Optional[bool], optional
                :param are_options_locked: Indicates if the template document options
        are editable or not,
        for example renaming the document., defaults to None
                :type are_options_locked: Optional[bool], optional
                :param are_recipients_locked: Indicates if the template signers are editable or not., defaults to None
                :type are_recipients_locked: Optional[bool], optional
                :param are_email_settings_locked: Indicates if the template email settings are editable or not., defaults to None
                :type are_email_settings_locked: Optional[bool], optional
                :param are_files_locked: Indicates if the template files are editable or not.
        This includes deleting or renaming template files., defaults to None
                :type are_files_locked: Optional[bool], optional
                :param signers: Array of signers for the template.

        **Note**: It may happen that some signers specified in the template belong to conflicting [segments](r://shield-information-barrier-segment-member) (user groups).
        This means that due to the security policies, users are assigned to segments to prevent exchanges or communication that could lead to ethical conflicts.
        In such a case, an attempt to send a sign request based on a template that lists signers in conflicting segments will result in an error.

        Read more about [segments and ethical walls](https://support.box.com/hc/en-us/articles/9920431507603-Understanding-Information-Barriers#h_01GFVJEHQA06N7XEZ4GCZ9GFAQ)., defaults to None
                :type signers: Optional[List[TemplateSigner]], optional
                :param additional_info: Additional information on which fields are
        required and which fields are not editable., defaults to None
                :type additional_info: Optional[SignTemplateAdditionalInfoField], optional
                :param ready_sign_link: Box's ready-sign link feature enables you to create a
        link to a signature request that
        you've created from a template. Use this link
        when you want to post a signature request
        on a public form — such as an email, social media post,
        or web page — without knowing who the signers will be.
        Note: The ready-sign link feature is
        limited to Enterprise Plus customers and not
        available to Box Verified Enterprises., defaults to None
                :type ready_sign_link: Optional[SignTemplateReadySignLinkField], optional
                :param custom_branding: Custom branding applied to notifications
        and signature requests., defaults to None
                :type custom_branding: Optional[SignTemplateCustomBrandingField], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.name = name
        self.email_subject = email_subject
        self.email_message = email_message
        self.days_valid = days_valid
        self.parent_folder = parent_folder
        self.source_files = source_files
        self.are_fields_locked = are_fields_locked
        self.are_options_locked = are_options_locked
        self.are_recipients_locked = are_recipients_locked
        self.are_email_settings_locked = are_email_settings_locked
        self.are_files_locked = are_files_locked
        self.signers = signers
        self.additional_info = additional_info
        self.ready_sign_link = ready_sign_link
        self.custom_branding = custom_branding

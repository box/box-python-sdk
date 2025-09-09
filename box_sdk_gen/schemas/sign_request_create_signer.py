from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestCreateSignerRoleField(str, Enum):
    SIGNER = 'signer'
    APPROVER = 'approver'
    FINAL_COPY_READER = 'final_copy_reader'


class SignRequestCreateSigner(BaseObject):
    def __init__(
        self,
        *,
        email: Optional[str] = None,
        role: Optional[SignRequestCreateSignerRoleField] = None,
        is_in_person: Optional[bool] = None,
        order: Optional[int] = None,
        embed_url_external_user_id: Optional[str] = None,
        redirect_url: Optional[str] = None,
        declined_redirect_url: Optional[str] = None,
        login_required: Optional[bool] = None,
        verification_phone_number: Optional[str] = None,
        password: Optional[str] = None,
        signer_group_id: Optional[str] = None,
        suppress_notifications: Optional[bool] = None,
        **kwargs
    ):
        """
                :param email: Email address of the signer.
        The email address of the signer is required when making signature requests, except when using templates that are configured to include emails., defaults to None
                :type email: Optional[str], optional
                :param role: Defines the role of the signer in the signature request. A `signer`
        must sign the document and an `approver` must approve the document. A
        `final_copy_reader` only receives the final signed document and signing
        log., defaults to None
                :type role: Optional[SignRequestCreateSignerRoleField], optional
                :param is_in_person: Used in combination with an embed URL for a sender. After the
        sender signs, they are redirected to the next `in_person` signer., defaults to None
                :type is_in_person: Optional[bool], optional
                :param order: Order of the signer., defaults to None
                :type order: Optional[int], optional
                :param embed_url_external_user_id: User ID for the signer in an external application responsible
        for authentication when accessing the embed URL., defaults to None
                :type embed_url_external_user_id: Optional[str], optional
                :param redirect_url: The URL that a signer will be redirected
        to after signing a document. Defining this URL
        overrides default or global redirect URL
        settings for a specific signer.
        If no declined redirect URL is specified,
        this URL will be used for decline actions as well., defaults to None
                :type redirect_url: Optional[str], optional
                :param declined_redirect_url: The URL that a signer will be redirect
        to after declining to sign a document.
        Defining this URL overrides default or global
        declined redirect URL settings for a specific signer., defaults to None
                :type declined_redirect_url: Optional[str], optional
                :param login_required: If set to true, the signer will need to log in to a Box account
        before signing the request. If the signer does not have
        an existing account, they will have the option to create
        a free Box account., defaults to None
                :type login_required: Optional[bool], optional
                :param verification_phone_number: If set, this phone number will be used to verify the signer
        via two-factor authentication before they are able to sign the document.
        Cannot be selected in combination with `login_required`., defaults to None
                :type verification_phone_number: Optional[str], optional
                :param password: If set, the signer is required to enter the password before they are able
        to sign a document. This field is write only., defaults to None
                :type password: Optional[str], optional
                :param signer_group_id: If set, signers who have the same value will be assigned to the same input and to the same signer group.
        A signer group is not a Box Group. It is an entity that belongs to a Sign Request and can only be
        used/accessed within this Sign Request. A signer group is expected to have more than one signer.
        If the provided value is only used for one signer, this value will be ignored and request will be handled
        as it was intended for an individual signer. The value provided can be any string and only used to
        determine which signers belongs to same group. A successful response will provide a generated UUID value
        instead for signers in the same signer group., defaults to None
                :type signer_group_id: Optional[str], optional
                :param suppress_notifications: If true, no emails about the sign request will be sent., defaults to None
                :type suppress_notifications: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.email = email
        self.role = role
        self.is_in_person = is_in_person
        self.order = order
        self.embed_url_external_user_id = embed_url_external_user_id
        self.redirect_url = redirect_url
        self.declined_redirect_url = declined_redirect_url
        self.login_required = login_required
        self.verification_phone_number = verification_phone_number
        self.password = password
        self.signer_group_id = signer_group_id
        self.suppress_notifications = suppress_notifications

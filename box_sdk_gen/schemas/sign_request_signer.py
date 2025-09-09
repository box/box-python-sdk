from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.sign_request_create_signer import (
    SignRequestCreateSignerRoleField,
)

from box_sdk_gen.schemas.sign_request_create_signer import SignRequestCreateSigner

from box_sdk_gen.schemas.sign_request_signer_input import SignRequestSignerInput

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class SignRequestSignerSignerDecisionTypeField(str, Enum):
    SIGNED = 'signed'
    DECLINED = 'declined'


class SignRequestSignerSignerDecisionField(BaseObject):
    _discriminator = 'type', {'signed', 'declined'}

    def __init__(
        self,
        *,
        type: Optional[SignRequestSignerSignerDecisionTypeField] = None,
        finalized_at: Optional[DateTime] = None,
        additional_info: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: Type of decision made by the signer., defaults to None
        :type type: Optional[SignRequestSignerSignerDecisionTypeField], optional
        :param finalized_at: Date and Time that the decision was made., defaults to None
        :type finalized_at: Optional[DateTime], optional
        :param additional_info: Additional info about the decision, such as the decline reason from the signer., defaults to None
        :type additional_info: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.finalized_at = finalized_at
        self.additional_info = additional_info


class SignRequestSigner(SignRequestCreateSigner):
    def __init__(
        self,
        *,
        has_viewed_document: Optional[bool] = None,
        signer_decision: Optional[SignRequestSignerSignerDecisionField] = None,
        inputs: Optional[List[SignRequestSignerInput]] = None,
        embed_url: Optional[str] = None,
        iframeable_embed_url: Optional[str] = None,
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
                :param has_viewed_document: Set to `true` if the signer views the document., defaults to None
                :type has_viewed_document: Optional[bool], optional
                :param signer_decision: Final decision made by the signer., defaults to None
                :type signer_decision: Optional[SignRequestSignerSignerDecisionField], optional
                :param embed_url: URL to direct a signer to for signing., defaults to None
                :type embed_url: Optional[str], optional
                :param iframeable_embed_url: This URL is specifically designed for
        signing documents within an HTML `iframe` tag.
        It will be returned in the response
        only if the `embed_url_external_user_id`
        parameter was passed in the
        `create Box Sign request` call., defaults to None
                :type iframeable_embed_url: Optional[str], optional
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
        super().__init__(
            email=email,
            role=role,
            is_in_person=is_in_person,
            order=order,
            embed_url_external_user_id=embed_url_external_user_id,
            redirect_url=redirect_url,
            declined_redirect_url=declined_redirect_url,
            login_required=login_required,
            verification_phone_number=verification_phone_number,
            password=password,
            signer_group_id=signer_group_id,
            suppress_notifications=suppress_notifications,
            **kwargs
        )
        self.has_viewed_document = has_viewed_document
        self.signer_decision = signer_decision
        self.inputs = inputs
        self.embed_url = embed_url
        self.iframeable_embed_url = iframeable_embed_url

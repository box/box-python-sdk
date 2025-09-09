from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.template_signer_input import TemplateSignerInput

from box_sdk_gen.box.errors import BoxSDKError


class TemplateSignerRoleField(str, Enum):
    SIGNER = 'signer'
    APPROVER = 'approver'
    FINAL_COPY_READER = 'final_copy_reader'


class TemplateSigner(BaseObject):
    def __init__(
        self,
        *,
        inputs: Optional[List[TemplateSignerInput]] = None,
        email: Optional[str] = None,
        role: Optional[TemplateSignerRoleField] = None,
        is_in_person: Optional[bool] = None,
        order: Optional[int] = None,
        signer_group_id: Optional[str] = None,
        label: Optional[str] = None,
        public_id: Optional[str] = None,
        is_password_required: Optional[bool] = None,
        is_phone_number_required: Optional[bool] = None,
        login_required: Optional[bool] = None,
        **kwargs
    ):
        """
                :param email: Email address of the signer., defaults to None
                :type email: Optional[str], optional
                :param role: Defines the role of the signer in the signature request. A role of
        `signer` needs to sign the document, a role `approver`
        approves the document and
        a `final_copy_reader` role only
        receives the final signed document and signing log., defaults to None
                :type role: Optional[TemplateSignerRoleField], optional
                :param is_in_person: Used in combination with an embed URL for a sender.
        After the sender signs, they will be
        redirected to the next `in_person` signer., defaults to None
                :type is_in_person: Optional[bool], optional
                :param order: Order of the signer., defaults to None
                :type order: Optional[int], optional
                :param signer_group_id: If provided, this value points signers that are assigned the same inputs and belongs to same signer group.
        A signer group is not a Box Group. It is an entity that belongs to the template itself and can only be used
        within Box Sign requests created from it., defaults to None
                :type signer_group_id: Optional[str], optional
                :param label: A placeholder label for the signer set by the template creator to differentiate between signers., defaults to None
                :type label: Optional[str], optional
                :param public_id: An identifier for the signer. This can be used to identify a signer within the template., defaults to None
                :type public_id: Optional[str], optional
                :param is_password_required: If true for signers with a defined email, the password provided when the template was created is used by default.
        If true for signers without a specified / defined email, the creator needs to provide a password when using the template., defaults to None
                :type is_password_required: Optional[bool], optional
                :param is_phone_number_required: If true for signers with a defined email, the phone number provided when the template was created is used by default.
        If true for signers without a specified / defined email, the template creator needs to provide a phone number when creating a request., defaults to None
                :type is_phone_number_required: Optional[bool], optional
                :param login_required: If true, the signer is required to login to access the document., defaults to None
                :type login_required: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.inputs = inputs
        self.email = email
        self.role = role
        self.is_in_person = is_in_person
        self.order = order
        self.signer_group_id = signer_group_id
        self.label = label
        self.public_id = public_id
        self.is_password_required = is_password_required
        self.is_phone_number_required = is_phone_number_required
        self.login_required = login_required

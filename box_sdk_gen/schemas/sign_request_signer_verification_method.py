from typing import Union

from box_sdk_gen.schemas.sign_request_signer_verification_method_login import (
    SignRequestSignerVerificationMethodLogin,
)

from box_sdk_gen.schemas.sign_request_signer_verification_method_phone_sms import (
    SignRequestSignerVerificationMethodPhoneSms,
)

from box_sdk_gen.schemas.sign_request_signer_verification_method_cac_piv import (
    SignRequestSignerVerificationMethodCacPiv,
)

from box_sdk_gen.box.errors import BoxSDKError

SignRequestSignerVerificationMethod = Union[
    SignRequestSignerVerificationMethodLogin,
    SignRequestSignerVerificationMethodPhoneSms,
    SignRequestSignerVerificationMethodCacPiv,
]

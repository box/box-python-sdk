from typing import Union

from box_sdk_gen.schemas.template_signer_verification_method_login import (
    TemplateSignerVerificationMethodLogin,
)

from box_sdk_gen.schemas.template_signer_verification_method_phone_sms import (
    TemplateSignerVerificationMethodPhoneSms,
)

from box_sdk_gen.schemas.template_signer_verification_method_cac_piv import (
    TemplateSignerVerificationMethodCacPiv,
)

from box_sdk_gen.box.errors import BoxSDKError

TemplateSignerVerificationMethod = Union[
    TemplateSignerVerificationMethodLogin,
    TemplateSignerVerificationMethodPhoneSms,
    TemplateSignerVerificationMethodCacPiv,
]

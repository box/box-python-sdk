from typing import Union

from box_sdk_gen.schemas.sign_request_signer_input_email_validation import (
    SignRequestSignerInputEmailValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_custom_validation import (
    SignRequestSignerInputCustomValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_zip_validation import (
    SignRequestSignerInputZipValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_zip_4_validation import (
    SignRequestSignerInputZip4Validation,
)

from box_sdk_gen.schemas.sign_request_signer_input_ssn_validation import (
    SignRequestSignerInputSsnValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_number_with_period_validation import (
    SignRequestSignerInputNumberWithPeriodValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_number_with_comma_validation import (
    SignRequestSignerInputNumberWithCommaValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_date_iso_validation import (
    SignRequestSignerInputDateIsoValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_date_us_validation import (
    SignRequestSignerInputDateUsValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_date_eu_validation import (
    SignRequestSignerInputDateEuValidation,
)

from box_sdk_gen.schemas.sign_request_signer_input_date_asia_validation import (
    SignRequestSignerInputDateAsiaValidation,
)

from box_sdk_gen.box.errors import BoxSDKError

SignRequestSignerInputValidation = Union[
    SignRequestSignerInputEmailValidation,
    SignRequestSignerInputCustomValidation,
    SignRequestSignerInputZipValidation,
    SignRequestSignerInputZip4Validation,
    SignRequestSignerInputSsnValidation,
    SignRequestSignerInputNumberWithPeriodValidation,
    SignRequestSignerInputNumberWithCommaValidation,
    SignRequestSignerInputDateIsoValidation,
    SignRequestSignerInputDateUsValidation,
    SignRequestSignerInputDateEuValidation,
    SignRequestSignerInputDateAsiaValidation,
]

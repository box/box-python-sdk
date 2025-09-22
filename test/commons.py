from box_sdk_gen.internal.utils import to_string

from typing import List

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.terms_of_services import TermsOfServices

from box_sdk_gen.managers.terms_of_services import CreateTermsOfServiceStatus

from box_sdk_gen.managers.terms_of_services import CreateTermsOfServiceTosType

from box_sdk_gen.schemas.classification_template import (
    ClassificationTemplateFieldsOptionsField,
)

from box_sdk_gen.managers.classifications import AddClassificationRequestBody

from box_sdk_gen.managers.classifications import AddClassificationRequestBodyDataField

from box_sdk_gen.managers.classifications import (
    AddClassificationRequestBodyDataStaticConfigField,
)

from box_sdk_gen.managers.classifications import (
    AddClassificationRequestBodyDataStaticConfigClassificationField,
)

from box_sdk_gen.managers.classifications import CreateClassificationTemplateFields

from box_sdk_gen.schemas.shield_information_barrier import ShieldInformationBarrier

from box_sdk_gen.schemas.shield_information_barriers import ShieldInformationBarriers

from box_sdk_gen.schemas.enterprise_base import EnterpriseBase

from box_sdk_gen.internal.utils import decode_base_64

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.classification_template import ClassificationTemplate

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.terms_of_service import TermsOfService

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.box.ccg_auth import BoxCCGAuth

from box_sdk_gen.box.ccg_auth import CCGConfig

from box_sdk_gen.internal.utils import is_browser


def get_ccg_auth() -> BoxCCGAuth:
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        enterprise_id=get_env_var('ENTERPRISE_ID'),
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    return auth


from box_sdk_gen.box.jwt_auth import BoxJWTAuth

from box_sdk_gen.box.jwt_auth import JWTConfig


def get_jwt_auth() -> BoxJWTAuth:
    jwt_config: JWTConfig = JWTConfig.from_config_json_string(
        decode_base_64(get_env_var('JWT_CONFIG_BASE_64'))
    )
    auth: BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    return auth


def get_default_client_with_user_subject(user_id: str) -> BoxClient:
    if is_browser():
        ccg_auth: BoxCCGAuth = get_ccg_auth()
        ccg_auth_user: BoxCCGAuth = ccg_auth.with_user_subject(user_id)
        return BoxClient(auth=ccg_auth_user)
    auth: BoxJWTAuth = get_jwt_auth()
    auth_user: BoxJWTAuth = auth.with_user_subject(user_id)
    return BoxClient(auth=auth_user)


def get_default_client() -> BoxClient:
    client: BoxClient = BoxClient(
        auth=get_ccg_auth() if is_browser() else get_jwt_auth()
    )
    return client


def create_new_folder() -> FolderFull:
    client: BoxClient = get_default_client()
    new_folder_name: str = get_uuid()
    return client.folders.create_folder(new_folder_name, CreateFolderParent(id='0'))


def upload_new_file() -> FileFull:
    client: BoxClient = get_default_client()
    new_file_name: str = ''.join([get_uuid(), '.pdf'])
    file_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_content_stream,
    )
    return uploaded_files.entries[0]


def get_or_create_terms_of_services() -> TermsOfService:
    client: BoxClient = get_default_client()
    tos: TermsOfServices = client.terms_of_services.get_terms_of_service()
    number_of_tos: int = len(tos.entries)
    if number_of_tos >= 1:
        first_tos: TermsOfService = tos.entries[0]
        if to_string(first_tos.tos_type) == 'managed':
            return first_tos
    if number_of_tos >= 2:
        second_tos: TermsOfService = tos.entries[1]
        if to_string(second_tos.tos_type) == 'managed':
            return second_tos
    return client.terms_of_services.create_terms_of_service(
        CreateTermsOfServiceStatus.DISABLED,
        'Test TOS',
        tos_type=CreateTermsOfServiceTosType.MANAGED,
    )


def get_or_create_classification(
    classification_template: ClassificationTemplate,
) -> ClassificationTemplateFieldsOptionsField:
    client: BoxClient = get_default_client()
    classifications: List[ClassificationTemplateFieldsOptionsField] = (
        classification_template.fields[0].options
    )
    current_number_of_classifications: int = len(classifications)
    if current_number_of_classifications == 0:
        classification_template_with_new_classification: ClassificationTemplate = (
            client.classifications.add_classification(
                [
                    AddClassificationRequestBody(
                        data=AddClassificationRequestBodyDataField(
                            key=get_uuid(),
                            static_config=AddClassificationRequestBodyDataStaticConfigField(
                                classification=AddClassificationRequestBodyDataStaticConfigClassificationField(
                                    color_id=3,
                                    classification_definition='Some description',
                                )
                            ),
                        )
                    )
                ]
            )
        )
        return classification_template_with_new_classification.fields[0].options[0]
    return classifications[0]


def get_or_create_classification_template() -> ClassificationTemplate:
    client: BoxClient = get_default_client()
    try:
        return client.classifications.get_classification_template()
    except Exception:
        return client.classifications.create_classification_template(
            [CreateClassificationTemplateFields(options=[])]
        )


def get_or_create_shield_information_barrier(
    client: BoxClient, enterprise_id: str
) -> ShieldInformationBarrier:
    barriers: ShieldInformationBarriers = (
        client.shield_information_barriers.get_shield_information_barriers()
    )
    number_of_barriers: int = len(barriers.entries)
    if number_of_barriers == 0:
        return client.shield_information_barriers.create_shield_information_barrier(
            EnterpriseBase(id=enterprise_id)
        )
    return barriers.entries[number_of_barriers - 1]

from typing import List

import pytest

from box_sdk_gen.client import BoxClient

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

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.classification import Classification

from box_sdk_gen.managers.file_classifications import (
    UpdateClassificationOnFileRequestBody,
)

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import get_or_create_classification_template

from test.box_sdk_gen.test.commons import get_or_create_classification

from box_sdk_gen.schemas.classification_template import ClassificationTemplate

client: BoxClient = get_default_client()


def get_or_create_second_classification(
    classification_template: ClassificationTemplate,
) -> ClassificationTemplateFieldsOptionsField:
    classifications: List[ClassificationTemplateFieldsOptionsField] = (
        classification_template.fields[0].options
    )
    current_number_of_classifications: int = len(classifications)
    if current_number_of_classifications == 1:
        classification_template_with_new_classification: ClassificationTemplate = (
            client.classifications.add_classification(
                [
                    AddClassificationRequestBody(
                        data=AddClassificationRequestBodyDataField(
                            key=get_uuid(),
                            static_config=AddClassificationRequestBodyDataStaticConfigField(
                                classification=AddClassificationRequestBodyDataStaticConfigClassificationField(
                                    color_id=4,
                                    classification_definition='Other description',
                                )
                            ),
                        )
                    )
                ]
            )
        )
        return classification_template_with_new_classification.fields[0].options[1]
    return classifications[1]


def testFileClassifications():
    classification_template: ClassificationTemplate = (
        get_or_create_classification_template()
    )
    classification: ClassificationTemplateFieldsOptionsField = (
        get_or_create_classification(classification_template)
    )
    file: FileFull = upload_new_file()
    with pytest.raises(Exception):
        client.file_classifications.get_classification_on_file(file.id)
    created_file_classification: Classification = (
        client.file_classifications.add_classification_to_file(
            file.id, box_security_classification_key=classification.key
        )
    )
    assert (
        created_file_classification.box_security_classification_key
        == classification.key
    )
    file_classification: Classification = (
        client.file_classifications.get_classification_on_file(file.id)
    )
    assert file_classification.box_security_classification_key == classification.key
    second_classification: ClassificationTemplateFieldsOptionsField = (
        get_or_create_second_classification(classification_template)
    )
    updated_file_classification: Classification = (
        client.file_classifications.update_classification_on_file(
            file.id,
            [UpdateClassificationOnFileRequestBody(value=second_classification.key)],
        )
    )
    assert (
        updated_file_classification.box_security_classification_key
        == second_classification.key
    )
    client.file_classifications.delete_classification_from_file(file.id)
    with pytest.raises(Exception):
        client.file_classifications.get_classification_on_file(file.id)
    client.files.delete_file_by_id(file.id)

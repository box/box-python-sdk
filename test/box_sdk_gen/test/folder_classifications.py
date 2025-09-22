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

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.classification import Classification

from box_sdk_gen.managers.folder_classifications import (
    UpdateClassificationOnFolderRequestBody,
)

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

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


def testFolderClassifications():
    classification_template: ClassificationTemplate = (
        get_or_create_classification_template()
    )
    classification: ClassificationTemplateFieldsOptionsField = (
        get_or_create_classification(classification_template)
    )
    folder: FolderFull = create_new_folder()
    with pytest.raises(Exception):
        client.folder_classifications.get_classification_on_folder(folder.id)
    created_folder_classification: Classification = (
        client.folder_classifications.add_classification_to_folder(
            folder.id, box_security_classification_key=classification.key
        )
    )
    assert (
        created_folder_classification.box_security_classification_key
        == classification.key
    )
    folder_classification: Classification = (
        client.folder_classifications.get_classification_on_folder(folder.id)
    )
    assert folder_classification.box_security_classification_key == classification.key
    second_classification: ClassificationTemplateFieldsOptionsField = (
        get_or_create_second_classification(classification_template)
    )
    updated_folder_classification: Classification = (
        client.folder_classifications.update_classification_on_folder(
            folder.id,
            [UpdateClassificationOnFolderRequestBody(value=second_classification.key)],
        )
    )
    assert (
        updated_folder_classification.box_security_classification_key
        == second_classification.key
    )
    client.folder_classifications.delete_classification_from_folder(folder.id)
    with pytest.raises(Exception):
        client.folder_classifications.get_classification_on_folder(folder.id)
    client.folders.delete_folder_by_id(folder.id)

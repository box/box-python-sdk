from typing import List

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.classification_template import (
    ClassificationTemplateFieldsOptionsField,
)

from box_sdk_gen.managers.classifications import UpdateClassificationRequestBody

from box_sdk_gen.managers.classifications import (
    UpdateClassificationRequestBodyDataField,
)

from box_sdk_gen.managers.classifications import (
    UpdateClassificationRequestBodyDataStaticConfigField,
)

from box_sdk_gen.managers.classifications import (
    UpdateClassificationRequestBodyDataStaticConfigClassificationField,
)

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_or_create_classification_template

from test.box_sdk_gen.test.commons import get_or_create_classification

from box_sdk_gen.schemas.classification_template import ClassificationTemplate

client: BoxClient = get_default_client()


def testClassifications():
    classification_template: ClassificationTemplate = (
        get_or_create_classification_template()
    )
    classification: ClassificationTemplateFieldsOptionsField = (
        get_or_create_classification(classification_template)
    )
    assert not classification.key == ''
    assert not classification.static_config.classification.color_id == 100
    assert (
        not classification.static_config.classification.classification_definition == ''
    )
    updated_classification_name: str = get_uuid()
    updated_classification_description: str = get_uuid()
    classification_template_with_updated_classification: ClassificationTemplate = (
        client.classifications.update_classification(
            [
                UpdateClassificationRequestBody(
                    enum_option_key=classification.key,
                    data=UpdateClassificationRequestBodyDataField(
                        key=updated_classification_name,
                        static_config=UpdateClassificationRequestBodyDataStaticConfigField(
                            classification=UpdateClassificationRequestBodyDataStaticConfigClassificationField(
                                color_id=2,
                                classification_definition=updated_classification_description,
                            )
                        ),
                    ),
                )
            ]
        )
    )
    updated_classifications: List[ClassificationTemplateFieldsOptionsField] = (
        classification_template_with_updated_classification.fields[0].options
    )
    updated_classification: ClassificationTemplateFieldsOptionsField = (
        updated_classifications[0]
    )
    assert updated_classification.key == updated_classification_name
    assert updated_classification.static_config.classification.color_id == 2
    assert (
        updated_classification.static_config.classification.classification_definition
        == updated_classification_description
    )

from boxsdk.pagination.box_object_collection import BoxObjectCollection

from test.boxsdk.integration_new import CLIENT


def test_get_sign_templates():
    sign_templates = CLIENT.get_sign_templates()
    assert isinstance(sign_templates, BoxObjectCollection)

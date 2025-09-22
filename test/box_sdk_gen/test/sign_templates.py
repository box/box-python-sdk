from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.sign_templates import SignTemplates

from box_sdk_gen.schemas.sign_template import SignTemplate

from box_sdk_gen.internal.utils import decode_base_64

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject


def testGetSignTemplates():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    sign_templates: SignTemplates = client.sign_templates.get_sign_templates(limit=2)
    assert len(sign_templates.entries) >= 0


def testGetSignTemplate():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    sign_templates: SignTemplates = client.sign_templates.get_sign_templates(limit=2)
    assert len(sign_templates.entries) >= 0
    if len(sign_templates.entries) > 0:
        sign_template: SignTemplate = client.sign_templates.get_sign_template_by_id(
            sign_templates.entries[0].id
        )
        assert sign_template.id == sign_templates.entries[0].id
        assert len(sign_template.source_files) > 0
        assert not sign_template.name == ''
        assert not sign_template.parent_folder.id == ''

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.v2025_r0.doc_gen_template_base_v2025_r0 import (
    DocGenTemplateBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_templates_v2025_r0 import (
    DocGenTemplatesV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_template_v2025_r0 import DocGenTemplateV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_tags_v2025_r0 import DocGenTagsV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_jobs_v2025_r0 import DocGenJobsV2025R0

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testDocgenTemplateCRUD():
    file: FileFull = upload_new_file()
    created_docgen_template: DocGenTemplateBaseV2025R0 = (
        client.docgen_template.create_docgen_template_v2025_r0(
            FileReferenceV2025R0(id=file.id)
        )
    )
    docgen_templates: DocGenTemplatesV2025R0 = (
        client.docgen_template.get_docgen_templates_v2025_r0()
    )
    assert len(docgen_templates.entries) > 0
    fetched_docgen_template: DocGenTemplateV2025R0 = (
        client.docgen_template.get_docgen_template_by_id_v2025_r0(
            created_docgen_template.file.id
        )
    )
    assert fetched_docgen_template.file.id == created_docgen_template.file.id
    docgen_template_tags: DocGenTagsV2025R0 = (
        client.docgen_template.get_docgen_template_tags_v2025_r0(
            fetched_docgen_template.file.id
        )
    )
    docgen_template_jobs: DocGenJobsV2025R0 = (
        client.docgen_template.get_docgen_template_job_by_id_v2025_r0(
            fetched_docgen_template.file.id
        )
    )
    assert len(docgen_template_jobs.entries) == 0
    client.docgen_template.delete_docgen_template_by_id_v2025_r0(
        created_docgen_template.file.id
    )
    client.files.delete_file_by_id(file.id)

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.v2025_r0.doc_gen_template_base_v2025_r0 import (
    DocGenTemplateBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_batch_base_v2025_r0 import (
    DocGenBatchBaseV2025R0,
)

from box_sdk_gen.managers.docgen import CreateDocgenBatchV2025R0DestinationFolder

from box_sdk_gen.schemas.v2025_r0.doc_gen_document_generation_data_v2025_r0 import (
    DocGenDocumentGenerationDataV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_jobs_v2025_r0 import DocGenJobsV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_jobs_full_v2025_r0 import (
    DocGenJobsFullV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_full_v2025_r0 import DocGenJobFullV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_v2025_r0 import DocGenJobV2025R0

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import create_new_folder

client: BoxClient = get_default_client()


def testDocgenBatchAndJobs():
    uploaded_file: FileFull = upload_new_file()
    folder: FolderFull = create_new_folder()
    created_docgen_template: DocGenTemplateBaseV2025R0 = (
        client.docgen_template.create_docgen_template_v2025_r0(
            FileReferenceV2025R0(id=uploaded_file.id)
        )
    )
    docgen_batch: DocGenBatchBaseV2025R0 = client.docgen.create_docgen_batch_v2025_r0(
        FileReferenceV2025R0(id=uploaded_file.id),
        'api',
        CreateDocgenBatchV2025R0DestinationFolder(id=folder.id),
        'pdf',
        [
            DocGenDocumentGenerationDataV2025R0(
                generated_file_name='test', user_input={'abc': 'xyz'}
            )
        ],
    )
    assert not docgen_batch.id == ''
    assert to_string(docgen_batch.type) == 'docgen_batch'
    docgen_batch_jobs: DocGenJobsV2025R0 = (
        client.docgen.get_docgen_batch_job_by_id_v2025_r0(docgen_batch.id)
    )
    assert len(docgen_batch_jobs.entries) >= 1
    assert not docgen_batch_jobs.entries[0].id == ''
    assert to_string(docgen_batch_jobs.entries[0].type) == 'docgen_job'
    assert docgen_batch_jobs.entries[0].output_type == 'pdf'
    assert not to_string(docgen_batch_jobs.entries[0].status) == ''
    assert docgen_batch_jobs.entries[0].template_file.id == uploaded_file.id
    assert docgen_batch_jobs.entries[0].batch.id == docgen_batch.id
    docgen_jobs: DocGenJobsFullV2025R0 = client.docgen.get_docgen_jobs_v2025_r0(
        limit=10000
    )
    assert len(docgen_jobs.entries) >= 1
    assert not docgen_jobs.entries[0].batch.id == ''
    assert not docgen_jobs.entries[0].created_by.id == ''
    assert not docgen_jobs.entries[0].enterprise.id == ''
    assert not docgen_jobs.entries[0].id == ''
    assert not docgen_jobs.entries[0].output_type == ''
    assert not docgen_jobs.entries[0].source == ''
    assert not to_string(docgen_jobs.entries[0].status) == ''
    assert to_string(docgen_jobs.entries[0].template_file.type) == 'file'
    assert not docgen_jobs.entries[0].template_file.id == ''
    assert (
        to_string(docgen_jobs.entries[0].template_file_version.type) == 'file_version'
    )
    assert not docgen_jobs.entries[0].template_file_version.id == ''
    assert to_string(docgen_jobs.entries[0].type) == 'docgen_job'
    index_of_item: int = len(docgen_jobs.entries) - 1
    docgen_job_item_from_list: DocGenJobFullV2025R0 = docgen_jobs.entries[index_of_item]
    docgen_job: DocGenJobV2025R0 = client.docgen.get_docgen_job_by_id_v2025_r0(
        docgen_job_item_from_list.id
    )
    assert not docgen_job.batch.id == ''
    assert not docgen_job.id == ''
    assert not docgen_job.output_type == ''
    assert not to_string(docgen_job.status) == ''
    assert to_string(docgen_job.template_file.type) == 'file'
    assert not docgen_job.template_file.id == ''
    assert to_string(docgen_job.template_file_version.type) == 'file_version'
    assert not docgen_job.template_file_version.id == ''
    assert to_string(docgen_job.type) == 'docgen_job'
    client.folders.delete_folder_by_id(folder.id)
    client.files.delete_file_by_id(uploaded_file.id)

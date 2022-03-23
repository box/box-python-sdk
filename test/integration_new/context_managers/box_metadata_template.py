from typing import Any, Iterable

from boxsdk.object.metadata_template import MetadataTemplate, MetadataField, MetadataFieldType
from test.integration_new import CLIENT


class BoxTestMetadataTemplate:

    def __init__(self, *, display_name: str, fields: Iterable = None):
        if fields is None:
            fields = []
        self._metadata_template: MetadataTemplate = CLIENT.create_metadata_template(display_name=display_name, fields=fields)

    def __enter__(self) -> MetadataTemplate:
        return self._metadata_template

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._metadata_template.delete()

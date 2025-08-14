from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.schemas.keyword_skill_card import KeywordSkillCard

from box_sdk_gen.schemas.timeline_skill_card import TimelineSkillCard

from box_sdk_gen.schemas.transcript_skill_card import TranscriptSkillCard

from box_sdk_gen.schemas.status_skill_card import StatusSkillCard

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.skill_cards_metadata import SkillCardsMetadata

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.skill_card import SkillCard

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class UpdateBoxSkillCardsOnFileRequestBodyOpField(str, Enum):
    REPLACE = 'replace'


class UpdateBoxSkillCardsOnFileRequestBody(BaseObject):
    def __init__(
        self,
        *,
        op: Optional[UpdateBoxSkillCardsOnFileRequestBodyOpField] = None,
        path: Optional[str] = None,
        value: Optional[SkillCard] = None,
        **kwargs
    ):
        """
                :param op: The value will always be `replace`., defaults to None
                :type op: Optional[UpdateBoxSkillCardsOnFileRequestBodyOpField], optional
                :param path: The JSON Path that represents the card to replace. In most cases
        this will be in the format `/cards/{index}` where `index` is the
        zero-indexed position of the card in the list of cards., defaults to None
                :type path: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.op = op
        self.path = path
        self.value = value


class UpdateAllSkillCardsOnFileStatus(str, Enum):
    INVOKED = 'invoked'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    TRANSIENT_FAILURE = 'transient_failure'
    PERMANENT_FAILURE = 'permanent_failure'


class UpdateAllSkillCardsOnFileMetadata(BaseObject):
    def __init__(self, *, cards: Optional[List[SkillCard]] = None, **kwargs):
        """
        :param cards: A list of Box Skill cards to apply to this file., defaults to None
        :type cards: Optional[List[SkillCard]], optional
        """
        super().__init__(**kwargs)
        self.cards = cards


class UpdateAllSkillCardsOnFileFileTypeField(str, Enum):
    FILE = 'file'


class UpdateAllSkillCardsOnFileFile(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        *,
        type: Optional[UpdateAllSkillCardsOnFileFileTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `file`., defaults to None
        :type type: Optional[UpdateAllSkillCardsOnFileFileTypeField], optional
        :param id: The ID of the file., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class UpdateAllSkillCardsOnFileFileVersionTypeField(str, Enum):
    FILE_VERSION = 'file_version'


class UpdateAllSkillCardsOnFileFileVersion(BaseObject):
    _discriminator = 'type', {'file_version'}

    def __init__(
        self,
        *,
        type: Optional[UpdateAllSkillCardsOnFileFileVersionTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `file_version`., defaults to None
        :type type: Optional[UpdateAllSkillCardsOnFileFileVersionTypeField], optional
        :param id: The ID of the file version., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class UpdateAllSkillCardsOnFileUsage(BaseObject):
    def __init__(
        self, *, unit: Optional[str] = None, value: Optional[float] = None, **kwargs
    ):
        """
        :param unit: The value will always be `file`., defaults to None
        :type unit: Optional[str], optional
        :param value: Number of resources affected., defaults to None
        :type value: Optional[float], optional
        """
        super().__init__(**kwargs)
        self.unit = unit
        self.value = value


class SkillsManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_box_skill_cards_on_file(
        self, file_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SkillCardsMetadata:
        """
                List the Box Skills metadata cards that are attached to a file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/global/boxSkillsCards',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SkillCardsMetadata)

    def create_box_skill_cards_on_file(
        self,
        file_id: str,
        cards: List[SkillCard],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SkillCardsMetadata:
        """
                Applies one or more Box Skills metadata cards to a file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param cards: A list of Box Skill cards to apply to this file.
                :type cards: List[SkillCard]
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'cards': cards}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/global/boxSkillsCards',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SkillCardsMetadata)

    def update_box_skill_cards_on_file(
        self,
        file_id: str,
        request_body: List[UpdateBoxSkillCardsOnFileRequestBody],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SkillCardsMetadata:
        """
                Updates one or more Box Skills metadata cards to a file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param request_body: Request body of updateBoxSkillCardsOnFile method
                :type request_body: List[UpdateBoxSkillCardsOnFileRequestBody]
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/global/boxSkillsCards',
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json-patch+json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SkillCardsMetadata)

    def delete_box_skill_cards_from_file(
        self, file_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes any Box Skills cards metadata from a file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/global/boxSkillsCards',
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def update_all_skill_cards_on_file(
        self,
        skill_id: str,
        status: UpdateAllSkillCardsOnFileStatus,
        metadata: UpdateAllSkillCardsOnFileMetadata,
        file: UpdateAllSkillCardsOnFileFile,
        *,
        file_version: Optional[UpdateAllSkillCardsOnFileFileVersion] = None,
        usage: Optional[UpdateAllSkillCardsOnFileUsage] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                An alternative method that can be used to overwrite and update all Box Skill

                metadata cards on a file.

                :param skill_id: The ID of the skill to apply this metadata for.
        Example: "33243242"
                :type skill_id: str
                :param status: Defines the status of this invocation. Set this to `success` when setting Skill cards.
                :type status: UpdateAllSkillCardsOnFileStatus
                :param metadata: The metadata to set for this skill. This is a list of
        Box Skills cards. These cards will overwrite any existing Box
        skill cards on the file.
                :type metadata: UpdateAllSkillCardsOnFileMetadata
                :param file: The file to assign the cards to.
                :type file: UpdateAllSkillCardsOnFileFile
                :param file_version: The optional file version to assign the cards to., defaults to None
                :type file_version: Optional[UpdateAllSkillCardsOnFileFileVersion], optional
                :param usage: A descriptor that defines what items are affected by this call.

        Set this to the default values when setting a card to a `success`
        state, and leave it out in most other situations., defaults to None
                :type usage: Optional[UpdateAllSkillCardsOnFileUsage], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'status': status,
            'metadata': metadata,
            'file': file,
            'file_version': file_version,
            'usage': usage,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/skill_invocations/',
                        to_string(skill_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

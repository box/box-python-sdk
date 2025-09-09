from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from typing import List

from box_sdk_gen.internal.null_value import NullValue

from typing import Union

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.sign_request_create_signer import SignRequestCreateSigner

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.sign_request_prefill_tag import SignRequestPrefillTag

from box_sdk_gen.schemas.sign_request import SignRequest

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.sign_requests import SignRequests

from box_sdk_gen.schemas.sign_request_create_request import SignRequestCreateRequest

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


class CreateSignRequestSignatureColor(str, Enum):
    BLUE = 'blue'
    BLACK = 'black'
    RED = 'red'


class SignRequestsManager:
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

    def cancel_sign_request(
        self,
        sign_request_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SignRequest:
        """
                Cancels a sign request.
                :param sign_request_id: The ID of the signature request.
        Example: "33243242"
                :type sign_request_id: str
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
                        '/2.0/sign_requests/',
                        to_string(sign_request_id),
                        '/cancel',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SignRequest)

    def resend_sign_request(
        self,
        sign_request_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Resends a signature request email to all outstanding signers.
                :param sign_request_id: The ID of the signature request.
        Example: "33243242"
                :type sign_request_id: str
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
                        '/2.0/sign_requests/',
                        to_string(sign_request_id),
                        '/resend',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def get_sign_request_by_id(
        self,
        sign_request_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SignRequest:
        """
                Gets a sign request by ID.
                :param sign_request_id: The ID of the signature request.
        Example: "33243242"
                :type sign_request_id: str
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
                        '/2.0/sign_requests/',
                        to_string(sign_request_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SignRequest)

    def get_sign_requests(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        senders: Optional[List[str]] = None,
        shared_requests: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SignRequests:
        """
                Gets signature requests created by a user. If the `sign_files` and/or

                `parent_folder` are deleted, the signature request will not return in the list.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param senders: A list of sender emails to filter the signature requests by sender.
        If provided, `shared_requests` must be set to `true`., defaults to None
                :type senders: Optional[List[str]], optional
                :param shared_requests: If set to `true`, only includes requests that user is not an owner,
        but user is a collaborator. Collaborator access is determined by the
        user access level of the sign files of the request.
        Default is `false`. Must be set to `true` if `senders` are provided., defaults to None
                :type shared_requests: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'marker': to_string(marker),
                'limit': to_string(limit),
                'senders': to_string(senders),
                'shared_requests': to_string(shared_requests),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/sign_requests']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, SignRequests)

    def create_sign_request(
        self,
        signers: List[SignRequestCreateSigner],
        *,
        source_files: Union[Optional[List[FileBase]], NullValue] = None,
        signature_color: Union[
            Optional[CreateSignRequestSignatureColor], NullValue
        ] = None,
        parent_folder: Optional[FolderMini] = None,
        is_document_preparation_needed: Optional[bool] = None,
        redirect_url: Union[Optional[str], NullValue] = None,
        declined_redirect_url: Union[Optional[str], NullValue] = None,
        are_text_signatures_enabled: Optional[bool] = None,
        email_subject: Union[Optional[str], NullValue] = None,
        email_message: Union[Optional[str], NullValue] = None,
        are_reminders_enabled: Optional[bool] = None,
        name: Optional[str] = None,
        prefill_tags: Optional[List[SignRequestPrefillTag]] = None,
        days_valid: Union[Optional[int], NullValue] = None,
        external_id: Union[Optional[str], NullValue] = None,
        template_id: Union[Optional[str], NullValue] = None,
        external_system_name: Union[Optional[str], NullValue] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> SignRequest:
        """
                Creates a signature request. This involves preparing a document for signing and

                sending the signature request to signers.

                :param signers: Array of signers for the signature request. 35 is the
        max number of signers permitted.

        **Note**: It may happen that some signers belong to conflicting [segments](r://shield-information-barrier-segment-member) (user groups).
        This means that due to the security policies, users are assigned to segments to prevent exchanges or communication that could lead to ethical conflicts.
        In such a case, an attempt to send the sign request will result in an error.

        Read more about [segments and ethical walls](https://support.box.com/hc/en-us/articles/9920431507603-Understanding-Information-Barriers#h_01GFVJEHQA06N7XEZ4GCZ9GFAQ).
                :type signers: List[SignRequestCreateSigner]
                :param source_files: List of files to create a signing document from. This is currently limited to ten files. Only the ID and type fields are required for each file., defaults to None
                :type source_files: Union[Optional[List[FileBase]], NullValue], optional
                :param signature_color: Force a specific color for the signature (blue, black, or red)., defaults to None
                :type signature_color: Union[Optional[CreateSignRequestSignatureColor], NullValue], optional
                :param is_document_preparation_needed: Indicates if the sender should receive a `prepare_url` in the response to complete document preparation using the UI., defaults to None
                :type is_document_preparation_needed: Optional[bool], optional
                :param redirect_url: When specified, the signature request will be redirected to this url when a document is signed., defaults to None
                :type redirect_url: Union[Optional[str], NullValue], optional
                :param declined_redirect_url: The uri that a signer will be redirected to after declining to sign a document., defaults to None
                :type declined_redirect_url: Union[Optional[str], NullValue], optional
                :param are_text_signatures_enabled: Disables the usage of signatures generated by typing (text)., defaults to None
                :type are_text_signatures_enabled: Optional[bool], optional
                :param email_subject: Subject of sign request email. This is cleaned by sign request. If this field is not passed, a default subject will be used., defaults to None
                :type email_subject: Union[Optional[str], NullValue], optional
                :param email_message: Message to include in sign request email. The field is cleaned through sanitization of specific characters. However, some html tags are allowed. Links included in the message are also converted to hyperlinks in the email. The message may contain the following html tags including `a`, `abbr`, `acronym`, `b`, `blockquote`, `code`, `em`, `i`, `ul`, `li`, `ol`, and `strong`. Be aware that when the text to html ratio is too high, the email may end up in spam filters. Custom styles on these tags are not allowed. If this field is not passed, a default message will be used., defaults to None
                :type email_message: Union[Optional[str], NullValue], optional
                :param are_reminders_enabled: Reminds signers to sign a document on day 3, 8, 13 and 18. Reminders are only sent to outstanding signers., defaults to None
                :type are_reminders_enabled: Optional[bool], optional
                :param name: Name of the signature request., defaults to None
                :type name: Optional[str], optional
                :param prefill_tags: When a document contains sign-related tags in the content, you can prefill them using this `prefill_tags` by referencing the 'id' of the tag as the `external_id` field of the prefill tag., defaults to None
                :type prefill_tags: Optional[List[SignRequestPrefillTag]], optional
                :param days_valid: Set the number of days after which the created signature request will automatically expire if not completed. By default, we do not apply any expiration date on signature requests, and the signature request does not expire., defaults to None
                :type days_valid: Union[Optional[int], NullValue], optional
                :param external_id: This can be used to reference an ID in an external system that the sign request is related to., defaults to None
                :type external_id: Union[Optional[str], NullValue], optional
                :param template_id: When a signature request is created from a template this field will indicate the id of that template., defaults to None
                :type template_id: Union[Optional[str], NullValue], optional
                :param external_system_name: Used as an optional system name to appear in the signature log next to the signers who have been assigned the `embed_url_external_id`., defaults to None
                :type external_system_name: Union[Optional[str], NullValue], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'source_files': source_files,
            'signature_color': signature_color,
            'signers': signers,
            'parent_folder': parent_folder,
            'is_document_preparation_needed': is_document_preparation_needed,
            'redirect_url': redirect_url,
            'declined_redirect_url': declined_redirect_url,
            'are_text_signatures_enabled': are_text_signatures_enabled,
            'email_subject': email_subject,
            'email_message': email_message,
            'are_reminders_enabled': are_reminders_enabled,
            'name': name,
            'prefill_tags': prefill_tags,
            'days_valid': days_valid,
            'external_id': external_id,
            'template_id': template_id,
            'external_system_name': external_system_name,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/sign_requests']
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
        return deserialize(response.data, SignRequest)

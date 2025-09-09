from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.zip_download import ZipDownload

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.zip_download_request import ZipDownloadRequest

from box_sdk_gen.schemas.zip_download_status import ZipDownloadStatus

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.serialization.json import sd_to_json


class CreateZipDownloadItemsTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class CreateZipDownloadItems(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(self, type: CreateZipDownloadItemsTypeField, id: str, **kwargs):
        """
                :param type: The type of the item to add to the archive.
                :type type: CreateZipDownloadItemsTypeField
                :param id: The identifier of the item to add to the archive. When this item is
        a folder then this can not be the root folder with ID `0`.
                :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class DownloadZipItemsTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class DownloadZipItems(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(self, type: DownloadZipItemsTypeField, id: str, **kwargs):
        """
                :param type: The type of the item to add to the archive.
                :type type: DownloadZipItemsTypeField
                :param id: The identifier of the item to add to the archive. When this item is
        a folder then this can not be the root folder with ID `0`.
                :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class ZipDownloadsManager:
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

    def create_zip_download(
        self,
        items: List[CreateZipDownloadItems],
        *,
        download_file_name: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ZipDownload:
        """
                Creates a request to download multiple files and folders as a single `zip`

                archive file. This API does not return the archive but instead performs all


                the checks to ensure that the user has access to all the items, and then


                returns a `download_url` and a `status_url` that can be used to download the


                archive.


                The limit for an archive is either the Account's upload limit or


                10,000 files, whichever is met first.


                **Note**: Downloading a large file can be


                affected by various


                factors such as distance, network latency,


                bandwidth, and congestion, as well as packet loss


                ratio and current server load.


                For these reasons we recommend that a maximum ZIP archive


                total size does not exceed 25GB.

                :param items: A list of items to add to the `zip` archive. These can
        be folders or files.
                :type items: List[CreateZipDownloadItems]
                :param download_file_name: The optional name of the `zip` archive. This name will be appended by the
        `.zip` file extension, for example `January Financials.zip`., defaults to None
                :type download_file_name: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'items': items, 'download_file_name': download_file_name}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/zip_downloads']
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
        return deserialize(response.data, ZipDownload)

    def get_zip_download_content(
        self,
        download_url: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ByteStream:
        """
               Returns the contents of a `zip` archive in binary format. This URL does not

               require any form of authentication and could be used in a user's browser to


               download the archive to a user's device.


               By default, this URL is only valid for a few seconds from the creation of


               the request for this archive. Once a download has started it can not be


               stopped and resumed, instead a new request for a zip archive would need to


               be created.


               The URL of this endpoint should not be considered as fixed. Instead, use


               the [Create zip download](e://post_zip_downloads) API to request to create a


               `zip` archive, and then follow the `download_url` field in the response to


               this endpoint.

               :param download_url: The URL that can be used to download created `zip` archive.
        Example: `https://dl.boxcloud.com/2.0/zip_downloads/29l00nfxDyHOt7RphI9zT_w==nDnZEDjY2S8iEWWCHEEiptFxwoWojjlibZjJ6geuE5xnXENDTPxzgbks_yY=/content`
               :type download_url: str
               :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
               :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=download_url,
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.BINARY,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return response.content

    def get_zip_download_status(
        self,
        status_url: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ZipDownloadStatus:
        """
               Returns the download status of a `zip` archive, allowing an application to

               inspect the progress of the download as well as the number of items that


               might have been skipped.


               This endpoint can only be accessed once the download has started.


               Subsequently this endpoint is valid for 12 hours from the start of the


               download.


               The URL of this endpoint should not be considered as fixed. Instead, use


               the [Create zip download](e://post_zip_downloads) API to request to create a


               `zip` archive, and then follow the `status_url` field in the response to


               this endpoint.

               :param status_url: The URL that can be used to get the status of the `zip` archive being downloaded.
        Example: `https://dl.boxcloud.com/2.0/zip_downloads/29l00nfxDyHOt7RphI9zT_w==nDnZEDjY2S8iEWWCHEEiptFxwoWojjlibZjJ6geuE5xnXENDTPxzgbks_yY=/status`
               :type status_url: str
               :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
               :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=status_url,
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ZipDownloadStatus)

    def download_zip(
        self,
        items: List[DownloadZipItems],
        *,
        download_file_name: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ByteStream:
        """
                Creates a zip and downloads its content
                :param items: A list of items to add to the `zip` archive. These can
        be folders or files.
                :type items: List[DownloadZipItems]
                :param download_file_name: The optional name of the `zip` archive. This name will be appended by the
        `.zip` file extension, for example `January Financials.zip`., defaults to None
                :type download_file_name: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'items': items, 'download_file_name': download_file_name}
        zip_download_session: ZipDownload = self.create_zip_download(
            items, download_file_name=download_file_name, extra_headers=extra_headers
        )
        return self.get_zip_download_content(
            zip_download_session.download_url, extra_headers=extra_headers
        )

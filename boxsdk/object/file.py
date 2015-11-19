# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API
from .item import Item
from .metadata import Metadata
from boxsdk.util.api_response_decorator import api_response, promisify


class File(Item):
    """Box API endpoint for interacting with files."""

    _item_type = 'file'

    def preflight_check(self, size, name=None):
        """
        Make an API call to check if the file can be updated with the new name and size of the file.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be updated. It's optional, if the name is not being changed.
        :type name:
            `unicode`
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        self._preflight_check(
            size=size,
            name=name,
            file_id=self._object_id,
        )

    def _get_accelerator_upload_url_for_update(self):
        """
        Get Accelerator upload url for updating the file.

        :return:
            The Accelerator upload url for updating the file or None if cannot get one
        :rtype:
            `unicode` or None
        """
        return self._get_accelerator_upload_url(file_id=self._object_id)

    @api_response
    def content(self):
        """
        Get the content of a file on Box.

        :returns:
            File content as bytes.
        :rtype:
            `bytes`
        """
        url = self.get_url('content')
        return self._session.get(url, expect_json_response=False)

    @content.translator
    def content(self, response):
        """
        Translate the response into the file content.
        """
        return response.content

    @api_response
    def download_to(self, writeable_stream):
        """
        Download the file; write it to the given stream.

        :param writeable_stream:
            A file-like object where bytes can be written into.
        :type writeable_stream:
            `file`
        """
        # pylint:disable=unused-argument
        url = self.get_url('content')
        return self._session.get(url, expect_json_response=False, stream=True)

    @download_to.translator
    def download_to(self, response):
        """
        Translate the response into writing the downloaded chunks to the supplied stream.
        """
        for chunk in response.network_response.response_as_stream.stream(decode_content=True):
            writeable_stream = response.kwargs.pop('writeable_stream', None) or response.args[-1]
            writeable_stream.write(chunk)

    @api_response
    def update_contents_with_stream(
            self,
            file_stream,
            etag=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """
        Upload a new version of a file, taking the contents from the given file stream.

        :param file_stream:
            The file-like object containing the bytes
        :type file_stream:
            `file`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :type preflight_check:
            `bool`
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :type preflight_expected_size:
            `int`
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :type upload_using_accelerator:
            `bool`
        :returns:
            A new file object
        :rtype:
            :class:`File`
        :raises:
            :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file or preflight
            check fails.
        """
        files = {'file': ('unused', file_stream)}
        headers = {'If-Match': etag} if etag is not None else None
        url = self.get_url('content').replace(API.BASE_API_URL, API.UPLOAD_URL)

        preflight_promise = promisify(not preflight_check or self.preflight_check(size=preflight_expected_size))
        accelerator_promise = promisify(
            self._get_accelerator_upload_url_for_update() if upload_using_accelerator else None,
        )

        def do_upload(accelerator_upload_url):
            response = self._session.post(
                accelerator_upload_url or url,
                expect_json_response=False,
                files=files,
                headers=headers,
            )
            return promisify(response)

        return preflight_promise.then(lambda _: accelerator_promise).then(do_upload)

    @update_contents_with_stream.translator
    def update_contents_with_stream(self, response):
        """
        Translate the response into a File object.
        """
        return File(
            session=self._session,
            object_id=self._object_id,
            response_object=response.json(),
        )

    def update_contents(
            self,
            file_path,
            etag=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """Upload a new version of a file. The contents are taken from the given file path.

        :param file_path:
            The path of the file that should be uploaded.
        :type file_path:
            `unicode`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :type preflight_check:
            `bool`
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :type preflight_expected_size:
            `int`
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :type upload_using_accelerator:
            `bool`
        :returns:
            A new file object
        :rtype:
            :class:`File`
        :raises:
            :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file or preflight
            check fails.
        """
        with open(file_path, 'rb') as file_stream:
            return self.update_contents_with_stream(
                file_stream,
                etag,
                preflight_check,
                preflight_expected_size=preflight_expected_size,
                upload_using_accelerator=upload_using_accelerator,
            )

    def lock(self, prevent_download=False):
        """
        Lock a file, preventing others from modifying (or possibly even downloading) it.

        :param prevent_download:
            Whether or not the lock should prevent other users from downloading the file.
        :type prevent_download:
            `bool`
        :return:
            A new :class:`File` instance reflecting that the file has been locked.
        :rtype:
            :class:`File`
        """
        data = {
            'lock': {
                'is_download_prevented': prevent_download,
                'type': 'lock',
            }
        }
        return self.update_info(data)

    def unlock(self):
        """
        Unlock a file, releasing any restrictions that the lock maintained.

        :return:
            A new :class:`File` instance reflecting that the file has been unlocked.
        :rtype:
            :class:`File`
        """
        data = {'lock': None}
        return self.update_info(data)

    def metadata(self, scope='global', template='properties'):
        """
        Instantiate a :class:`Metadata` object associated with this file.

        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :type scope:
            `unicode`
        :param template:
            The name of the metadata template. See https://developers.box.com/metadata-api/#basics for more details.
        :type template:
            `unicode`
        :return:
            A new metadata instance associated with this file.
        :rtype:
            :class:`Metadata`
        """
        return Metadata(self._session, self, scope, template)

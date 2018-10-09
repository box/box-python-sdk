# coding: utf-8

from __future__ import unicode_literals

from collections import OrderedDict

from requests_toolbelt.multipart.encoder import MultipartEncoder


class MultipartStream(MultipartEncoder):
    """
    Subclass of the requests_toolbelt's :class:`MultipartEncoder` that ensures that data
    is encoded before files. This allows a server to process information in the data before
    receiving the file bytes.
    """
    def __init__(self, data, files):
        fields = OrderedDict()
        for k in data:
            fields[k] = data[k]
        for k in files:
            fields[k] = files[k]
        super(MultipartStream, self).__init__(fields)

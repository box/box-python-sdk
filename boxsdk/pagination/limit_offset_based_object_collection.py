# coding: utf-8

from __future__ import unicode_literals

from .box_object_collection import BoxObjectCollection


class LimitOffsetBasedObjectCollection(BoxObjectCollection):
    """
    An iterator of Box objects (BaseObjects) that were retrieved from a Box API endpoint that supports
    limit-offset type of pagination.

    See https://developer.box.com/reference#pagination for more details.
    """

    def __init__(
            self,
            session,
            url,
            limit=None,
            fields=None,
            additional_params=None,
            return_full_pages=False,
            offset=0,
    ):
        """
        :param offset:
            The offset index to start paging from.
        :type offset:
            `int`
        """
        super(LimitOffsetBasedObjectCollection, self).__init__(
            session,
            url,
            limit=limit,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=return_full_pages,
        )
        self._offset = offset

    def _update_pointer_to_next_page(self, response_object):
        """Baseclass override."""
        total_count = response_object['total_count']

        # The API might use a lower limit than the client asked for, if the
        # client asked for a limit above the maximum limit for that endpoint.
        # The API is supposed to respond with the limit that it actually used.
        # If that is given, then use that limit for the offset calculation, and
        # also for the remainder of the paging.
        #
        # Similarly, the API reports the offset that it used. In theory, this
        # should always be the same as what was requested. But just in case, do
        # the same thing with offset.
        if 'limit' in response_object:
            self._limit, old_limit = int(response_object['limit']), self._limit

            # If the API erroneously sends a bad value for limit, we want to
            # avoid getting into an infinite chain of API calls. So abort with
            # a runtime error.
            if self._limit <= 0 < old_limit:
                self._offset = total_count  # Disable additional paging.
                raise RuntimeError('API returned limit={0}, cannot continue paging'.format(self._limit))

        if 'offset' in response_object:
            self._offset = int(response_object['offset'])

        if total_count >= self._offset + self._limit:
            self._offset += self._limit
        else:
            self._offset = total_count

    def _has_more_pages(self, response_object):
        """Baseclass override."""
        return self._offset < response_object['total_count']

    def _next_page_pointer_params(self):
        """Baseclass override."""
        return {'offset': self._offset}

    def next_pointer(self):
        """Baseclass override."""
        return self._offset

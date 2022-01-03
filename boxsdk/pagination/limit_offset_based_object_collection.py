# coding: utf-8
from typing import Optional, Iterator, TYPE_CHECKING

from .box_object_collection import BoxObjectCollection

if TYPE_CHECKING:
    from boxsdk.session.session import Session


class LimitOffsetBasedObjectCollection(BoxObjectCollection):
    """
    An iterator of Box objects (BaseObjects) that were retrieved from a Box API endpoint that supports
    limit-offset type of pagination.

    See https://developer.box.com/en/guides/api-calls/pagination/ for more details.
    """

    def __init__(
            self,
            session: 'Session',
            url: str,
            limit: Optional[int] = None,
            fields: Iterator[str] = None,
            additional_params: Optional[dict] = None,
            return_full_pages: bool = False,
            offset: int = 0,
    ):
        """
        :param session:
            The Box session used to make requests.
        :param url:
            The endpoint url to hit.
        :param limit:
            The number of entries for each page to return. The default, as well as the upper limit of this value,
            differs by endpoint. See https://developer.box.com/en/reference. If limit is set to None, then the default
            limit (returned by Box in the response) is used.
        :param fields:
            List of fields to request. If None, will return the default fields for the object.
        :param additional_params:
            Additional HTTP params to send in the request.
        :param return_full_pages:
            If True, then the returned iterator for this collection will return full pages of Box objects on each
            call to next(). If False, the iterator will return a single Box object on each next() call.
        :param offset:
            The offset index to start paging from.
        """
        super().__init__(
            session,
            url,
            limit=limit,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=return_full_pages,
        )
        self._offset = offset

    def _update_pointer_to_next_page(self, response_object: dict) -> None:
        """Baseclass override."""
        total_count = response_object['total_count']

        if 'limit' in response_object:
            self._limit, old_limit = int(response_object['limit']), self._limit

            # The API might use a lower limit than the client asked for, if the
            # client asked for a limit above the maximum limit for that endpoint.
            # The API is supposed to respond with the limit that it actually used.
            # If that is given, then use that limit for the offset calculation, and
            # also for the remainder of the paging.

            # Do not apply this same logic to "offset". Offset is not documented to be
            # changed in the response, so respecting that value can lead to undefined
            # behavior.

            # If the API erroneously sends a bad value for limit, we want to
            # avoid getting into an infinite chain of API calls. So abort with
            # a runtime error.
            if self._limit <= 0 < old_limit:
                self._offset = total_count  # Disable additional paging.
                raise RuntimeError(f'API returned limit={self._limit}, cannot continue paging')

        # de-none-ify the _offset value so that the arthimatic below works
        self._offset = self._offset or 0

        if total_count >= self._offset + self._limit:
            self._offset += self._limit
        else:
            self._offset = total_count

    def _has_more_pages(self, response_object: dict) -> bool:
        """Baseclass override."""
        return self._offset < response_object['total_count']

    def _next_page_pointer_params(self) -> dict:
        """Baseclass override."""
        return {'offset': self._offset}

    def next_pointer(self) -> int:
        """Baseclass override."""
        return self._offset

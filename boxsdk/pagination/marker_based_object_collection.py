# coding: utf-8
from typing import Optional, Iterator, TYPE_CHECKING

from .box_object_collection import BoxObjectCollection

if TYPE_CHECKING:
    from boxsdk.session.session import Session


class MarkerBasedObjectCollection(BoxObjectCollection):
    """
    An iterator of Box objects (BaseObjects) that were retrieved from a Box API endpoint that supports
    marker type of pagination.

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
            marker: Optional[str] = None,
            supports_limit_offset_paging: bool = False,
            use_post: bool = False
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
        :param marker:
            The offset index to start paging from.
        :param supports_limit_offset_paging:
            Does this particular endpoint also support limit-offset paging? This information is needed, as
            the endpoints that support both require an special extra request parameter.
        :param use_post:
            If True, then the returned iterator will make POST requests with all the data in the body on each
            call to next().
            If False, the iterator will make GET requets with all the data as query params on each call to next().
        """
        super().__init__(
            session,
            url,
            limit=limit,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=return_full_pages,
            use_post=use_post
        )
        self._marker = marker
        self._supports_limit_offset_paging = supports_limit_offset_paging

    def _update_pointer_to_next_page(self, response_object: dict) -> None:
        """Baseclass override."""
        self._marker = self._get_next_marker_from_response_object(response_object)

    def _has_more_pages(self, response_object) -> bool:
        """Baseclass override."""
        return bool(self._get_next_marker_from_response_object(response_object))

    @staticmethod
    def _get_next_marker_from_response_object(response_object) -> Optional[str]:
        """Get the marker that should be used to retrieve the next page.

        When we've just retrieved the last page, the API is inconsistent about
        what it returns. Some endpoints return "next_marker":"", some return
        "next_marker":null, some don't give any "next_marker" value. In all of
        these cases, this method will return `None`.

        Otherwise, this method returns the string value of the "next_marker"
        field.
        """
        return response_object.get('next_marker') or None

    def _next_page_pointer_params(self) -> dict:
        """Baseclass override."""
        pointer_params = {}
        # For transitioning endpoints that support both marker and limit-offset paging, we must specify an
        # additional 'useMarker' parameter to the Box API.
        if self._supports_limit_offset_paging:
            pointer_params['useMarker'] = True
        if self._marker is not None:
            pointer_params['marker'] = self._marker
        return pointer_params

    def next_pointer(self) -> Optional[str]:
        """Baseclass override."""
        return self._marker

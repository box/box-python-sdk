# coding: utf-8
from typing import Optional, Any

from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET
from .base_item import BaseItem


class WebLink(BaseItem):
    """Box API endpoint for interacting with WebLinks."""

    _item_type = 'web_link'

    @api_call
    def create_shared_link(
            self,
            *,
            access: Optional[str] = None,
            unshared_at: Optional[str] = SDK_VALUE_NOT_SET,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> 'WebLink':
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.  Takes an RFC3339-formatted string, e.g.
            '2018-10-31T23:59:59-07:00' for 11:59:59 PM on October 31, 2018 in the America/Los_Angeles timezone.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :return:
            The updated object with s shared link.
            Returns a new object of the same type, without modifying the original object passed as self.
        """
        # pylint:disable=arguments-differ
        return super().create_shared_link(
            access=access,
            unshared_at=unshared_at,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def get_shared_link(
            self,
            *,
            access: Optional[str] = None,
            unshared_at: Optional[str] = SDK_VALUE_NOT_SET,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> str:
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :returns:
            The URL of the shared link.
        """
        # pylint:disable=arguments-differ
        return super().get_shared_link(
            access=access,
            unshared_at=unshared_at,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def remove_shared_link(self, **kwargs: Any) -> bool:
        """
        Baseclass override.

        :param kwargs:
            Used to fulfill the contract of overriden method
        :returns:
            Whether or not the update was successful.
        """
        return super().remove_shared_link()

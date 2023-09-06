from typing import Any

from .base_object import BaseObject


class SignTemplate(BaseObject):
    """
    Represents a Sign Template used by Box Sign
    """
    _item_type = 'sign-template'

    def get_url(self, *args: Any) -> str:
        """
        Returns the url for this sign template.
        """
        return self._session.get_url('sign_templates', self._object_id, *args)

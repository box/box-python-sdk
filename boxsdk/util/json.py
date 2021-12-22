# coding: utf-8
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boxsdk import NetworkResponse


def is_json_response(network_response: 'NetworkResponse') -> bool:
    """Return whether or not the network response content is json.

    :param network_response:
        The response from the Box API.
    """
    try:
        network_response.json()
        return True
    except ValueError:
        return False

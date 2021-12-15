# coding: utf-8

def is_json_response(network_response):
    """Return whether or not the network response content is json.

    :param network_response:
        The response from the Box API.
    :type network_response:
        :class:`NetworkResponse`
    """
    try:
        network_response.json()
        return True
    except ValueError:
        return False

# coding: utf-8

def get_shared_link_header(shared_link: str, password: str = None) -> dict:
    """
    Gets the HTTP header required to use a shared link to grant access to a shared item.

    :param shared_link:
        The shared link.
    :param password:
        The password for the shared link.
    :return:
        The item referred to by the shared link.
    """
    shared_link_password = f'&shared_link_password={password}' if password is not None else ''
    box_api_header = f'shared_link={shared_link}{shared_link_password}'
    return {'BoxApi': box_api_header}

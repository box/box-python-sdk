# coding: utf-8

from logging import getLogger
from multiprocessing import Manager, Process
from os import getpid

from boxsdk.auth.cooperatively_managed_oauth2 import CooperativelyManagedOAuth2
from boxsdk.util.log import setup_logging
from boxsdk import Client

from .auth import authenticate, CLIENT_ID, CLIENT_SECRET


def main():
    # Create a multiprocessing manager to use as the token store
    global tokens, refresh_lock
    manager = Manager()
    tokens = manager.Namespace()
    refresh_lock = manager.Lock()

    # Authenticate in main process
    oauth2, tokens.access, tokens.refresh = authenticate(CooperativelyManagedOAuth2)

    # Create 2 worker processes and wait on them to finish
    workers = []
    for _ in range(2):
        worker_process = Process(target=worker)
        worker_process.start()
        workers.append(worker_process)
    for worker_process in workers:
        worker_process.join()


def _retrive_tokens():
    return tokens.access, tokens.refresh


def _store_tokens(access_token, refresh_token):
    tokens.access, tokens.refresh = access_token, refresh_token


def worker():
    # Set up a logging network, but use the LoggingProxy so we can see which PID is generating messages
    logger = getLogger('boxsdk.network.{0}'.format(getpid()))
    setup_logging(name=logger.name)

    # Create a coop oauth2 instance.
    # Tokens will be retrieved from and stored to the multiprocessing Namespace.
    # A multiprocessing Lock will be used to synchronize token refresh.
    # The tokens from the main process are used for initial auth.
    # Whichever process needs to refresh
    oauth2 = CooperativelyManagedOAuth2(
        retrieve_tokens=_retrive_tokens,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        store_tokens=_store_tokens,
        access_token=tokens.access,
        refresh_token=tokens.refresh,
        refresh_lock=refresh_lock,
    )
    client = Client(oauth2)
    _do_work(client)


def _do_work(client):
    # Do some work in a worker process.
    # To see token refresh, perhaps put this in a loop (and don't forget to sleep for a bit between requests).
    me = client.user(user_id='me').get()
    items = client.folder('0').get_items(10)


if __name__ == '__main__':
    main()

# coding: utf-8

from __future__ import unicode_literals, absolute_import

from logging import Logger
from multiprocessing import Manager, Process
from os import getpid

from boxsdk.auth.cooperatively_managed_oauth2 import CooperativelyManagedOAuth2
from boxsdk.network.logging_network import LoggingNetwork
from boxsdk.util.log import setup_logging
from boxsdk import Client

from auth import authenticate, CLIENT_ID, CLIENT_SECRET


def main():
    # Create a multiprocessing manager to use as the token store
    global tokens, refresh_lock
    manager = Manager()
    tokens = manager.Namespace()
    refresh_lock = manager.Lock()

    # Authenticate in master process
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
    logger = setup_logging(name='boxsdk.network.{0}'.format(getpid()))
    logger_proxy = LoggerProxy(logger)
    logging_network = LoggingNetwork(logger)

    # Create a coop oauth2 instance.
    # Tokens will be retrieved from and stored to the multiprocessing Namespace.
    # A multiprocessing Lock will be used to synchronize token refresh.
    # The tokens from the master process are used for initial auth.
    # Whichever process needs to refresh
    oauth2 = CooperativelyManagedOAuth2(
        retrieve_tokens=_retrive_tokens,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        store_tokens=_store_tokens,
        network_layer=logging_network,
        access_token=tokens.access,
        refresh_token=tokens.refresh,
        refresh_lock=refresh_lock,
    )
    client = Client(oauth2, network_layer=logging_network)
    _do_work(client)


def _do_work(client):
    # Do some work in a worker process.
    # To see token refresh, perhaps put this in a loop (and don't forget to sleep for a bit between requests).
    me = client.user(user_id='me').get()
    items = client.folder('0').get_items(10)


class LoggerProxy(Logger):
    """
    Proxy for a logger that injects the current PID before log messages.
    """
    def __init__(self, logger):
        self._logger_log = logger._log
        logger._log = self._log
        self._preamble = 'PID {0}: '.format(getpid())

    def _log(self, level, msg, args, exc_info=None, extra=None):
        msg = self._preamble + msg
        return self._logger_log(level, msg, args, exc_info=exc_info, extra=extra)


if __name__ == '__main__':
    main()

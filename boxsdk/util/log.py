# coding: utf-8

from __future__ import unicode_literals

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
import sys

from six import string_types


_no_logger = object()


class Logging(object):
    _has_setup = False

    def setup_logging(self, stream_or_file=_no_logger, debug=False, name=None):
        if not self._has_setup:
            self._has_setup = True
            self._setup_logging(stream_or_file, debug, name)

    @staticmethod
    def _setup_logging(stream_or_file=_no_logger, debug=False, name=None):
        logger = logging.getLogger(name)
        if isinstance(stream_or_file, string_types):
            logger.addHandler(logging.FileHandler(stream_or_file, mode='a'))
        elif stream_or_file is not _no_logger:
            logger.addHandler(logging.StreamHandler(stream_or_file or sys.stdout))
        logger.setLevel(logging.DEBUG if debug else logging.INFO)


_logging = Logging()


def setup_logging(stream_or_file=_no_logger, debug=False, name=None):
    """
    Create a logger for communicating with the user or writing to log files.
    Sets the level to INFO or DEBUG, depending on the debug flag.

    If a stream or file is passed (or None is passed to stream_or_file), then
    a handler to that stream or file (stdout for None) is added to the logger.

    :param stream_or_file:
        The destination of the log messages. If None, stdout will be used.
    :type stream_or_file:
        `unicode` or `file` or None
    :param debug:
        Whether or not the logger will be at the DEBUG level (if False, the logger will be at the INFO level).
    :type debug:
        `bool` or None
    :param name:
        The logging channel. If None, a root logger will be created.
    :type name:
        `unicode` or None
    """
    _logging.setup_logging(stream_or_file, debug, name)


logging.getLogger(__name__).addHandler(NullHandler())


__all__ = list(map(str, ['setup_logging']))

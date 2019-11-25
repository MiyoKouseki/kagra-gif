#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG, INFO


class Logger:
    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        #formatter = Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
        formatter = Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

        # stdout
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # file
        handler = handlers.RotatingFileHandler(filename = './log/main.log',
                                               maxBytes = 1048576,
                                               backupCount = 3)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, *msg):
        self.logger.debug(*msg)

    def info(self, *msg):
        self.logger.info(*msg)

    def warn(self, *msg):
        self.logger.warning(*msg)

    def error(self, *msg):
        self.logger.error(*msg)

    def critical(self, *msg):
        self.logger.critical(*msg)

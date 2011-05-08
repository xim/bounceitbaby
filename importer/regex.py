# encoding: utf-8

import re

from base import LogReader, DataItem

import logging

logger = logging.getLogger('bounceitbaby')

class BaseRegExReader(LogReader):
    u"""
    Base class for simple regex line parsers.

    Uses line_fmt and re.match(…).groupdict() to yield DataItem objects
    """
    line_fmt = None

    def process(self):
        for line in self.get_data():
            match = re.match(self.line_fmt, line)
            if match is not None:
                kwargs = dict((field, None) for field in DataItem._fields)
                kwargs.update(match.groupdict())
                yield DataItem(**kwargs)
            else:
                logger.warning('Encountered a line that did not match the ' +
                        'log format "%s"' % type(self).__name__)
                logger.debug('Line: ' + line)

    def get_aptitude(self):
        """
        Regex aptitude is defined as amount of lines matching the line_fmt
        regex, up to 5.
        """
        hits = 0
        for line in self.get_data(5):
            if re.match(self.line_fmt, line):
                hits += 1
        return hits

    def get_actors(self):
        if not self._actors:
            for item in self.process():
                for actor in (item.sender, item.recipient):
                    if not actor in self._actors:
                        self._actors.append(actor)
        return self._actors

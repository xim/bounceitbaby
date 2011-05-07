from collections import namedtuple
from itertools import izip

import logging

logger = logging.getLogger('bounceitbaby')

DataItem = namedtuple('DataItem', ['sender', 'recipient', 'sent_time',
        'rcvd_time', 'msg_type', 'data', 'port_name'])

class LogReader(object):
    """
    Base class of all log readers.
    """

    def __init__(self, filename, filehandle=None):
        logger.debug('Init: %s for file %s' % (self, filename))

        self._filename = str(filename)
        self._cache = []
        self._done = False

        if filehandle is not None:
            filehandle.seek(0)
        self._filehandle = filehandle
        self._actors = []

    def __unicode__(self):
        return '<%s Logreader>' % self.__class__.__name__

    def get_data(self, num_of_lines=None):
        """
        Magic methos that ensures data is cached. Allows fetching the first n
        lines of a file as well.
        """

        if self._cache:
            logger.debug('%s reading data for %s from cache' % (self,
                    self._filename))
        if num_of_lines is None:
            for line in self._cache:
                yield line
        else:
            for line, _ in izip(self._cache, xrange(num_of_lines)):
                yield line
            if num_of_lines <= len(self._cache):
                raise StopIteration

        if self._done:
            logger.debug('No more lines, no need to open file')
            raise StopIteration
        logger.debug('%s reading %s' % (self, self._filename))
        if self._filehandle is None:
            self._filehandle = open(self._filename)
        line_number = len(self._cache)
        while num_of_lines != line_number:
            line_number += 1
            try:
                line = self._filehandle.next()
                self._cache.append(line)
                yield line
            except StopIteration:
                logger.debug('We hit EOF. Closing %s' % self._filename)
                self._filehandle.close()
                self._done = True
                break
        raise StopIteration

    def process(self):
        pass

    def get_aptitude(self):
        return 0

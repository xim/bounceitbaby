# encoding: utf-8

from collections import namedtuple
from itertools import izip
import logging
import re

LOG_TYPES = ['Guess', 'CDpp', 'Foo']

DataItem = namedtuple('DataItem', ['sender', 'recipient', 'sent_time',
        'rcvd_time', 'msg_type', 'data', 'port_name'])

class LogReader(object):
    """
    Base class of all log readers.
    """

    def __init__(self, filename):
        self._filename = filename
        self._cache = []
        self._filehandle = None
        self._done = False

    def get_data(self, num_of_lines=None):
        """
        Magic class that ensures data is cached. Allows fetching the first n
        lines of a file.
        """

        if num_of_lines is None:
            for line in self._cache:
                yield line
        else:
            for line, _ in izip(self._cache, xrange(num_of_lines)):
                yield line
            if num_of_lines <= len(self._cache):
                raise StopIteration

        if self._done:
            raise StopIteration
        logging.debug('%s reading %s' % (self, self._filename))
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
                self._filehandle.close()
                self._done = True
                break
        raise StopIteration

    def process(self):
        pass

    def get_aptitude(self):
        return 0

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
                kwargs = match.groupdict()
                for field in DataItem._fields:
                    if field not in kwargs:
                        kwargs[field] = None
                yield DataItem(**kwargs)

    def get_aptitude(self):
        hits = 0
        for line in self.get_data(5):
            if re.match(self.line_fmt, line):
                hits += 1
        return hits

class Foo(BaseRegExReader):
    """
    A test regex based parser.

    Expexts "from to time time type data", whitespace seperated.
    """
    line_fmt = r'^(?P<sender>\S+)\s+(?P<recipient>\S+)\s+(?P<sent_time>\S+)\s+(?P<rcvd_time>\S+)\s+(?P<msg_type>\S+)\s+(?P<data>\S+)\s*$'

class CDpp(BaseRegExReader):
    """
    Regex based parser for CD++ logs
    """
    line_fmt = r'^Me(nsaj|ssag)e (?P<msg_type>\S+)\s+/\s+(?P<sent_time>\S+)\s+/\s+(?P<sender>\S+?)(\(\S+\))?(\s+/\s+(?P<port_name>\S+))??(\s+/\s+(?P<data>\S+))?\s+(para|to)\s+(?P<recipient>\S+?)(\(\S+\))?\s*$'

    def get_data(self, *args, **kwargs):
        for line in super(CDpp, self).get_data(*args, **kwargs):
            yield re.sub(r'(\d{2}:\d{2}):(\d{3})', r'\1.\2', line)

class Guess(LogReader):
    """
    A log reader that reads a few lines and tests it against all available log
    parser classes using their line_fmt string.
    """
    def __init__(self, *args, **kwargs):
        super(Guess, self).__init__(*args, **kwargs)
        self.reader = None
        self.candidates = [Foo, CDpp]

    def __unicode__(self):
        return '<Guess Logreader: %s>' % self.reader

    def guess_reader(self):
        logging.debug('Guessing log reader')
        if not self.reader is None:
            return
        self.candidates = [reader(self._filename) \
                for reader in self.candidates]
        for line in self.get_data():
            pass
        for reader in self.candidates:
            reader._cache = self._cache
            reader._done = True
        aptitudes = [(reader, reader.get_aptitude()) \
                for reader in self.candidates]
        logging.debug('Aptitudes: %s' % repr(aptitudes))
        self.reader = sorted(aptitudes, lambda x,y: x[1] - y[1])[-1][0]
        self.candidates = []

    def process(self):
        self.guess_reader()

        return self.reader.process()

# encoding: utf-8

import logging
import re

LOG_TYPES = ['Guess', 'Foo']

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
            for line, _ in zip(self._cache, xrange(num_of_lines)):
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

    Uses line_fmt and re.match(…).groups()
    """
    line_fmt = None

    def process(self):
        for line in self.get_data():
            match = re.match(self.line_fmt, line)
            if match is not None:
                yield match.groups()

    def get_aptitude(self):
        hits = 0
        for line in self.get_data(5):
            if re.match(self.line_fmt, line):
                hits += 1
        return hits

class Foo(BaseRegExReader):
    """
    A test regex based parser.

    Expexts "from to time time sigtype", whitespace seperated.
    """
    line_fmt = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$'

class Guess(LogReader):
    """
    A log reader that reads a few lines and tests it against all available log
    parser classes using their line_fmt string.
    """
    def __init__(self, *args, **kwargs):
        super(Guess, self).__init__(*args, **kwargs)
        self.reader = None
        self.candidates = [Foo]

    def __unicode__(self):
        return '<Guess Logreader: %s>' % self.reader

    def guess_reader(self):
        logging.debug('Guessing log reader')
        if not self.reader is None:
            return
        self.candidates = [reader(self._filehandle) \
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

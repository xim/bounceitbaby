import logging

logger = logging.getLogger('bounceitbaby')

from base import LogReader
from cdpp import CDpp
from regex import BaseRegExReader

LOG_TYPES = ['Guess', 'CDpp', 'Foo']

class Foo(BaseRegExReader):
    """
    A test regex based parser.

    Expexts "from to time time type data", whitespace seperated.
    """
    line_fmt = r'^(?P<sender>\S+)\s+(?P<recipient>\S+)\s+(?P<sent_time>\S+)\s+(?P<rcvd_time>\S+)\s+(?P<msg_type>\S+)\s+(?P<data>\S+)\s*$'

class Guess(LogReader):
    """
    A log reader that reads a few lines and tests it against all available log
    parser classes using their line_fmt string.
    The available candidate classes are set in self.candidates.
    The get_aptitude function is called on each, and the hightest ranking class
    is used for parsing the file.
    """
    def __init__(self, *args, **kwargs):
        super(Guess, self).__init__(*args, **kwargs)
        self.reader = None
        self.candidates = [Foo, CDpp]

    def __unicode__(self):
        return '<Guess Logreader: %s>' % self.reader

    def guess_reader(self):
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
        logger.debug('%s: List of log readers and their aptitudes: %s' % \
                (self, repr(aptitudes)))
        self.reader = sorted(aptitudes, lambda x,y: x[1] - y[1])[-1][0]
        logger.info('Determined "%s" to be of %s format' % \
                (self._filename, type(self.reader).__name__))
        self.candidates = []

        self.process = self.reader.process
        self.get_actors = self.reader.get_actors

    def process(self):
        self.guess_reader()

        return self.reader.process()

    def get_actors(self):
        self.guess_reader()

        return self.reader.get_actors()

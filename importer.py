import re

LOG_TYPES = ['Guess', 'Foo']

class LogReader(object):
    """
    Base class of all log readers.

    LogReaders must define a regex to match the line layout.
    """
    line_fmt = None

class Foo(LogReader):
    line_fmt = r'^(\S+)\s+(\S+)\s+(\S+)$'

    def process_lines(self, lines):
        for line in lines:
            match = re.match(self.line_fmt, line)
            if match is not None:
                yield match.groups()

class Guess(LogReader):
    def __init__(self):
        self.reader = None
        self.readers = [Foo]

    def guess_reader(self, lines):
        hits = dict((reader, 0) for reader in self.readers)
        for reader in self.readers:
            line_count = 0
            for line in lines:
                if line_count == 5:
                    break
                line_count += 1
                if re.match(reader.line_fmt, line):
                    hits[reader] += 1
        if hasattr(lines, 'seek'):
            lines.seek(0)
        self.reader = sorted(hits, lambda x,y: hits[x] - hits[y])[-1]()

    def process_lines(self, lines):
        self.guess_reader(lines)

        return self.reader.process_lines(lines)

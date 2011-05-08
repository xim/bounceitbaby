# encoding: utf-8

import os
import re

from regex import BaseRegExReader

class CDpp(BaseRegExReader):
    """
    Regex based parser for CD++ logs.
    These log files are ugly, thus my regex is as well.
    """
    line_fmt = r'^Me(nsaj|ssag)e (?P<msg_type>\S+)\s+/\s+(?P<sent_time>\S+)\s+/\s+(?P<sender>\S+?)(\(\S+\))?(\s+/\s+(?P<port_name>\S+))??(\s+/\s+(?P<data>\S+))?\s+(para|to)\s+(?P<recipient>\S+?)(\(\S+\))?\s*$'

    def __init__(self, *args, **kwargs):
        super(CDpp, self).__init__(*args, **kwargs)
        self._ma_filename = self._filename[:self._filename.rfind('.')] + '.ma'

    def get_data(self, *args, **kwargs):
        u"""
        Overridden to fix timestamp data from format mm:ss:µµµ to mm:ss.µµµ
        """
        for line in super(CDpp, self).get_data(*args, **kwargs):
            yield re.sub(r'(\d{2}:\d{2}):(\d{3})', r'\1.\2', line)

    def get_aptitude(self):
        """
        Aptitude for a CDpp file is amount of lines matching the line_fmt in
        the top five lines of the file, plus one bonus point for having a .ma
        file with a corresponding name.
        """
        aptitude = super(CDpp, self).get_aptitude()
        if os.path.isfile(self._ma_filename):
            aptitude += 1
        return aptitude

    def get_actors(self):
        # TODO: Parse the CD++ .ma file!
        return super(CDpp, self).get_actors()

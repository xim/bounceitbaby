# encoding: utf-8

import re

from regex import BaseRegExReader

class CDpp(BaseRegExReader):
    """
    Regex based parser for CD++ logs.
    These log files are ugly, thus my regex is as well.
    """
    line_fmt = r'^Me(nsaj|ssag)e (?P<msg_type>\S+)\s+/\s+(?P<sent_time>\S+)\s+/\s+(?P<sender>\S+?)(\(\S+\))?(\s+/\s+(?P<port_name>\S+))??(\s+/\s+(?P<data>\S+))?\s+(para|to)\s+(?P<recipient>\S+?)(\(\S+\))?\s*$'

    def get_data(self, *args, **kwargs):
        u"""
        Overridden to fix timestamp data from format mm:ss:µµµ to mm:ss.µµµ
        """
        for line in super(CDpp, self).get_data(*args, **kwargs):
            yield re.sub(r'(\d{2}:\d{2}):(\d{3})', r'\1.\2', line)

    def get_actors(self):
        # TODO: Parse the CD++ .ma file!
        return super(CDpp, self).get_actors()

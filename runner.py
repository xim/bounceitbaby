#!/usr/bin/python
# encoding: utf-8

# Written by Morten Minde Neergaard – m@8d.no

u"""Usage: %prog [options] filename(s)

Makes pretty bounce diagrams from misc. input formats.
Examples:
  %prog logfile.log  – Analyzes logfile.log and visualizes
  %prog -d -         – Analyzes in debug mode from STDIN
  %prog -o PNG       – Force 'PNG' output module
  %prog -l Foo       – Force 'Foo' log parser module
"""

from optparse import OptionParser
import logging
import sys

import importer, grapher

def main():
    '''
    Method run when starting from command line.
    Does not get run if importing as a python module.
    '''

    parser = OptionParser(usage=__doc__)

    def filename_callback(option, opt_str, value, parser):
        print option, opt_str, value, parser
        setattr(parser.values, option.dest, value)
        parser.values.graph_output = 'File'

    parser.add_option('-d', '--debug',
            action='store_const', dest='loglevel', default=logging.INFO,
            const=logging.DEBUG, help='Set log level to debug')
    parser.add_option('-l', '--log-parser',
            choices=importer.LOG_TYPES,
            default=importer.LOG_TYPES[0],
            help='Force log parser (%s)' % ', '.join(importer.LOG_TYPES))
    parser.add_option('-o', '--graph-output',
            choices=grapher.GRAPH_TYPES,
            default=grapher.GRAPH_TYPES[0],
            help='Force output module (%s)' % ', '.join(grapher.GRAPH_TYPES))
    parser.add_option('-f', '--output-file', action='callback',
            callback=filename_callback, dest="output_file", type="string",
            default="out.png", help='Set output filename. This also ' \
                    + 'overrides the output module to "File"')
    parser.add_option('-n', '--linear',
            action='store_true', dest='linear', default=False,
            help='Use linear scale on time axis')

    options, args = parser.parse_args()

    if not args:
        raise Exception('Pass at least one file name (- for STDIN)')

    if options.loglevel == logging.DEBUG:
        log_fmt = '[%(levelname)8s] %(asctime)s: %(message)s'
    else:
        log_fmt = '%(message)s'

    logging.basicConfig(
            level=options.loglevel,
            format=log_fmt
            )

    for filename in args:
        if filename == '-':
            filename = '/dev/stdin'

        log_parser_instance = getattr(importer, options.log_parser)(filename)
        grapher_instance = getattr(grapher, options.graph_output)(linear=options.linear)

        data = log_parser_instance.process()
        grapher_instance.process_data(data)

if __name__ == '__main__':
    main()

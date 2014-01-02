#!/usr/bin/python

import argparse
from play_parser import OutputFormat
from play_parser import play_parser


def parse_args(args=None):
    #parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles', nargs='+', help='one or more CSV files ' +
        'downloaded from ' +
        'http://www.advancednflstats.com/2010/04/play-by-play-data.html')
    parser.add_argument('output', help='database connection string (example: ' +
        '\'mysql+mysqldb://user:password@hostname/mydatabase\') or output ' +
        'filename when used with --fileout option')
    parser.add_argument('-f', '--outputfiletype', help='output parsed plays ' +
        'to file of specified format instead of database (\'json\' or \'csv\')')
    parser.add_argument('-t', '--createtable', help='create the \'plays\' ' +
        'database table', action='store_true')
    if args is not None:
        return parser.parse_args(args)
    else:
        return parser.parse_args()


def run():
    args = parse_args()
    #parser(in_files, out_str, out_format, create_table)
    out_format = OutputFormat.DATABASE
    if args.outputfiletype == 'json':
        out_format = OutputFormat.JSON
    elif args.outputfiletype == 'csv':
        out_format = OutputFormat.CSV
    play_parser(args.infiles, args.output, out_format, args.createtable)


if __name__ == "__main__":
    run()

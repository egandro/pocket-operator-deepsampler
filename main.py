#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

#import argparse
from audacity import Audacity

if sys.version_info[0] < 4 and sys.version_info[1] < 8:
    sys.exit('PipeClient Error: Python 3.9 or later required')

# def _bool_from_string(strval):
#     """Return boolean value from string"""
#     if strval.lower() in ('true', 't', '1', 'yes', 'y'):
#         return True
#     if strval.lower() in ('false', 'f', '0', 'no', 'n'):
#         return False
#     raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--timeout', type=float, metavar='', default=10,
    #                     help="timeout for reply in seconds (default: 10")
    # parser.add_argument('-s', '--show-time', metavar='True/False',
    #                     nargs='?', type=_bool_from_string,
    #                     const='t', default='t', dest='show',
    #                     help='show command execution time (default: True)')
    # parser.add_argument('-d', '--docs', action='store_true',
    #                     help='show documentation and exit')
    # args = parser.parse_args()
    # foo = args.show

    # if args.docs:
    #     print(__doc__)
    #     sys.exit(0)

    main_dir = os.path.abspath(os.path.dirname(__file__))
    tmp_file = os.path.join(main_dir, 'output.wav')

    audacity = Audacity()
    audacity.play_record()
    audacity.truncate_silence()
    audacity.export(tmp_file)

if __name__ == '__main__':
    main()
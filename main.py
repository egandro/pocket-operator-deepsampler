#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Automate Audacity via mod-script-pipe.

Pipe Client may be used as a command-line script to send commands to
Audacity via the mod-script-pipe interface, or loaded as a module.
Requires Python 2.7 or later. Python 3 strongly recommended.

======================
Command Line Interface
======================

    usage: pipeaudacity.client.py [-h] [-t] [-s ] [-d]

Arguments
---------
    -h,--help: optional
        show short help and exit
    -t, --timeout: float, optional
        timeout for reply in seconds (default: 10)
    -s, --show-time: bool, optional
        show command execution time (default: True)
    -d, --docs: optional
        show this documentation and exit

Example
-------
    $ python3 pipeaudacity.client.py -t 20 -s False

    Launches command line interface with 20 second time-out for
    returned message, and don't show the execution time.

    When prompted, enter the command to send (not quoted), or 'Q' to quit.

    $ Enter command or 'Q' to quit: GetInfo: Type=Tracks Format=LISP

============
Module Usage
============

Note that on a critical error (such as broken pipe), the module just exits.
If a more graceful shutdown is required, replace the sys.exit()'s with
exceptions.

Example
-------

    # Import the module:
    >>> import pipeclient

    # Create a client instance:
    >>> client = pipeaudacity.client.PipeClient()

    # Send a command:
    >>> audacity.client.write("Command", timer=True)

    # Read the last reply:
    >>> print(audacity.client.read())

See Also
--------
Pipeaudacity.client.write : Write a command to _write_pipe.
Pipeaudacity.client.read : Read Audacity's reply from pipe.

Copyright Steve Daulton 2018
Released under terms of the GNU General Public License version 2:
<http://www.gnu.org/licenses/old-licenses/gpl-2.0.html />

"""

import sys
import time
import argparse
from audacity import Audacity

from pipeclient import PipeClient

if sys.version_info[0] < 4 and sys.version_info[1] < 8:
    sys.exit('PipeClient Error: Python 3.9 or later required')

def bool_from_string(strval):
    """Return boolean value from string"""
    if strval.lower() in ('true', 't', '1', 'yes', 'y'):
        return True
    if strval.lower() in ('false', 'f', '0', 'no', 'n'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    """Interactive command-line for PipeClient"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=float, metavar='', default=10,
                        help="timeout for reply in seconds (default: 10")
    parser.add_argument('-s', '--show-time', metavar='True/False',
                        nargs='?', type=bool_from_string,
                        const='t', default='t', dest='show',
                        help='show command execution time (default: True)')
    parser.add_argument('-d', '--docs', action='store_true',
                        help='show documentation and exit')
    args = parser.parse_args()

    if args.docs:
        print(__doc__)
        sys.exit(0)

    audacity = Audacity()
    # while True:
    #     reply = ''
    #     message = input("\nEnter command or 'Q' to quit: ")
    #     start = time.time()
    #     if message.upper() == 'Q':
    #         sys.exit(0)
    #     elif message == '':
    #         pass
    #     else:
    #         audacity.client.write(message, timer=args.show)
    #         while reply == '':
    #             time.sleep(0.1)  # allow time for reply
    #             if time.time() - start > args.timeout:
    #                 reply = 'PipeClient: Reply timed-out.'
    #             else:
    #                 reply = audacity.client.read()
    #         print(reply)

    audacity.play_record('C:/projects/pocket-operator-deepsampler/samples/silence-10sec.wav')
    audacity.export('C:/projects/pocket-operator-deepsampler/samples/output.wav')

if __name__ == '__main__':
    main()
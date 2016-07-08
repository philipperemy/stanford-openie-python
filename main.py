#!/usr/bin/env python

"""
A simple Python wrapper for the stanford IE binary that makes it easier to use it
on UNIX/Windows systems.
Note: The script does some minimal sanity checking of the input, but don't
    expect it to cover all cases. After all, it is a just a wrapper.
Example:
    > echo "Barack Obama was born in Hawaii." > text.txt
    > python python main.py -f text.txt
    Should display
    1.000: (Barack Obama; was; born)
    1.000: (Barack Obama; was born in; Hawaii)
Authors:    Philippe Remy       <github: philipperemy>
Version:    2016-07-08
"""

# Copyright (c) 2016, Philippe Remy <github: philipperemy>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import print_function

import os
from argparse import ArgumentParser
from platform import system
from subprocess import Popen
from sys import argv
from sys import stderr

IS_WINDOWS = True if system() == 'Windows' else False
JAVA_BIN_PATH = 'java.exe' if IS_WINDOWS else 'java'


def arg_parse():
    arg_p = ArgumentParser('Stanford IE Python Wrapper')
    arg_p.add_argument('-f', '--filename', type=str, default=None)
    arg_p.add_argument('-v', '--verbose', action='store_true')
    return arg_p


def debug_print(log, verbose):
    if verbose:
        print(log)


def stanford_ie(filename, verbose=True):
    command = '{} -mx1g -cp "stanford-openie.jar:stanford-openie-models.jar:lib/*" ' \
              'edu.stanford.nlp.naturalli.OpenIE {} -format ollie > out.txt'.format(JAVA_BIN_PATH, filename)
    if verbose:
        debug_print('Executing command = {}'.format(command), verbose)
        java_process = Popen(command, stdout=stderr, shell=True)
    else:
        java_process = Popen(command, stdout=stderr, stderr=open(os.devnull, 'w'), shell=True)
    java_process.wait()
    assert not java_process.returncode, 'ERROR: Call to stanford_ie exited with a non-zero code status.'

    with open('out.txt', 'r') as output_file:
        return output_file.readlines()


def main(args):
    arg_p = arg_parse().parse_args(args[1:])
    filename = arg_p.filename
    verbose = arg_p.verbose
    if filename is None:
        print('please provide a text file containing your input. Program will exit.')
        exit(1)
    if verbose:
        debug_print('filename = {}'.format(filename), verbose)
    entities_relations = stanford_ie(filename, verbose)
    print(entities_relations)


if __name__ == '__main__':
    exit(main(argv))

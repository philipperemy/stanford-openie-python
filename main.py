#!/usr/bin/env python

"""
A simple Python wrapper for the stanford IE binary that makes it easier to use it
on UNIX/Windows systems.
Note: The script does some minimal sanity checking of the input, but don't
    expect it to cover all cases. After all, it is a just a wrapper.
Example:
    > echo "Barack Obama was born in Hawaii." > text.txt
    > python main.py -f text.txt
    > python main.py -f text.txt,text2.txt (for batch mode).
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
from subprocess import Popen
from sys import argv
from sys import stderr

JAVA_BIN_PATH = 'java'
DOT_BIN_PATH = 'dot'
STANFORD_IE_FOLDER = 'stanford-openie'

tmp_folder = '/tmp/openie/'
if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)


def arg_parse():
    arg_p = ArgumentParser('Stanford IE Python Wrapper')
    arg_p.add_argument('-f', '--filename', type=str, default=None)
    arg_p.add_argument('-v', '--verbose', action='store_true')
    arg_p.add_argument('-g', '--generate_graph', action='store_true')
    return arg_p


def debug_print(log, verbose):
    if verbose:
        print(log)


def process_entity_relations(entity_relations_str, verbose=True):
    # format is ollie.
    entity_relations = list()
    for s in entity_relations_str:
        entity_relations.append(s[s.find("(") + 1:s.find(")")].split(';'))
    return entity_relations


def generate_graphviz_graph(entity_relations, verbose=True):
    """digraph G {
    # a -> b [ label="a to b" ];
    # b -> c [ label="another label"];
    }"""
    graph = list()
    graph.append('digraph {')
    for er in entity_relations:
        graph.append('"{}" -> "{}" [ label="{}" ];'.format(er[0], er[2], er[1]))
    graph.append('}')

    out_dot = tmp_folder + 'out.dot'
    with open(out_dot, 'w') as output_file:
        output_file.writelines(graph)

    out_png = tmp_folder + 'out.png'
    command = '{} -Tpng {} -o {}'.format(DOT_BIN_PATH, out_dot, out_png)
    debug_print('Executing command = {}'.format(command), verbose)
    dot_process = Popen(command, stdout=stderr, shell=True)
    dot_process.wait()
    assert not dot_process.returncode, 'ERROR: Call to dot exited with a non-zero code status.'
    print('Wrote graph to {} and {}'.format(out_dot, out_png))


def stanford_ie(input_filename, verbose=True, generate_graphviz=False):
    out = tmp_folder + 'out.txt'
    input_filename = input_filename.replace(',', ' ')

    new_filename = ''
    for filename in input_filename.split():
        if filename.startswith('/'):  # absolute path.
            new_filename += '{} '.format(filename)
        else:
            new_filename += '../{} '.format(filename)

    absolute_path_to_script = os.path.dirname(os.path.realpath(__file__)) + '/'
    command = 'cd {};'.format(absolute_path_to_script)
    command += 'cd {}; {} -mx4g -cp "stanford-openie.jar:stanford-openie-models.jar:lib/*" ' \
               'edu.stanford.nlp.naturalli.OpenIE {} -format ollie > {}'. \
        format(STANFORD_IE_FOLDER, JAVA_BIN_PATH, new_filename, out)

    if verbose:
        debug_print('Executing command = {}'.format(command), verbose)
        java_process = Popen(command, stdout=stderr, shell=True)
    else:
        java_process = Popen(command, stdout=stderr, stderr=open(os.devnull, 'w'), shell=True)
    java_process.wait()
    assert not java_process.returncode, 'ERROR: Call to stanford_ie exited with a non-zero code status.'

    with open(out, 'r') as output_file:
        results_str = output_file.readlines()
    os.remove(out)

    results = process_entity_relations(results_str, verbose)
    if generate_graphviz:
        generate_graphviz_graph(results, verbose)

    return results


def main(args):
    arg_p = arg_parse().parse_args(args[1:])
    filename = arg_p.filename
    verbose = arg_p.verbose
    generate_graphviz = arg_p.generate_graph
    # print(arg_p)
    if filename is None:
        print('please provide a text file containing your input. Program will exit.')
        exit(1)
    if verbose:
        debug_print('filename = {}'.format(filename), verbose)
    entities_relations = stanford_ie(filename, verbose, generate_graphviz)

    print('\n'.join([' |'.join(a) for a in entities_relations]))


if __name__ == '__main__':
    exit(main(argv))

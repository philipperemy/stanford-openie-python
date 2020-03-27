import os
import tempfile
from pathlib import Path
from subprocess import Popen
from sys import stderr
from zipfile import ZipFile

import wget


class StanfordOpenIE:

    def __init__(self, core_nlp_version: str = '2018-10-05'):
        self.remote_url = 'https://nlp.stanford.edu/software/stanford-corenlp-full-{}.zip'.format(core_nlp_version)
        self.install_dir = Path('~/.stanfordnlp_resources/').expanduser()
        self.install_dir.mkdir(exist_ok=True)
        if not (self.install_dir / Path('stanford-corenlp-full-{}'.format(core_nlp_version))).exists():
            print('Downloading from %s.' % self.remote_url)
            output_filename = wget.download(self.remote_url, out=str(self.install_dir))
            print('\nExtracting to %s.' % self.install_dir)
            zf = ZipFile(output_filename)
            zf.extractall(path=self.install_dir)
            zf.close()

        os.environ['CORENLP_HOME'] = str(self.install_dir / 'stanford-corenlp-full-2018-10-05')
        from stanfordnlp.server import CoreNLPClient
        self.client = CoreNLPClient(annotators=['openie'], memory='8G')

    def annotate(self, text: str, properties_key: str = None, properties: dict = None, simple_format: bool = True):
        """
        :param (str | unicode) text: raw text for the CoreNLPServer to parse
        :param (str) properties_key: key into properties cache for the client
        :param (dict) properties: additional request properties (written on top of defaults)
        :param (bool) simple_format: whether to return the full format of CoreNLP or a simple dict.
        :return: Depending on simple_format: full or simpler format of triples <subject, relation, object>.
        """
        # https://stanfordnlp.github.io/CoreNLP/openie.html
        core_nlp_output = self.client.annotate(text=text, annotators=['openie'], output_format='json',
                                               properties_key=properties_key, properties=properties)
        if simple_format:
            triples = []
            for sentence in core_nlp_output['sentences']:
                for triple in sentence['openie']:
                    triples.append({
                        'subject': triple['subject'],
                        'relation': triple['relation'],
                        'object': triple['object']
                    })
            return triples
        else:
            return core_nlp_output

    def generate_graphviz_graph(self, text: str, png_filename: str = './out/graph.png'):
        """
       :param (str | unicode) text: raw text for the CoreNLPServer to parse
       :param (list | string) png_filename: list of annotators to use
       """
        entity_relations = self.annotate(text, simple_format=True)
        """digraph G {
        # a -> b [ label="a to b" ];
        # b -> c [ label="another label"];
        }"""
        graph = list()
        graph.append('digraph {')
        for er in entity_relations:
            graph.append('"{}" -> "{}" [ label="{}" ];'.format(er['subject'], er['object'], er['relation']))
        graph.append('}')

        output_dir = os.path.join('.', os.path.dirname(png_filename))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        out_dot = os.path.join(tempfile.gettempdir(), 'graph.dot')
        with open(out_dot, 'w') as output_file:
            output_file.writelines(graph)

        command = 'dot -Tpng {} -o {}'.format(out_dot, png_filename)
        dot_process = Popen(command, stdout=stderr, shell=True)
        dot_process.wait()
        assert not dot_process.returncode, 'ERROR: Call to dot exited with a non-zero code status.'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self.client.stop()
        del os.environ['CORENLP_HOME']

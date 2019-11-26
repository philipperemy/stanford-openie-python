import os
from pathlib import Path
from subprocess import Popen
from sys import stderr
from zipfile import ZipFile

import wget


class StanfordOpenIE:

    def __init__(self, core_nlp_version='2018-10-05'):
        self.remote_url = 'http://nlp.stanford.edu/software/stanford-corenlp-full-{}.zip'.format(core_nlp_version)
        self.install_dir = Path('~/stanfordnlp_resources/').expanduser()
        self.install_dir.mkdir(exist_ok=True)
        if not (self.install_dir / Path('stanford-corenlp-full-{}'.format(core_nlp_version))).exists():
            print('Downloading to %s.' % self.install_dir)
            output_filename = wget.download(self.remote_url, out=str(self.install_dir))
            print('\nExtracting to %s.' % self.install_dir)
            zf = ZipFile(output_filename)
            zf.extractall(path=self.install_dir)
            zf.close()

        os.environ['CORENLP_HOME'] = str(self.install_dir / 'stanford-corenlp-full-2018-10-05')
        from stanfordnlp.server import CoreNLPClient
        self.client = CoreNLPClient(annotators=['openie'], memory='8G')

    def annotate(self, text):
        o = self.client.annotate(text=text, annotators=['openie'], output_format='json')
        for triple in o['sentences'][0]['openie']:
            print(triple['subject'], '|', triple['relation'], '|', triple['object'])

    def generate_graphviz_graph(self, text, out='.'):
        entity_relations = self.client.annotate(text=text, annotators=['openie'], output_format='ollie')
        """digraph G {
        # a -> b [ label="a to b" ];
        # b -> c [ label="another label"];
        }"""
        graph = list()
        graph.append('digraph {')
        for er in entity_relations:
            graph.append('"{}" -> "{}" [ label="{}" ];'.format(er[0], er[2], er[1]))
        graph.append('}')

        out_dot = out + 'out.dot'
        with open(out_dot, 'w') as output_file:
            output_file.writelines(graph)

        out_png = out + 'out.png'
        command = 'dot -Tpng {} -o {}'.format(out_dot, out_png)
        dot_process = Popen(command, stdout=stderr, shell=True)
        dot_process.wait()
        assert not dot_process.returncode, 'ERROR: Call to dot exited with a non-zero code status.'
        print('Wrote graph to {} and {}'.format(out_dot, out_png))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        self.client.stop()
        del os.environ['CORENLP_HOME']

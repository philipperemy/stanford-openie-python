from setuptools import setup

setup(
    name='stanford-openie',
    version='1.3.0',
    description='Minimalist wrapper around Stanford OpenIE',
    author='Philippe Remy',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=['openie'],
    install_requires=[
        'wget',
        'stanfordnlp',
        'six'
    ]
)

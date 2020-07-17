# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="B3Parser",
    version="0.0.1",
    packages=find_packages(),
    # scripts=["say_hello.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        'pymongo',
        'psycopg2'
    ],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     "": ["*.txt", "*.rst"],
    #     # And include any *.msg files found in the "hello" package, too:
    #     "hello": ["*.msg"],
    # },

    # metadata to display on PyPI
    author="Diogo L. Rebouças",
    author_email="diogolr@gmail.com",
    description="Um parser para os arquivos de histórico de cotações da B3.",
    keywords="COTAHIST Cotações Históricas B3",
    url="https://github.com/diogolr/b3parser",   # project home page, if any
    # project_urls={
        # "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        # "Documentation": "https://docs.example.com/HelloWorld/",
        # "Source Code": "https://github.com/diogolr/b3parser",
    # },
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License '
        'v3 or later (LGPLv3+)'
    ],
    license = 'LGPL v3'

    # could also include long_description, download_url, etc.
)
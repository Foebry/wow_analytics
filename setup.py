import os

from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = ['wow']

requires = [
    'Databases @ git+https://github.com/Foebry/Databases.git#egg=Databases',
    'Logger @ git+https://github.com/Foebry/Logger.git#egg=Logger',
    'requires',
    'mysql-connector'
]

about = {}
with open(os.path.join(here, 'wow', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'wow': 'wow'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    project_urls={
        'Source': 'https://github.com/Foebry/Wow_Analytics',
    },
)

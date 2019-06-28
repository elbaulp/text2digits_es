import os
import sys

from setuptools import setup

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'w2n', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='w2n',
    version=version['__version__'],
    description=('Convert spanish number text to its numerical representation.'),
    author='Alejandro Alcalde',
    author_email='algui91@gmail.com',
    url='https://github.com/elbaulp/text2digits_es',
    license='GPL-v3',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
)

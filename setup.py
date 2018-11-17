from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyerrors',
    version='1.0.0',
    description='Simply error propagation package',
    long_description=long_description,
    url='https://github.com/aminnj/pyerrors',
    author='Nick Amin',
    author_email='amin.nj@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    py_modules=["pyerrors"],
    test_suite="tests",
    install_requires=[],
)

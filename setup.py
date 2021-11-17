from setuptools import setup
import os
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

# The following two methods were copied from
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            print (line)
            delim = '"' if '"' in line else "'"
            print ('delim = ', delim)
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='SBMLDiagrams',
    packages=['SBMLDiagrams'],
    version=version['SBMLDiagrams/_version.py'],
    description='Visualize, edit and write SBML files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jin Xu',
    author_email='jxu2019@uw.edu',
    url='https://github.com/SunnyXu/SBMLDiagrams',
    license='MIT License',
    install_requires=[
        'coverage',
        'numpy',
        'pandas',
	'python-libsbml',
	'pip>20',
	'simplesbml',
	'tellurium',
	'skia-python',
    ],
    #scripts=[''],# The name of your scipt, and also the command you'll be using for calling it
    include_package_data=True,
    classifiers=[
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python :: 3.6',
       'Programming Language :: Python :: 3.7',
       'Programming Language :: Python :: 3.8',
       'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

import os.path

from setuptools import setup, find_packages

# Get the long description from the relevant file
__here__ = os.path.dirname(os.path.realpath(__file__))
readme_filename = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(readme_filename, 'r') as f:
  readme = f.read()
try:
    import pypandoc
    readme = pypandoc.convert(readme, to='rst', format='md')
except:
    print("Conversion of long_description from markdown to reStructuredText failed, skipping...")
    pass

setup(
    name='pynYNAB',
    version='0.2',
    # Note: change 'master' to the tag name when release a new verion
    download_url='https://github.com/rienafairefr/nYNABapi/tarball/master',

    description=('Library for working with the nYNAB private API'
                 'Budget/Transactions Read/Write/Migration tools'),

    long_description=readme,

    url='https://github.com/rienafairefr/nYNABapi',

    author='rienafairefr',
    author_email='rienafairefr@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords=['nynab', 'ynab'],

    packages=find_packages(),

    install_requires=[
        'configargparse',
        'ofxtools',
        'pynab',
        'requests',
        'jsontableschema',
        'unicodecsv',
        'appdirs'
    ],

    package_data={
        'pynYNAB': ['tests/*'],
    },
)

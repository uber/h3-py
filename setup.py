import os
from setuptools import find_packages
from skbuild import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'src', 'h3', '_version.py')) as f:
    exec(f.read(), about)


def long_desc():
    here = os.path.abspath(os.path.dirname(__file__))
    fname = os.path.join(here, 'readme.md')
    with open(fname) as f:
        long_description = f.read()

    return long_description


numpy_requires = ['numpy']
test_requires = [
    'pytest',
    'pytest-cov',
    'flake8',
    'pylint',
    'pytest-mypy-plugins==1.9.3;python_version>="3.6"',
]
install_requires = ['typing_extensions;python_version<"3.8"']

setup(
    name = 'h3',
    version = about['__version__'],
    description = about['__description__'],
    long_description = long_desc(),
    long_description_content_type = 'text/markdown',
    license = about['__license__'],
    author = about['__author__'],
    author_email = about['__author_email__'],
    url = about['__url__'],
    classifiers = about['__classifiers__'],
    include_package_data=True,
    packages = find_packages(
        'src',
        exclude = ["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_data={
        'h3': [
            'py.typed',
        ]
    },
    zip_safe=False,
    package_dir = {'': 'src'},
    cmake_languages = ('C'),
    install_requires=install_requires,
    extras_require={
        'numpy': numpy_requires,
        'test': test_requires,
        'all': numpy_requires + test_requires,
    },
)

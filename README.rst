H3-Python
=========

|Build Status| |Build Status Appveyor| |H3 Version| |License|

This library provides Python bindings for the `H3 Core
Library <https://github.com/uber/h3>`__. For API reference, please see
the `H3 Documentation <https://uber.github.io/h3/>`__.

Installing
==========

You need to have ``cc``, ``make``, ``cmake`` (version 3.1 or above),
and ``git`` in your ``$PATH`` when installing this package:

.. code:: sh

    which cc
    /usr/bin/cc
    which make
    /usr/bin/make
    which cmake
    /usr/bin/cmake
    which git
    /usr/bin/git

.. code:: sh

    pip install h3

Installing on Windows
---------------------

On Windows you will also need to have ``bash`` (for example from Git)
installed.

Development
===========

.. code:: sh

    git clone https://github.com/uber/h3-py.git && cd h3-py
    virtualenv env 
    source env/bin/activate
    pip install -r requirements-dev.txt
    fab bootstrap



Gallery
===============

We love contributions. To contribute notebooks or cool visualizations,
please go to `Notebooks <https://github.com/uber/h3-py-notebooks>`__.
You can see using Jupyter's nbviewer:

https://nbviewer.jupyter.org/github/uber/h3-py-notebooks/tree/master/



Here is also a simple `walkthrough <https://nbviewer.jupyter.org/github/uber/h3-py-notebooks/blob/master/Usage.ipynb>`__ of the API. For more information, please see the `H3
Documentation <https://uber.github.io/h3/>`__.





    


.. |Build Status| image:: https://travis-ci.org/uber/h3-py.svg?branch=master
   :target: https://travis-ci.org/uber/h3-py
.. |Build Status Appveyor| image:: https://ci.appveyor.com/api/projects/status/eaa11gfwmr0gtr5y/branch/master?svg=true
   :target: https://ci.appveyor.com/project/Uber/h3-py/branch/master
.. |H3 Version| image:: https://img.shields.io/badge/h3-v3.4.2-blue.svg
   :target: https://github.com/uber/h3/releases/tag/v3.4.2
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: LICENSE

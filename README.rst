====
SDpy
====

SDpy is a TUI application for querying StarDict dictionaries.


Requirements
------------

SDpy uses the Python3, and following libraries:

* URWID
* pystardict
* rapidfuzz

This project also uses a `scroll widget`_ from `stig`_ project (included in the
sources).


Installation
------------

Currently it is possible to install SDpy with virtualenv

Installation
------------

SDpy can be installed using virtualenv:
didn't place it on `pypi`_ yet.

Preferred way for installation is to use virtualenv (or any other virtualenv
managers), i.e:

.. code:: shell-session

   $ python -m venv venv
   $ . venv/bin/activate
   (venv) $ git clone https://github.com/gryf/sdpy
   (venv) $ cd sdpy
   (venv) $ pip install -r requirements.txt .

Or via pip:

.. code:: shell-session

   $ git clone https://github.com/gryf/sdpy
   $ cd sdpy
   $ pip install --user -r requirements.txt .

Executable ``sdpy`` should be now available in the ``$PATH``.


Configuration
-------------

Config file ``sdpy.conf`` will be looked in ``$XDG_CONFIG_HOME``, which usually
means ``~/.config``. Config is very simple:

.. code:: ini

   [DEFAULT]
   basedir = /usr/share/stardict/dic

   [dict.1]
   filebase = dictd_www.freedict.de_eng-spa
   name = Freedict English-Spanish

   [dict.2]
   filebase = quick_english-japanese
   name = Quick English-Japanese

Where

* ``basedir`` - optional path to the dictionary files, saves typing whole path
* ``filebase`` - mandatory filename of the database (without extensions like
  ``.idx``, ``.dict``, ``.dict.dz``, ``.ifo``)
* ``name`` - optional name of the dictionary. If omitted, section name will be
  used.

Sections can be named whatever you want, it doesn't matter, and will be used
only if name is missing.


License
-------

This work is licensed on GPL3 license. See LICENSE file for details.

.. _pypi: https://pypi.org
.. _scroll widget: https://github.com/rndusr/stig/blob/8e2b5679eae3e78017400ae35fea8b3eb5652ee4/stig/tui/scroll.py
.. _stig: https://github.com/rndusr/stig

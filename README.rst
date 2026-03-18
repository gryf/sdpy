====
SDpy
====

SDpy is a TUI application for querying StarDict dictionaries.

.. image:: /images/iface.png?raw=true
      :alt: sdpy interface


Requirements
------------

SDpy uses the Python3, and following libraries:

* `URWID`_
* `pystardict`_
* `rapidfuzz`_

This project also uses a `scroll widget`_ from `stig`_ project (included in the
sources).


Installation
------------

Preferred way for installation is to use virtualenv (or any other virtualenv
managers), i.e:

.. code:: shell-session

   $ python -m venv venv
   $ . venv/bin/activate
   (venv) $ git clone https://github.com/gryf/sdpy
   (venv) $ cd sdpy
   (venv) $ pip install .

Or via pip:

.. code:: shell-session

   $ git clone https://github.com/gryf/sdpy
   $ cd sdpy
   $ pip install --user .

Executable ``sdpy`` should be now available in the ``$PATH``.


Configuration
-------------

Config file ``sdpy.conf`` will be looked in ``$XDG_CONFIG_HOME``, which usually
means ``~/.config``. Config is very simple:

.. code:: ini

   [DEFAULT]
   basedir = /usr/share/stardict/dic
   use-section-name = false
   fuzzy-ratio = 85
   len-phrase = 4
   max-definitions = -1

   [dict.1]
   filebase = dictd_www.freedict.de_eng-spa
   name = Freedict English-Spanish

   [dict.2]
   filebase = quick_english-japanese
   name = Quick English-Japanese
   find-recursively-dir = 

Where

* ``basedir`` - optional path to the dictionary files, saves typing whole path
* ``use-section-name`` - false by default, forces sections name to be used
  instead of name field
* ``fuzzy-ratio`` - indicates phrase similarity. The higher the number, the
  more precise entry must be. Highest possible value is 100. Default is 85.
  Note, don't provide too low values, as the search will become unusable, and
  the listed results may be totally random.
* ``len-phrase`` - by default definition are searched by first couple of
  letters, by default 4. This behaviour may become default if set pretty high
  number here - fuzzy find will never be used in that case.
* ``max-definitions`` - display only specified number of definitions on the
  list view. By default all of them will be displayed using negative number.
  Adding any positive number will display that much of found definitions at
  most, and setting 0 will display no definitions in case search phrase is
  empty.
* ``find-recursively-dir`` - instead of manually adding dicts one by one, scan
  provided directory for dictionary files
* ``filebase`` - mandatory filename of the database (without extensions like
  ``.idx``, ``.dict``, ``.dict.dz``, ``.ifo``)
* ``name`` - optional name of the dictionary. If omitted, name will be obtained
  form dictionary ``.ifo`` file ``bookname`` field

Sections can be named whatever you want, it doesn't matter, and will be used
instead of provided (or not) name only if ``use-section-name`` is set to true.

You can use ``filebase`` as relative path to the global ``basedir`` or local
``basedir`` placed in each section or even provide basedir for selected
sections.

Note, that section order determine order of displayed definitions on the
definitions view. Automatically scanned directory doesn't guarantee the order.
Also note, that adding many dictionaries will increase startup time and will
have impact on searching for the terms.


License
-------

This work is licensed on GPL3 license. See LICENSE file for details.

.. _pypi: https://pypi.org
.. _scroll widget: https://github.com/rndusr/stig/blob/8e2b5679eae3e78017400ae35fea8b3eb5652ee4/stig/tui/scroll.py
.. _stig: https://github.com/rndusr/stig
.. _URWID: http://urwid.org
.. _pystardict: https://github.com/lig/pystardict
.. _rapidfuzz: https://rapidfuzz.github.io/RapidFuzz

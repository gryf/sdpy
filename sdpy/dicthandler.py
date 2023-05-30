import configparser
import os

import pystardict
import rapidfuzz


XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))


class Dict:
    def __init__(self, dictfile, name=None):
        self._name = name
        self.dictfile = dictfile
        self.dictionary = None

    def load_dict(self):
        self.dictionary = pystardict.Dictionary(self.dictfile, in_memory=True)

    def keys(self):
        return self.dictionary.keys()

    def value(self, key):
        if key not in self.dictionary:
            return None
        return self.dictionary[key]

    @property
    def name(self):
        # precedence have provided by user custom name, than if
        # use-section-name is set to true, section name will be used, and as a
        # fallback bookname from the dictionary file.
        if self._name:
            return self._name
        if self.dictionary:
            try:
                return self.dictionary.ifo.bookname
            except Exception:
                warnings.warn(f'Seems like {self.dictfile} have no bookname '
                              f'in ifo')


class DictHandler:
    def __init__(self):
        self.conf = None
        self.dicts = []
        self._keys = []

        self._load_config()

    def _load_config(self):
        conf = os.path.join(XDG_CONF_DIR, 'sdpy.conf')
        if not os.path.exists(conf):
            return

        cp = configparser.ConfigParser()
        cp.read(conf)
        try:
            basedir = cp.get('DEFAULT', 'basedir')
        except configparser.NoOptionError:
            basedir = ''
        try:
            use_section_name = cp.getboolean('DEFAULT', 'use-section-name')
        except configparser.NoOptionError:
            use_section_name = False

        for section in cp.sections():
            if cp.items(section=section):
                options = dict(cp.items(section=section))

                if options.get('filebase'):
                    dictfile = os.path.join(basedir, options['filebase'])
                else:
                    # no dictfile, warning?
                    continue

                name = section if use_section_name else options.get('name')

                try:
                    dictionary = Dict(dictfile, name)
                    dictionary.load_dict()
                    self.dicts.append(dictionary)
                except Exception:
                    warnings.warn(f'There is an issue loading dictionary with '
                                  f'filebase {options["filebase"]}.')
    def keys(self):
        if not self._keys:
            keys = []
            for d in self.dicts:
                keys += d.keys()
            self._keys = sorted(list(set(keys)))

        return self._keys

    def get_definition(self, key):
        result = {}
        for dict_ in self.dicts:
            definition = dict_.value(key)
            if not definition:
                continue
            result[dict_.name] = definition
        return result

    def match_words(self, phrase):
        if not self._keys:
            self.keys()

        result = []
        if len(phrase) < 4:
            # do matching based only on the beginning of the word match to the
            # phrase.
            for k in self._keys:
                if k.startswith(phrase):
                    result.append(k)
            return result

        for k in self._keys:
            if rapidfuzz.fuzz.ratio(k, phrase) > 85:
                result.append(k)
        return result

import configparser
import os
import sys
import warnings

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
        try:
            cp.read(conf)
        except configparser.Error as err:
            print("There were errors reading config: %s" % err.message)
            sys.exit(10)

        defaults = {'basedir': '',
                    'use-section-name': False,
                    'max-definitions': -1,
                    'len-phrase': 4,
                    'fuzzy-ratio': 85}

        for key in defaults:
            try:
                if key in ('max-definitions', 'len-phrase', 'fuzzy-ratio'):
                    defaults[key] = cp.getint('DEFAULT', key)
                else:
                    defaults[key] = cp.get('DEFAULT', key)
            except (configparser.NoOptionError, ValueError):
                pass

        self.conf = defaults

        for section in cp.sections():
            if cp.items(section=section):
                options = dict(cp.items(section=section))
                if options.get('basedir'):
                    basedir = options.get('basedir')
                else:
                    basedir = defaults['basedir']

                if options.get('filebase'):
                    dictfile = os.path.join(basedir, options['filebase'])
                else:
                    warnings.warn(f'Dictionary filebase in section {section} '
                                  f'not found. Check your configuration')
                    continue

                name = (section if defaults['use-section-name'] else
                        options.get('name'))

                try:
                    dictionary = Dict(dictfile, name)
                    dictionary.load_dict()
                    self.dicts.append(dictionary)
                except Exception:
                    warnings.warn(f'There is an issue loading dictionary with '
                                  f'filebase {options["filebase"]}.')

        try:
            find_recursively = cp.get('DEFAULT', 'find-recursively-dir')
            if not find_recursively:
                return
            for root, dires, files in os.walk(find_recursively):
                for fname in files:
                    if fname.lower().endswith('.ifo'):
                        fpath = os.path.join(root, fname[:-4])
                        try:
                            d = Dict(fpath)
                            d.load_dict()
                            self.dicts.append(d)
                        except Exception:
                            warnings.warn(f'There is an issue loading '
                                          f'dictionary with filebase '
                                          f'{fpath}.')
        except configparser.NoOptionError:
            pass

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

        # if phrase is empty, return, depending on the settings
        if not phrase:
            if self.conf['max-definitions'] < 0:
                # all keys
                return list(self._keys)
            elif self.conf['max-definitions'] == 0:
                # no keys
                return []
            else:
                # only fixed amount of keys
                return list(self._keys[:self.conf['max-definitions']])

        result = []
        if len(phrase) < self.conf['len-phrase']:
            # do matching based only on the beginning of the word match to the
            # phrase.
            for k in self._keys:
                if k.startswith(phrase):
                    result.append(k)
            if self.conf['max-definitions'] > 0:
                return result[:self.conf['max-definitions']]
            else:
                return result

        for k in self._keys:
            if rapidfuzz.fuzz.ratio(k, phrase) > self.conf['fuzzy-ratio']:
                result.append(k)
        if self.conf['max-definitions'] > 0:
            return result[:self.conf['max-definitions']]
        else:
            return result

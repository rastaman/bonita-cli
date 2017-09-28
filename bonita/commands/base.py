"""The base command."""

import os
import pickle


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.configurationPath = os.environ['HOME'] + '/.bonita'
        self.results = None
        self.headless = False

    def run(self):
        raise NotImplementedError(
            'You must implement the run() method yourself!')

    def loadConfiguration(self):
        if os.path.exists(self.configurationPath):
            with open(self.configurationPath) as f:
                return pickle.load(f)
        else:
            return dict()

    def saveConfiguration(self, configuration):
        with open(self.configurationPath, 'w') as f:
            pickle.dump(configuration, f)

    def processResults(self, rc, datas):
        if self.headless:
            self.results = dict(rc=rc, datas=datas)
        else:
            if rc == 200:
                print(datas)
            else:
                print('KO - %d' % rc)

    def processResultCode(self, rc):
        if self.headless:
            self.results = dict(rc=rc)
        else:
            if rc == 200:
                print('OK')
            else:
                print('KO - %d' % rc)

    def hasOption(self, option):
        return option in self.options and self.options[option]

    def getResults(self):
        return self.results

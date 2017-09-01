"""The base command."""

import os
import pickle
import requests


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.configurationPath = os.environ['HOME'] + '/.bonita'

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')

    def loadConfiguration(self):
        with open( self.configurationPath ) as f:
            configuration = pickle.load(f)
            configuration['cookies'] = requests.utils.cookiejar_from_dict(configuration['cookies'])
            return configuration

    def saveConfiguration(self, configuration):
        with open( self.configurationPath, 'w') as f:
            pickle.dump( configuration, f)

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
        if os.path.exists( self.configurationPath ):
            with open( self.configurationPath ) as f:
                configuration = pickle.load(f)
                if 'cookies' in configuration:
                    print(configuration['cookies'])
                    configuration['cookies'] = requests.utils.cookiejar_from_dict(configuration['cookies'])
                if 'platform_cookies' in configuration:
                    configuration['platform_cookies'] = requests.utils.cookiejar_from_dict(configuration['platform_cookies'])
                return configuration
        else:
            return dict()

    def saveConfiguration(self, configuration):
        with open( self.configurationPath, 'w') as f:
            pickle.dump( configuration, f)

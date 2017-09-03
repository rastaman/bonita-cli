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

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')

    def loadConfiguration(self):
        if os.path.exists( self.configurationPath ):
            with open( self.configurationPath ) as f:
                return pickle.load(f)
        else:
            return dict()

    def saveConfiguration(self, configuration):
        with open( self.configurationPath, 'w') as f:
            pickle.dump( configuration, f)

"""The upload command."""


from json import dumps

from .base import Base

import os
import requests
import requests.utils
import pickle


class Upload(Base):
    """Manage uploads"""

    def run(self):
        configuration = self.loadConfiguration()
        #print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))


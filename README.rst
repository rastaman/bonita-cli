bonita-cli
==========

*A command line client for Bonita.*


Purpose
-------

This is a command line client which allows to interact with the Bonita BPM platform.

Usage
-----

You first need to open a session in Bonita, the command you'll want to run is::

    $ bonita session login <url> <username> <password>

Before you leave, close your session::

    $ bonita session logout

All commands::

    $ bonita session [login <url> <username> <password>|logout|get]
    $ bonita system [tenant [get|pause|resume]]
    $ bonita platform [login <url> <username> <password>|logout|get|start|stop]
    $ bonita upload <type> <filename>
    $ bonita -h | --help
    $ bonita --version

Examples::

    $ bonita session login http://myhost:8080/bonita myusername mypassword
    $ bonita system tenant pause

Help
----

For help using this tool, please open an issue on the Github repository:
https://github.com/rastaman/bonita-cli

References
----------

 * `Building Simple Command Line Interfaces in Python <https://stormpath.com/blog/building-simple-cli-interfaces-in-python>`__

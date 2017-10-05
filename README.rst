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

    bonita session [login <url> <username> <password>|logout|get]
    bonita system [tenant [get|pause|resume]]
    bonita platform [login <url> <username> <password>|logout|get|start|stop]
    bonita upload <type> <filename>
    bonita process [deploy <filename_on_server>|get [<process_id>]|enable <process_id>|disable <process_id>]
    bonita portal [page [deploy <filename_on_server>|get <page_id>|update <page_id> <filename_on_server>]]
    bonita application [get [<application_id>]|create <filename>|update <application_id> <filename>|delete <application_id>|import <server_filename>]
    bonita packaging [generate <dist_folder> <descriptor_file>|install <dist_folder> <descriptor_file>]
    bonita organization [import <filename>|export|delete]
    bonita bdm [install <filename>|uninstall|cleanAndUninstall|get [version|clientZip <filename>]]
    bonita profile [import <filename>|export <filename>|search [<criteria>]|merge <default_profiles> <custom_profiles> <output_profiles>]
    bonita user [add <login> <password> [<manager_id>]|get [<user_id>]|enable <user_id>|disable <user_id>|remove <user_id>]
    bonita membership [add <user_id> <group_id> <role_id>|get <user_id>|remove <user_id> <group_id> <role_id>]
    bonita -h | --help
    bonita --version

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

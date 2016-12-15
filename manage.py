#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    if 'TRAVIS' in os.environ:
        default = 'config.settings.testing'
    else:
        default = 'config.settings.local'

    print (default)

    # default = 'config.settings.testing'

    # for production / staging environments, the correct settings
    # module is already set as an environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

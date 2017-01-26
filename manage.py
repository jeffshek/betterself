#!/usr/bin/env python
import os
import sys

import environ
env = environ.Env()

if __name__ == '__main__':
    if 'test' in sys.argv:
        default = 'config.settings.settings_testing'
    else:
        default = 'config.settings.local'

    # for production / staging environments, the correct settings
    # module is already set as an environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

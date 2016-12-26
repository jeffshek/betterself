#!/usr/bin/env python
import os
import sys

import environ
env = environ.Env()

if __name__ == '__main__':
    if 'TRAVIS' in os.environ:
        default = 'config.settings.testing'
    else:
        default = 'config.settings.local'

    # for production / staging environments, the correct settings
    # module is already set as an environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default)

    print ('Settings are being set from {}'.format(env('DJANGO_SETTINGS_MODULE')))

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

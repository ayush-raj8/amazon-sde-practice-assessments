#!/usr/bin/env python3
import os
import sys


def main():
    # Entry point → loads DJANGO_SETTINGS_MODULE (config.settings).
    # Trace starts here when you run: python manage.py runserver
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

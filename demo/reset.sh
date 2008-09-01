#!/bin/sh

find . -name '*.pyc' -print -delete
rm -f database.sqlite && ./manage.py syncdb --noinput


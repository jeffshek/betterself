#!/usr/bin/env bash
apt-get update -y
apt-get install python-pip -y

pip install virtualenv
pip install virtualenvwrapper

export WORKON_HOME=/betterself/config/development/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv betterself

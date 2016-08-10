#!/usr/bin/env bash
apt-get update -y
apt-get install python-pip -y
apt-get install libpq-dev python-dev -y
apt-get install git -y
apt-get install g++ -y

# td - way too much crap here try to simplify dependency chain
apt-get install libjpeg-dev -y # pillow
apt-get install libncurses5-dev libffi-dev -y
apt-get install gcc -y
apt-get libxslt1-dev -y
apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 -y

pip install virtualenv
pip install virtualenvwrapper

export WORKON_HOME=/betterself/config/development/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

# use only python 3, this defaults to python 3.4.3
mkvirtualenv betterself --python=/usr/bin/python3

workon betterself
pip install --upgrade setuptools

# local environments should have all requirements installed
pip install -r /betterself/requirements/production.txt
pip install -r /betterself/requirements/test.txt
pip install -r /betterself/requirements/local.txt

if ! command -v psql; then
    apt-get install postgresql -y
    # Create vagrant pgsql superuser
    su - postgres -c "createuser -s vagrant"
    su - postgres -c "createdb betterself"
fi

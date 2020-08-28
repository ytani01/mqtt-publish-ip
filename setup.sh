#!/bin/sh
#
# (c) 2020 Yoichi Tanibayashi
#
GITS="ytMQTT"
GITADDR="git@github.com:ytani01"

##############################################################################
MYNAME=`basename $0`
MYDIR=`dirname $0`
echo "MYDIR=$MYDIR"
cd $MYDIR
echo "===" `pwd`
##############################################################################
if [ -z "$VIRTUAL_ENV" ]; then
    echo "$MYNAME: Please activate venv"
    exit 1
fi
VENVNAME=`basename $VIRTUAL_ENV`
echo "VENVNAME=$VENVNAME"
##############################################################################
# update pip
echo "=== update pip command"
set -x
pip install -U pip
hash -r
pip -V
set +x
##############################################################################
# install python packages
echo "=== install python packages"
set -x
pip install -r requirements.txt
set +x
##############################################################################
# git clone
cd $VIRTUAL_ENV
echo "=== clone git repos in" `pwd`
for g in $GITS; do
    if [ ! -d $g ]; then
        set -x
        git clone "${GITADDR}/${g}.git"
        set +x
    fi
done

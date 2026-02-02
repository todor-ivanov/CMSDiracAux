WDIR=$( dirname -- "${BASH_SOURCE[0]}" )
WDIR=$(realpath $WDIR)
# realpath ${BASH_SOURCE[0]}
# export PYTHONPATH=$PWD/src/python/WMCore.zip:$PWD/src/python/PSetTweaks.zip:$PWD/src/python/Utils.zip:$PWD/src/python:$PWD:$PYTHONPATH
export PYTHONPATH=$WDIR/src/python/WMCore.zip:$WDIR/src/python/PSetTweaks.zip:$WDIR/src/python/Utils.zip:$WDIR/src/python:$WDIR:$PYTHONPATH
export PATH=$WDIR/bin:$PATH

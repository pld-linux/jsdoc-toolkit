#!/bin/sh
# launcher script for jsdoc

JSDOCDIR=/usr/share/jsdoc
TDIR=""

if [ -n "$JSDOCTEMPLATEDIR" ]; then
	TDIR="-Djsdoc.template.dir=$JSDOCTEMPLATEDIR"
fi

exec java -Djsdoc.dir=$JSDOCDIR $TDIR -jar $JSDOCDIR/jsrun.jar $JSDOCDIR/app/run.js "$@"

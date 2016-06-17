#/bin/bash
VERSION="0.1"
PROGNAME=$(basename $0)
TODAY=$(date +%F)
LOGDIR="log"
PREFIX="bflog"

if [ "$1" == "" ] ; then
	echo "### $PROGNAME - v$VERSION" >&2
	echo "    Usage:" >&2
	echo "    $PROGNAME add [category] [text]: add text to log file" >&2
	echo "    $PROGNAME send person@example.com: send results of last 7 days" >&2
	exit 0
fi

if [ $1 == "add" ] ; then
	if [ -z "$3" ] ; then
		echo "    $PROGNAME ERROR: need 3 parameters for 'add'" >&2
		exit 1
	else
		LOGFILE=$LOGDIR/$PREFIX.$TODAY.$2.log
		NOW=$(date --rfc-3339=s)
		shift 2
		echo "$NOW;$*" >> $LOGFILE
	fi
fi

if [ $1 == "send" ] ; then
	if [ -z "$2" ] ; then
		echo "    $PROGNAME ERROR: need 2 parameters for 'send'" >&2
		exit 1
	else
		EMAIL=$2
		DAYS=$(find log/ -mtime -7 -name bflog.\* -exec basename {} \; | cut -d. -f2 | sort -u)
		if [ ! -z "$DAYS" ] ; then
			# there are log files!
			for DAY in $DAYS ; do 
				echo $DAY
			done
		fi
	fi
fi
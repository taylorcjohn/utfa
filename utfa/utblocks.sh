#!/bin/bash
#
# utblocks.sh
#
# create byte file
#
# John Taylor (onefouronefour limited)
#
# 2021-12-03 19:30
#
################################################

if [ -z "$AWK" ]; then
	AWK=/usr/bin/awk
	# echo setting AWK = $AWK
fi

UTFADIR=~/Documents/GitHub/utfa/utfa

progress='X'

$AWK -v progress=$progress '
BEGIN	{
			FS = "."
			printf("%s\n", "blocks = [")
		}
		{
			a=$1
			d=index($3,";")
			b=substr($3,0,d-1)
			c=substr($3,d+2)
			printf("\t\t\t(0x%s,0x%s,\"%s\"),\n", a, b, c)
		}
END		{
			printf("\t\t%s\n", "]")
		}
' < $UTFADIR/Blocks-in > $UTFADIR/Blocks-out

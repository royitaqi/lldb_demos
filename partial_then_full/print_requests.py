#!/usr/bin/python3

import sys
import datetime

now = datetime.datetime.now()
uuid = sys.argv[1]
log = "%s Pulling dsym for %s" % (now.strftime("%H:%M:%S"), uuid)

f = open("log.txt", "a")
f.write(log + "\n")

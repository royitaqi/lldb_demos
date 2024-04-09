#!/usr/bin/python3

import sys
import datetime

should_return = True
target_uuid = '17FE9926-7AB6-49B8-9D1C-F8F3C694F5BE'
now = datetime.datetime.now()
uuid = sys.argv[1]
log = "%s Pulling dsym for %s" % (now.strftime("%H:%M:%S"), uuid)

f = open("pull_dsym.log", "a")
f.write(log + "\n")

if should_return and uuid == target_uuid:
    print("""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>%s</key>
    <dict>
        <key>DBGDSYMPath</key>
        <string>/tmp/a.out.dSYM/Contents/Resources/DWARF/a.out</string>
    </dict>
</dict>
</plist>
    """ % target_uuid)
    f.write("dSYM returned for %s\n" % target_uuid)

f.close()

# import time
# time.sleep(1)

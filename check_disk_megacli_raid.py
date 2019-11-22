#!/usr/bin/env python3

import os
import sys

fail = []

result = os.popen("""/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -a0 \
     | grep -E '(Slot Number)|(Firmware state)' \
     | sed ':a;N;$!ba;s/\\nFirmware state: /\:/g' \
     | grep -Eo '[0-9]+:[^,]+'""")

c = 0
for i in result:
    if not (i.endswith("Online\n") or i.endswith("Hotspare\n")):
        fail.append(c)
    c += 1

if len(fail) == 0:
    print("OK | All disks are operating within normal parameters")
    sys.exit(0)

print("FAIL - FAILED DISK NO.", "/".join(fail))
sys.exit(2)

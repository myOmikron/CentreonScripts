#!/usr/bin/env python3

import os
import sys

online = []
hotspare = []
unknown = []

output = []

result = os.popen("""/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -a0 \
     | grep -E '(Slot Number)|(Firmware state)' \
     | sed ':a;N;$!ba;s/\\nFirmware state: /\:/g' \
     | grep -Eo '[0-9]+:[^,]+'""")

c = 0
for line in result:
    output.append(line[:-1])
    if line.endswith("Online\n"):
        online.append(c)
    elif line.endswith("Hotspare\n"):
        hotspare.append(c)
    else:
        unknown.append(c)
    c += 1

if len(unknown) == 0:
    print("DISKS OK - Online: {}, Hotspare: {}|{}".format(
        "/".join([str(i) for i in online]),
        "/".join([str(i) for i in hotspare]),
        "\n".join(output)
    ))
    sys.exit(0)

else:
    print("DISKS FAILURE - Unknown: {}|{}".format(
        "/".join(others),
        "\n".join(output)
    ))
    sys.exit(2)


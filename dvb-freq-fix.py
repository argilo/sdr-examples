#!/usr/bin/env python

import os
import os.path
import struct

OLD_RTL2832_MAX =  862000000
OLD_R820T_MAX   = 1002000000
NEW_MAX         = 1750000000

def module_replace_bytes(filename, old_bytes, new_bytes):
    print("Replacing maximum frequency in " + filename)
    if os.path.isfile(filename + "-original"):
        raise Exception("Kernel module was already patched")
    if not os.path.isfile(filename):
        raise Exception("Kernel module not found")

    os.system("objcopy " + filename + " " + filename + "-unsigned")
    if not os.path.isfile(filename + "-unsigned"):
        raise Exception("Objcopy failed")

    with open(filename + "-unsigned", "rb") as f:
        bytes = f.read()
    if bytes.count(old_bytes) != 1:
        os.remove(filename + "-unsigned")
        raise Exception("Bytes not found in kernel module")

    os.rename(filename, filename + "-original")

    with open(filename, "wb") as f:
        f.write(bytes.replace(old_bytes, new_bytes))
    os.remove(filename + "-unsigned")
    print("Success!")

old_rtl2832_bytes = struct.pack("i", OLD_RTL2832_MAX)
old_r820t_bytes   = struct.pack("i", OLD_R820T_MAX)
new_max_bytes     = struct.pack("i", NEW_MAX)

module_path = '/lib/modules/' + os.uname()[2]
module_replace_bytes(module_path + "/kernel/drivers/media/dvb-frontends/rtl2832.ko", old_rtl2832_bytes, new_max_bytes)
module_replace_bytes(module_path + "/kernel/drivers/media/tuners/r820t.ko", old_r820t_bytes, new_max_bytes)

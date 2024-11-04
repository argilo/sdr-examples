#!/usr/bin/env python3

import os
import os.path
import struct

OLD_RTL2832_MAX = 862000000
OLD_R820T_MAX = 1002000000
NEW_MAX = 1750000000


def module_replace_bytes(filename, old_bytes, new_bytes):
    print(f"Replacing maximum frequency in {filename}.zst")
    if os.path.isfile(f"{filename}.zst-original"):
        raise Exception("Kernel module was already patched")
    if not os.path.isfile(f"{filename}.zst"):
        raise Exception("Kernel module not found")

    temp_file = "/tmp/" + filename.split("/")[-1]
    os.system(f"unzstd -c {filename}.zst > {temp_file}")
    if not os.path.isfile(temp_file):
        raise Exception("Failed to decompress {filename}.zst")

    os.system(f"objcopy {temp_file} {temp_file}-unsigned")
    os.remove(temp_file)
    if not os.path.isfile(f"{temp_file}-unsigned"):
        raise Exception("Objcopy failed")

    with open(f"{temp_file}-unsigned", "rb") as f:
        bytes = f.read()
    if bytes.count(old_bytes) != 1:
        os.remove(f"{temp_file}-unsigned")
        raise Exception("Bytes not found in kernel module")

    with open(f"{temp_file}-unsigned", "wb") as f:
        f.write(bytes.replace(old_bytes, new_bytes))

    os.rename(f"{filename}.zst", f"{filename}.zst-original")
    os.system(f"zstd -c {temp_file}-unsigned > {filename}.zst")

    os.remove(f"{temp_file}-unsigned")
    print("Success!")


old_rtl2832_bytes = struct.pack("i", OLD_RTL2832_MAX)
old_r820t_bytes = struct.pack("i", OLD_R820T_MAX)
new_max_bytes = struct.pack("i", NEW_MAX)

module_path = "/lib/modules/" + os.uname()[2]
module_replace_bytes(module_path + "/kernel/drivers/media/dvb-frontends/rtl2832.ko", old_rtl2832_bytes, new_max_bytes)
module_replace_bytes(module_path + "/kernel/drivers/media/tuners/r820t.ko", old_r820t_bytes, new_max_bytes)

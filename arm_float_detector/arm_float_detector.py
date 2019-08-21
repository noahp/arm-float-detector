"""
Utility to sniff out soft float function calls in arm object code (.o, .a,
.elf).
"""

import argparse
import subprocess

# Soft float library functions are enumerated here:
# https://github.com/gcc-mirror/gcc/blob/master/libgcc/config/arm/sfp-machine.h#L90-L108
# Manually copied into this list.
DOUBLE_DEFINES = """
#define __negdf2	__aeabi_dneg
#define __subdf3	__aeabi_dsub
#define __adddf3	__aeabi_dadd
#define __floatunsidf	__aeabi_ui2d
#define __floatsidf	__aeabi_i2d
#define __extendsfdf2	__aeabi_f2d
#define __truncdfsf2	__aeabi_d2f
#define __floatundidf	__aeabi_ul2d
#define __floatdidf	__aeabi_l2d
#define __muldf3	__aeabi_dmul
#define __divdf3	__aeabi_ddiv
#define __unorddf2	__aeabi_dcmpun
#define __fixdfsi	__aeabi_d2iz
#define __fixunsdfsi	__aeabi_d2uiz
#define __fixdfdi	__aeabi_d2lz
#define __fixunsdfdi	__aeabi_d2ulz
#define __floatdidf	__aeabi_l2d
#define __extendhfsf2	__gnu_h2f_ieee
#define __truncsfhf2	__gnu_f2h_ieee
"""
DOUBLE_FUNCTIONS = (x.split()[2] for x in DOUBLE_DEFINES.strip().splitlines())


def parse_args():
    """Parse cmd line args"""
    parser = argparse.ArgumentParser(description="Detect soft double in arm binaries")
    parser.add_argument("binary", metavar="FILE", help=".o/.a/.elf to process")
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    return parser.parse_args()


def main():
    """Cli entrance point"""

    args = parse_args()

    cmd = "nm {} | grep -E '{}'".format(args.binary, "|".join(DOUBLE_FUNCTIONS))
    retcode = subprocess.call(cmd, shell=True)
    if retcode == 0:
        # failure, exit non-zero!
        exit(-1)
    else:
        print("No soft double libs found!")
    exit(0)


if __name__ == "__main__":
    main()

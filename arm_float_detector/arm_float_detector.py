# -*- coding: UTF-8 -*-
"""
Utility to sniff out soft float function calls in arm object code (.o, .a,
.elf).
"""

from __future__ import print_function
from __future__ import absolute_import
import argparse
import subprocess
import sys

VERSION = "0.2.1"


# Soft float library functions are enumerated here, single + double:
# https://github.com/gcc-mirror/gcc/blob/master/libgcc/config/arm/sfp-machine.h
# Manually copied into these lists.
def gen_define_list(defines):
    """Return a generator of the references we care about"""
    # world's greatest clang define parser right here 😞
    return (x.split()[2] for x in defines.strip().splitlines())


SINGLE_DEFINES = """
#define __negsf2	__aeabi_fneg
#define __subsf3	__aeabi_fsub
#define __addsf3	__aeabi_fadd
#define __floatunsisf	__aeabi_ui2f
#define __floatsisf	__aeabi_i2f
#define __floatundisf	__aeabi_ul2f
#define __floatdisf	__aeabi_l2f
#define __mulsf3	__aeabi_fmul
#define __divsf3	__aeabi_fdiv
#define __unordsf2	__aeabi_fcmpun
#define __fixsfsi	__aeabi_f2iz
#define __fixunssfsi	__aeabi_f2uiz
#define __fixsfdi	__aeabi_f2lz
#define __fixunssfdi	__aeabi_f2ulz
#define __floatdisf	__aeabi_l2f
"""
SINGLE_FUNCTIONS = gen_define_list(SINGLE_DEFINES)

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
DOUBLE_FUNCTIONS = gen_define_list(DOUBLE_DEFINES)


def print_color(msg, color):
    """Print a ansi term color string"""
    if sys.stdout.isatty():
        print("\033[{}m{}\033[m".format(color, msg))
    else:
        print(msg)


def error(msg, terminate=True):
    """Print colorful text, optionally exit"""
    print_color(msg, 31)
    if terminate:
        exit(-1)


def success(msg):
    """Print colorfully positive text"""
    print_color(msg, 32)


def detect(binary, single, double):
    """Detect. binary path, single=boolean, double=boolean. Returns True if
    detected, False if not"""
    grepfor = ""
    if single:
        grepfor += "|".join(SINGLE_FUNCTIONS)
    if double:
        grepfor += "|".join(DOUBLE_FUNCTIONS)

    # grep for whole words (-w) to not show the *_veneer symbols
    cmd = "nm {} | grep -w -E '{}'".format(binary, grepfor)
    retcode = subprocess.call(cmd, shell=True)

    return retcode == 0


def parse_args():
    """Parse cmd line args"""
    parser = argparse.ArgumentParser(description="Detect soft double in arm binaries")
    parser.add_argument("binary", metavar="FILE", help=".o/.a/.elf to process")
    parser.add_argument(
        "--single", action="store_true", help="detect single-precision references"
    )
    parser.add_argument(
        "--double", action="store_true", help="detect double-precision references"
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(VERSION)
    )
    return parser.parse_args()


def main():
    """Cli entrance point"""

    args = parse_args()

    if not (args.single or args.double):
        error("Specify one or both of --single / --double")

    if detect(args.binary, args.single, args.double):
        # failure, exit non-zero!
        exit(-1)
    else:
        success(
            "No soft {} libs found!".format(
                "/".join(
                    (["single"] if args.single else [])
                    + (["double"] if args.double else [])
                )
            )
        )
    exit(0)


if __name__ == "__main__":
    main()

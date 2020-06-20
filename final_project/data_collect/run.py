#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call collect.py to collect data of sample files"""

import collectv2_class


with open('3001-4000.txt', 'r') as f_object:
    files = [line.rstrip() for line in f_object.readlines()]
# files = ["arch/arm/mach-iop32x/gpio-iop32x.h", "arch/arm/mach-iop32x/Kconfig",
#           "arch/alpha/kernel/bugs.c", "arch/alpha/kernel/core_wildfire.c", "arch/alpha/kernel/proto.h",
#           "arch/alpha/kernel/sys_sio.c", "arch/alpha/kernel/traps.c",
#           "arch/arm/probes/kprobes/checkers-arm.c", "arch/arm/probes/kprobes/test-arm.c",
#           "arch/nds32/kernel/signal.c", "arch/nds32/kernel/syscall_table.c"]
result_csv = 'class_results.csv'
collectv2_class.run(files, result_csv)
# collectv2_class.blame_many(files)

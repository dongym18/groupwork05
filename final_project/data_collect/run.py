#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Call collect.py to collect data"""

__author__ = "YeYinru"
__copyright__ = "Copyright2020,Group05 Final_Project"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = ["YeYinru", "YanHaoqiu"]

import collectv2_class


with open('3001-4000.txt', 'r') as f_object:
    files = [line.rstrip() for line in f_object.readlines()]
# files = ["arch/arm/mach-iop32x/gpio-iop32x.h", "arch/arm/mach-iop32x/Kconfig",
#           "arch/nds32/kernel/signal.c", "arch/nds32/kernel/syscall_table.c"]
result_csv = 'class_results.csv'
collectv2_class.run(files, result_csv)

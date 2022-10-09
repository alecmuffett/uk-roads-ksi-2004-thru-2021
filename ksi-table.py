#!/usr/bin/env python3

import csv
import re
import sys
import pprint

def get_file(srcname):
    with open(srcname, newline='') as srcfile: # IMPT: use newline='' to preserve infix "\r\n"
        reader = csv.DictReader(srcfile)
        rows = [x for x in reader]
        return rows

def make_table(rows):
    result = dict()
    for row in rows:
        lo = int(row['lo'])
        hi = int(row['hi'])
        year = row['year']
        ksi = row['ksi']
        if hi > 0:
            age_range = 'age {lo:02}-{hi:02}'.format(lo=lo, hi=hi)
        else:
            age_range = 'not logged'
        bucket = result.get(age_range, None)
        if not bucket:
            bucket = dict()
            bucket['age range'] = age_range
            result[age_range] = bucket
        bucket[year] = ksi
    return result

if __name__ == '__main__':
    fieldnames = ['age range']
    for i in range(2004, 2022):
        fieldnames.append(str(i))

    rows = get_file(sys.argv[1])
    table = make_table(rows)

    dstname = 'table.csv'
    with open(dstname, 'w', newline='') as dstfile:
        writer = csv.DictWriter(dstfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(table.keys()):
            writer.writerow(table[key])

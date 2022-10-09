#!/usr/bin/env python3

# Data Extract:
# https://roadtraffic.dft.gov.uk/custom-downloads/road-accidents
# Casualties
# Killed or seriously injured (KSI) adjusted
# All Years
# Great Britain, countries and regions
# Great Britain
# Casualty age
# Confirm
# Your report reference is 14fa598f-ea9c-4e5d-8db4-d2a6d32ac70c
# https://roadtraffic.dft.gov.uk/custom-downloads/road-accidents/reports/14fa598f-ea9c-4e5d-8db4-d2a6d32ac70c

import csv
import re
import sys
import pprint

YEAR = 'Accident year'
AGE = 'Casualty age'
KSI = 'Killed or seriously injured adjusted'

class Bucket:
    def __init__(self, key, lo, hi):
        self.key = key
        self.lo = lo
        self.hi = hi
        self.years = dict()

    def apply(self, row):
        age = row[AGE]
        if (re.match(r'\d+$', age)):
            iage = int(age) # now integer
            if iage > self.hi: return
            if iage < self.lo: return
        elif self.hi < 0: # flag to capture non-integer ages
            pass
        else:
            return
        ksi = row[KSI]
        if ksi == '':
            return # blank data
        year = int(row[YEAR])
        tally = self.years.get(year, 0.0)
        tally += float(ksi)
        self.years[year] = tally
        #print(tally, row)
        #print(self.years)

    def results(self):
        results = []
        for year in self.years.keys():
            row = dict()
            row['key'] = self.key
            row['lo'] = self.lo
            row['hi'] = self.hi
            row['year'] = year
            row['ksi'] = self.years[year]
            results.append(row)
        return results

def get_file(srcname):
    with open(srcname, newline='') as srcfile: # IMPT: use newline='' to preserve infix "\r\n"
        reader = csv.DictReader(srcfile)
        rows = [x for x in reader]
        return rows

if __name__ == '__main__':
    # https://ico.org.uk/for-organisations/guide-to-data-protection
    # /ico-codes-of-practice/age-appropriate-design-a-code-of-practice-for-online-services
    # /annex-b-age-and-developmental-stages/?q=security
    buckets = (
        Bucket('unknown', -1, -1),
        Bucket('early years', 0, 5),
        Bucket('core primary', 6, 9),
        Bucket('transition', 10, 12),
        Bucket('early teens', 13, 15),
        Bucket('late teens', 16, 17),
        Bucket('adult 18-29', 18, 29),
        Bucket('adult 30-49', 30, 49),
        Bucket('adult 50-69', 50, 69),
        Bucket('adult 70-89', 70, 89),
        Bucket('adult 90-109', 90, 109),
        #Bucket('overall u18', 0, 17),
        #Bucket('13-17', 13, 17),
        #Bucket('18-29', 18, 29),
        #Bucket('30-50', 30, 50),
    )

    individual_results = dict()
    all_results = []

    rows = get_file(sys.argv[1])
    for row in rows:
        for bucket in buckets:
            bucket.apply(row)

    for bucket in buckets:
        results = bucket.results()
        individual_results[bucket.key] = results
        all_results.extend(results)

    dstname = 'reduced.csv'
    #pprint.pprint(buckets[0].years)
    with open(dstname, 'w', newline='') as dstfile:
        fieldnames = (
            'key',
            'lo',
            'hi',
            'year',
            'ksi',
        )
        writer = csv.DictWriter(dstfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

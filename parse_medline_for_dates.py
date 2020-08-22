#!/usr/bin/python3

# this script parses titles and abstracts from the MEDLINE baseline

import gzip
import os
import re

months_list = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
               'Summer': 6, 'Winter': 12, 'Fall': 9, 'Spring': 3,
               'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 
               'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12,
}

source_directories = ['/pstore/data/i2e/i2e_sources/Source_Data/MEDLINE_download/2020/Base/']

output_file = "pmid_date.txt"


f_out = open(output_file, "w", encoding = "utf-8")


months_list_keys = sorted(months_list, key=months_list.get)


mesh_heading_area = 0
descriptor_names = []
found = 0
pmid = "0"
abstract = ""
title = ""
year = ""
month = ""
day = ""
pubdate_zone = 0
for source_directory in source_directories:
    print(source_directory)
    files = os.listdir(source_directory)
    # go through every file in MEDLINE
    for file in files:
        input_file = os.path.join(source_directory, file)
        if re.search("\.gz", input_file):
            print(input_file)
            f = gzip.open(input_file, "rt", encoding = "utf-8")
            for line in f:
                line = line[:-1]
                # take the first PMID as the PMID of the record
                if pmid == "0":
                    if re.search("<PMID", line):
                        if re.search("<PMID.*>(.+)<\/PMID>", line):
                            matched = re.search("<PMID.*>(.+)<\/PMID>", line)
                            pmid = matched.group(1)

                # read publication date
                if re.search("<PubDate", line):
                    pubdate_zone = 1
                if re.search("<\/PubDate", line):
                    pubdate_zone = 0
                if pubdate_zone == 1:
                    if re.search("<Year.*>(.+)<\/Year>", line):
                            matched = re.search("<Year.*>(.+)<\/Year>", line)
                            year = matched.group(1)
                    if re.search("<Month.*>(.+)<\/Month>", line):
                            matched = re.search("<Month.*>(.+)<\/Month>", line)
                            month = matched.group(1)
                            if month in months_list_keys:
                                month_index = months_list[month]
                                month = str(month_index)
                    if re.search("<Day.*>(.+)<\/Day>", line):
                            matched = re.search("<Day.*>(.+)<\/Day>", line)
                            day = matched.group(1)
                if re.search("<MedlineDate.*>(.+)<\/MedlineDate>", line):
                            matched = re.search("<MedlineDate.*>(.+)<\/MedlineDate>", line)
                            medlinedate = matched.group(1)
                            for month_name in months_list_keys:
                                if month == "":
                                    if month_name in medlinedate:
                                        month_index = months_list[month_name]
                                        month = str(month_index)
                                        print("==" + month + "--")
                            if re.search("[1-2][0-9][0-9][0-9]", medlinedate):
                                matched = re.search("([1-2][0-9][0-9][0-9])", medlinedate)
                                year = matched.group(1)
                # when the record ends write the output
                if re.search("</MedlineCitation", line):
                    if month == "":
                        month = "01"
                    if day == "":
                        day = "01"
                    date = year + str(month).zfill(2) + str(day).zfill(2)
                    f_out.write(pmid + "\t" + date + "\n")
                    if int(month) < 1 or int(month) > 12:
                        if int(day) < 1 or int(day) > 31:
                            if int(year) < 1000 or int(year) > 2030:
                                f_out.write(pmid + "\t" + date + "\n")
                    pmid = "0"
                    abstract = ""
                    title = ""
                    year = ""
                    month = ""
                    day = ""

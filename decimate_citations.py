#!/usr/bin/python3

# this script eliminates randomly a percentage of citations from the citation data

from random import randrange

input_file = "pmid_citations.txt"
# percentage of citation that will be left after the process
percentage_left = 80
output_file = "pmid_citations_" + str(percentage_left) + ".txt"

f_in = open(input_file, "r")
f_out = open(output_file, "w")

output_pmid = False
current_pmid = ""
input_count = 0
output_count = 0

# delete lines based on a random number
for line in f_in:
    data = line.split("\t")
    pmid1 = data[0]
    input_count += 1
    if pmid1 != current_pmid:
        current_pmid = pmid1
        if randrange(100) > percentage_left-1:
            output_pmid = False
        else:
            output_pmid = True
    if output_pmid == True:
        f_out.write(line)
        output_count += 1

print("Input count: " + str(input_count))
print("Output count: " + str(output_count))

#!/usr/bin/python3

# this script creates a shuffled version of the original network
# the shuffling is done by shuffling all PMIDs (nodes) while keeping the connection structure intact

import random

input_file = "pmid_citations.txt"
output_file = "pmid_citations_shuffled.txt"

# first it reads all PMIDs
print("Reading citations...")
f_in = open(input_file, "r")

pmid_set = set()
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = data[0]
    pmid2 = data[1]
    pmid_set.add(pmid1)
    pmid_set.add(pmid2)

pmid_list = list(pmid_set)

# then it assigns each PMID to another randomly chosen PMID from the network
shuffled_pmid_list = pmid_list.copy()

print("Shuffling...")
random.shuffle(shuffled_pmid_list)

print(shuffled_pmid_list[0:5])
print(pmid_list[0:5])
pmid_mapping = dict(zip(pmid_list, shuffled_pmid_list))

# and finally maps the network to the new shuffling
print("Write output...")
f_in = open(input_file, "r")
f_out = open(output_file, "w")

counter = 0
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = data[0]
    pmid2 = data[1]    
    pmid1_shuffled = pmid_mapping[pmid1]
    pmid2_shuffled = pmid_mapping[pmid2]
    f_out.write(pmid1_shuffled + "\t" + pmid2_shuffled + "\n")
    counter += 1

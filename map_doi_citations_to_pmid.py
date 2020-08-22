#!/usr/bin/python3

# this script maps DOIs from Open Citation Index citations
# to PMIDs using the mapping data from the EBI PMID-PMCID-DOI dataset

import re

mapping_file = "./data/PMID_PMCID_DOI.csv"

input_citation_files = ["2019-10-21T22:41:20_10.csv","2019-10-21T22:41:20_11.csv","2019-10-21T22:41:20_12.csv","2019-10-21T22:41:20_13.csv","2019-10-21T22:41:20_14.csv","2019-10-21T22:41:20_15.csv","2019-10-21T22:41:20_16.csv","2019-10-21T22:41:20_17.csv","2019-10-21T22:41:20_18.csv","2019-10-21T22:41:20_19.csv","2019-10-21T22:41:20_1.csv","2019-10-21T22:41:20_20.csv","2019-10-21T22:41:20_21.csv","2019-10-21T22:41:20_22.csv","2019-10-21T22:41:20_23.csv","2019-10-21T22:41:20_24.csv","2019-10-21T22:41:20_25.csv","2019-10-21T22:41:20_26.csv","2019-10-21T22:41:20_27.csv","2019-10-21T22:41:20_28.csv","2019-10-21T22:41:20_29.csv","2019-10-21T22:41:20_2.csv","2019-10-21T22:41:20_30.csv","2019-10-21T22:41:20_31.csv","2019-10-21T22:41:20_32.csv","2019-10-21T22:41:20_33.csv","2019-10-21T22:41:20_34.csv","2019-10-21T22:41:20_35.csv","2019-10-21T22:41:20_36.csv","2019-10-21T22:41:20_37.csv","2019-10-21T22:41:20_38.csv","2019-10-21T22:41:20_39.csv","2019-10-21T22:41:20_3.csv","2019-10-21T22:41:20_40.csv","2019-10-21T22:41:20_41.csv","2019-10-21T22:41:20_42.csv","2019-10-21T22:41:20_43.csv","2019-10-21T22:41:20_44.csv","2019-10-21T22:41:20_45.csv","2019-10-21T22:41:20_46.csv","2019-10-21T22:41:20_47.csv","2019-10-21T22:41:20_48.csv","2019-10-21T22:41:20_49.csv","2019-10-21T22:41:20_4.csv","2019-10-21T22:41:20_50.csv","2019-10-21T22:41:20_51.csv","2019-10-21T22:41:20_52.csv","2019-10-21T22:41:20_53.csv","2019-10-21T22:41:20_54.csv","2019-10-21T22:41:20_55.csv","2019-10-21T22:41:20_56.csv","2019-10-21T22:41:20_57.csv","2019-10-21T22:41:20_58.csv","2019-10-21T22:41:20_59.csv","2019-10-21T22:41:20_5.csv","2019-10-21T22:41:20_60.csv","2019-10-21T22:41:20_61.csv","2019-10-21T22:41:20_62.csv","2019-10-21T22:41:20_63.csv","2019-10-21T22:41:20_6.csv","2019-10-21T22:41:20_7.csv","2019-10-21T22:41:20_8.csv","2019-10-21T22:41:20_9.csv","2020-01-13T19:31:19_1.csv","2020-01-13T19:31:19_2.csv","2020-01-13T19:31:19_3.csv","2020-01-13T19:31:19_4.csv","2020-04-25T04:48:36_1.csv","2020-04-25T04:48:36_2.csv","2020-04-25T04:48:36_3.csv","2020-04-25T04:48:36_4.csv","2020-04-25T04:48:36_5.csv","2020-06-13T18:18:05_1.csv","2020-06-13T18:18:05_2.csv"]

output_citation_file = "pmid_citations.txt"

f_in = open(mapping_file, "r")

# first it reads all the PMID-DOI mappings provided 
# by the EBI mapping file
pmid_doi = {}
pmids = {}
counter=0
matched_counter=0
print("Read mappings of PMID to DOI...")
for line in f_in:
    line = line[:-1]
    data = line.split(",")
    pmid = data[0]
    doi = data[2]
    counter+=1
    if counter / 10000000 == int(counter / 10000000):
        print("Read " + str(counter) + " lines")
    if pmid != "" and doi != "":
        if re.search("[0-9a-z]", doi):
            if pmid not in pmids.keys():
                # DOI links are converted to DOI values
                doi = doi.replace("\"", "")
                doi = doi.replace("https://doi.org/", "")
                pmid_doi[doi] = pmid
                pmids[pmid] = 1
                matched_counter+=1

print("Total entries read: " + str(counter))
print("Number of PMIDs matched to DOIs: " + str(matched_counter))

# then it reads the citation data from the Open Citation Index
# and tries to map each pair of DOIs to PMIDs when possible

f_out = open(output_citation_file, "w")

pmid_pair_list = {}
counter=0
link_counter = 0

for input_citation_file in input_citation_files:
    print(input_citation_file)
    f_in = open("./data/" + input_citation_file, "r")
    for line in f_in:
        data = line.split(",")
        counter+=1
        if counter / 100000000 == int(counter / 100000000):
            print("Read " + str(counter) + " links, " + str(link_counter) + " matched")
        if len(data) > 2:
            doi1 = data[1]
            doi2 = data[2]
            # DOIs are simplified
            doi1 = doi1.replace("\"","")
            doi2 = doi2.replace("\"","")
            # check if there is mapping available for both DOIs
            if doi1 in pmid_doi.keys():
                if doi2 in pmid_doi.keys():
                    link_counter+=1
                    # if so then map DOIs to PMIDs and print output
                    pmid1 = pmid_doi[doi1]
                    pmid2 = pmid_doi[doi2]
                    if pmid1 + "\t" + pmid2 not in pmid_pair_list.keys():
                        f_out.write(pmid1 + "\t" + pmid2 + "\n")
                        pmid_pair_list[pmid1 + "\t" + pmid2] = 1



print("Number of PMIDs matched to DOIs: " + str(matched_counter))

print("Number of citations read: " + str(counter))
print("Number of citations matching PMIDs found: " + str(link_counter))

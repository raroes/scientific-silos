#!/usr/bin/python3

# this script eliminates duplicate facts
# only the one with earliest date is kept

input_interaction_files = ["interactions_chemicals_genes.txt", "interactions_genes_diseases.txt", "interactions_chemicals_diseases.txt"]
input_date_file = "pmid_date.txt"
output_files = ["interactions_chemicals_genes_filtered.txt", "interactions_genes_diseases_filtered.txt", "interactions_chemicals_diseases_filtered.txt"]

# read each input file

for input_interaction_file, output_file in zip(input_interaction_files, output_files):

    print("Input file: " + input_interaction_file)
    print("Reading interactions...")

    f_in = open(input_interaction_file, "r")

    pmids = set()

    # read all PMIDs in the input file
    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        pmid = data[2]
        pmids.add(pmid)

    # read all dates associated to the PMIDs
    print("Reading publication dates...")

    pmid_dates = {}

    f_in = open(input_date_file, "r")

    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        pmid = data[0]
        if pmid in pmids:
            date = data[1]
            pmid_dates[pmid] = date

    # read facts and keep track of the earliest date for each
    print("Selecting earliest found interactions...")

    f_in = open(input_interaction_file, "r")

    interaction_first_date = {}

    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        pmid = data[2]
        node1 = data[0]
        node2 = data[1]
        if node1 > node2:
            node_pair = node2 + "\t" + node1
        else:
            node_pair = node1 + "\t" + node2
        date = ""
        if pmid in pmid_dates.keys():
            date = pmid_dates[pmid]
        else:
            interaction_first_date[node_pair] = 0
        if node_pair not in interaction_first_date:
            interaction_first_date[node_pair] = date
        else:
            first_date = interaction_first_date[node_pair]
            if date != "":
                if int(date) < int(first_date):
                    interaction_first_date[node_pair] = date
 
    # read all facts again but only write out the earliest ones
    print("Writing output...")

    f_in = open(input_interaction_file, "r")
    f_out = open(output_file, "w")

    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        pmid = data[2]
        node1 = data[0]
        node2 = data[1]
        if pmid in pmid_dates.keys():
            date = pmid_dates[pmid]
        if node1 > node2:
            node_pair = node2 + "\t" + node1
        else:
            node_pair = node1 + "\t" + node2
        if node_pair in interaction_first_date:
            if int(interaction_first_date[node_pair]) > 0:
                first_date = interaction_first_date[node_pair]
                if date == first_date:
                    f_out.write(line + "\t" + date + "\n")

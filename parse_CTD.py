#!/usr/bin/python3

# this script parses several CTD files to extract relations between genes, chemicals and diseases

import re

input_files = ["CTD_chem_gene_ixns.tsv", "CTD_genes_diseases.tsv", "CTD_chemicals_diseases.tsv"]
output_files = ["interactions_chemicals_genes.txt", "interactions_genes_diseases.txt", "interactions_chemicals_diseases.txt"]

# because each file has slightly different format, each data point can be located in a different place
# location of second element of pair in each file
node2_positions = [4, 3 ,4]
# location of PMID reference in each file
publication_positions = [10, 8, 9]
# check if there is data missing
empty_checks = [0, 4, 5]

for input_file, output_file, node2_position, publication_position, empty_check in zip(input_files, output_files, node2_positions, publication_positions, empty_checks):
    print("Input file: " + input_file)
    print("Output file: " + output_file)

    f_in = open(input_file, "r")
    f_out = open(output_file, "w")

    already_written = set()

    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        # check if data is complete and not missing any element
        if len(data) > 8 and not "#" in data[0] and ((empty_check > 0 and data[empty_check] != "") or (empty_check == 0)):
            # read nodes from one pair
            node1 = data[1]
            node2 = data[node2_position]
            # nodes need to be different
            if node1 != node2:
                # there should be a publication associated with PMID
                if data[publication_position] != "":
                    publications = data[publication_position].split("|")
                    for pmid in publications:
                        # create one output line for each publication
                        node_pair = node1 + "\t" + node2
                        if node_pair + "\t" + pmid not in already_written:
                            f_out.write(node1 + "\t" + node2 + "\t" + pmid + "\n")
                            already_written.add(node_pair + "\t" + pmid)

    print("Unique node pairs + references read: " + str(len(already_written)))




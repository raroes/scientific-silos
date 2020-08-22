#!/usr/bin/python3

# this file parses each of the CTD datasets
# each dataset has slight differences

import re

input_files = ["CTD_chem_gene_ixns.tsv", "CTD_genes_diseases.tsv", "CTD_chemicals_diseases.tsv"]
output_files = ["interactions_chemicals_genes.txt", "interactions_genes_diseases.txt", "interactions_chemicals_diseases.txt"]
# the first node is always in the same location but not the second node
node2_positions = [4, 3 ,4]
# location of the PMID
publication_positions = [10, 8, 9]
# location that should be checked to see if it is empty
# if empty then ignore
empty_checks = [0, 4, 5]

# read each dataset
for input_file, output_file, node2_position, publication_position, empty_check in zip(input_files, output_files, node2_positions, publication_positions, empty_checks):
    print("Input file: " + input_file)
    print("Output file: " + output_file)

    f_in = open(input_file, "r")
    f_out = open(output_file, "w")

    already_written = set()

    # parse each line of each dataset
    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        # check to see if line had proper structure
        if len(data) > 8 and not "#" in data[0] and ((empty_check > 0 and data[empty_check] != "") or (empty_check == 0)):
            node1 = data[1]
            node2 = data[node2_position]
            if node1 != node2:
                if data[publication_position] != "":
                    # one line may have more than one PMID
                    publications = data[publication_position].split("|")
                    for pmid in publications:
                        node_pair = node1 + "\t" + node2
                        if node_pair + "\t" + pmid not in already_written:
                            f_out.write(node1 + "\t" + node2 + "\t" + pmid + "\n")
                            already_written.add(node_pair + "\t" + pmid)

    print("Unique node pairs + references read: " + str(len(already_written)))




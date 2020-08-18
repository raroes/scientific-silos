#!/usr/bin/python3

import re

input_files = ["CTD_chem_gene_ixns.tsv", "CTD_genes_diseases.tsv", "CTD_chemicals_diseases.tsv"]
output_files = ["interactions_chemicals_genes.txt", "interactions_genes_diseases.txt", "interactions_chemicals_diseases.txt"]
node2_positions = [4, 3 ,4]
publication_positions = [10, 8, 9]
empty_checks = [0, 4, 5]

#input_files = ["CTD_genes_diseases.tsv"]
#output_files = ["interactions_genes_diseases.txt"]
#node2_positions = [3]
#publication_positions = [8]
#empty_checks = [4]

#input_files = ["CTD_chemicals_diseases.tsv"]
#output_files = ["interactions_chemicals_diseases.txt"]
#node2_positions = [4]
#publication_positions = [9]

#input_files = ["CTD_chem_gene_ixns.tsv"]
#output_files = ["interactions_chemicals_genes.txt"]
#node2_positions = [4]
#publication_positions = [10]
#empty_checks = [0]



for input_file, output_file, node2_position, publication_position, empty_check in zip(input_files, output_files, node2_positions, publication_positions, empty_checks):
    print("Input file: " + input_file)
    print("Output file: " + output_file)

    f_in = open(input_file, "r")
    f_out = open(output_file, "w")

    already_written = set()

    for line in f_in:
        line = line[:-1]
        data = line.split("\t")
        #print(line)
        if len(data) > 8 and not "#" in data[0] and ((empty_check > 0 and data[empty_check] != "") or (empty_check == 0)):
            #print(data[empty_check] + "=====")
            node1 = data[1]
            node2 = data[node2_position]
            if node1 != node2:
                if data[publication_position] != "":
                    publications = data[publication_position].split("|")
                    for pmid in publications:
                        node_pair = node1 + "\t" + node2
                        if node_pair + "\t" + pmid not in already_written:
                            f_out.write(node1 + "\t" + node2 + "\t" + pmid + "\n")
                            #print(line)
                            #print(node1 + "\t" + node2 + "\t" + pmid)
                            already_written.add(node_pair + "\t" + pmid)
        #else:
        #    print(line)

    print("Unique node pairs + references read: " + str(len(already_written)))




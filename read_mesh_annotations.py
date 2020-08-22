#!/usr/bin/python3

# read MeSH annotations about chemicals/drugs and diseases

import re

annotation_file = "pmid_mesh.txt"

output_file_chemicals = "pmid_chemicals.txt"
output_file_diseases = "pmid_diseases.txt"

input_file = "d2020.bin"

f_out_chemicals = open(output_file_chemicals, "w")
f_out_diseases = open(output_file_diseases, "w")


# read first the mapping between MeSH terms and their IDs

print("Reading MeSH mappings...")

f_in = open(input_file, "r")

ui_mesh_header = {}
ui_is_chemical = set()
ui_is_disease = set()
for line in f_in:
    line = line[:-1]
    # read MeSH term
    if re.search("MH = (.*)", line):
        matched = re.search("MH = (.*)", line)
        mesh_header = matched.group(1)
        is_chemical = False
        is_disease = False
    # read tree ID for MeSH terms
    if re.search("MN = (.*)", line):
        matched = re.search("MN = (.*)", line)
        mn = matched.group(1)
        # chemical and drug branch of the MeSH tree
        if mn[0] == "D":
            is_chemical = True
        # disease branch of the MeSH tree
        if mn[0] == "C":
            is_disease = True
    # read general ID for MeSH terms
    if re.search("UI = (.*)", line):
        matched = re.search("UI = (.*)", line)
        ui = matched.group(1)
        ui_mesh_header[mesh_header] = ui
        if is_chemical == True:
            ui_is_chemical.add(ui)
        if is_disease == True:
            ui_is_disease.add(ui)


# read MeSH annotations and select those which are chemicals/drugs or diseases

f_in = open(annotation_file, "r")

print("Reading annotation file " + annotation_file + "...")

total_chemical_annotations = 0
total_disease_annotations = 0
already_out = set()
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    mesh_headers = data[1].split("|")
    for mesh_header in mesh_headers:
        if mesh_header in ui_mesh_header.keys():
            ui = ui_mesh_header[mesh_header]
            # check if MeSH term is chemical
            # if yes, then print it out
            if ui in ui_is_chemical:
                output = str(pmid) + "\t" + str(ui)
                if not output in already_out:
                    f_out_chemicals.write(output + "\n")
                    already_out.add(output)
                total_chemical_annotations += 1
            # same for MeSH terms that are diseases
            if ui in ui_is_disease:
                output = str(pmid) + "\t" + str(ui)
                if not output in already_out:
                    f_out_diseases.write(output + "\n")
                    total_disease_annotations += 1
                    already_out.add(output)

print("Total chemical annotations: " + str(total_chemical_annotations))
print("Total disease annotations: " + str(total_disease_annotations))


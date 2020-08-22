#!/usr/bin/python3

# generate the co-occurence files based on the annotations extracted from MeSH and gene2pubmed
# about chemicals/drugs, genes and diseases

# this list has each pair of files that will be used to compute co-occurrence
input_files_pairs = [("pmid_chemicals.txt", "pmid_diseases.txt"), ("pmid_genes.txt", "pmid_diseases.txt"), ("pmid_chemicals.txt", "pmid_genes.txt")]

output_files = ["interactions_chemicals_diseases.txt", "interactions_genes_diseases.txt", "interactions_chemicals_genes.txt"]

# for each pair of files
for input_files, output_file in zip(input_files_pairs, output_files):
    f_in1 = open(input_files[0], "r")
    f_in2 = open(input_files[1], "r")

    pmid_concept1_id = {}
    pmid_concept2_id = {}

    print("Reading pair of files...")
    print(input_files[0])
    print(input_files[1])

    # read all annotations from the first file
    pmids = set()
    for line in f_in1:
        data = line[:-1].split("\t")
        pmid = data[0]
        concept1_id = data[1]
        pmids.add(pmid)
        if pmid in pmid_concept1_id.keys(): 
            pmid_concept1_id[pmid].append(concept1_id)
        else:
            pmid_concept1_id[pmid] = [concept1_id]

    # read all annotations from the second file
    for line in f_in2:
        data = line[:-1].split("\t")
        pmid = data[0]
        concept2_id = data[1]
        pmids.add(pmid)
        if pmid in pmid_concept2_id.keys():
            pmid_concept2_id[pmid].append(concept2_id)
        else:
            pmid_concept2_id[pmid] = [concept2_id]

    print("Combining concepts...")

    f_out = open(output_file, "w")

    # create all the combinatorial pairs 
    # these are pairs created from annotations made to an individual publication (PMID)
    count = 0
    for pmid in pmids:
        if pmid in pmid_concept1_id.keys() and pmid in pmid_concept2_id:
            concepts1 = pmid_concept1_id[pmid]
            for concept1 in concepts1:
                concepts2 = pmid_concept2_id[pmid]
                for concept2 in concepts2:
                    f_out.write(concept1 + "\t" + concept2 + "\t" + pmid + "\n")
                    count += 1

    f_out.close()

    print(str(count) + " interactions found.\n")


#!/usr/bin/python3

# this script creates all the potential AB and BC pairs based on the CTD data
# in cases in which an AC pair exists, this is also added
# in cases in which an AC pair does not exist, a dummy pair is added with PMID 999999

output_file = "interactions_CTD_tuplets.txt"

input_files = ["interactions_chemicals_diseases_filtered.txt", "interactions_chemicals_genes_filtered.txt", "interactions_genes_diseases_filtered.txt"]

already_out = set()
interaction_date = {}
interaction_pmid = {}

# read files with CTD data about relations between genes, chemicals and diseases

for i in range(0,3):

    input_file = input_files[i]

    print("Reading input file: " + input_file)

    f_in = open(input_file, "r")

    counter = 0

    interaction_sets1 = {}
    interaction_sets2 = {}

    for line in f_in:
        counter += 1
        if counter < 100000:
            line = line[:-1]
            data = line.split("\t")
            node1 = data[0]
            node2 = data[1]
            pmid = data[2]
            date = data[3]
            if node1 not in interaction_sets1:
                interaction_sets1[node1] = set()
            interaction_sets1[node1].add(node2)
            if node2 not in interaction_sets2:
                interaction_sets2[node2] = set()
            interaction_sets2[node2].add(node1)
            node_pair = node1 + "\t" + node2
            interaction_date[str(node_pair)] = date
            interaction_pmid[node_pair] = pmid
    # for each file create a different interaction set
    if i == 0:
       interactions_chemical_disease = interaction_sets1
       interactions_disease_chemical = interaction_sets2
    if i == 1:
       interactions_chemical_gene = interaction_sets1
       interactions_gene_chemical = interaction_sets2
    if i == 2:
       interactions_gene_disease = interaction_sets1
       interactions_disease_gene = interaction_sets2

print("Writing output file: " + output_file)

f_out = open(output_file, "w")

output_counter = 0
output_counter_triplets = 0

# start with all chemicals read from CTD
# for each chemical find every gene and disease that have been found in relation to the chemical
chemicals = interactions_chemical_disease.keys()
for chemical in chemicals:
    diseases = []
    if chemical in interactions_chemical_disease.keys():
        diseases = interactions_chemical_disease[chemical]
    genes = []
    if chemical in interactions_chemical_gene.keys():
        genes = interactions_chemical_gene[chemical]
    if genes != [] and diseases != []:
        # here is the loop through all genes and diseases found to be in relation to the chemical
        for gene in genes:
            for disease in diseases:
                publication_dates = []
                node_pairs = []

                # here the nodes that will go into the output are gathered
                node_pair = str(chemical) + "\t" + str(disease)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])

                node_pair = str(chemical) + "\t" + str(gene)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])
                
                node_pair = str(gene) + "\t" + str(disease)
                node_pairs.append(node_pair)
                # if no AC relation exists then a dummy node is created
                interact_date = "999999"     
                if gene in interactions_gene_disease.keys():
                    diseases1 = interactions_gene_disease[gene]
                    if disease in diseases1:
                        interact_date = interaction_date[node_pair] 
                        output_counter_triplets += 1
                publication_dates.append(interact_date)
                
                # sort the relations based on date
                zipped = zip(node_pairs, publication_dates)
                sorted_zipped = sorted(zipped, key=lambda x: x[1])

                counter = 0
                output = ""
                # print the AB-BC-AC relations ordered by time
                for node_pair, publication_date in sorted_zipped:
                    if node_pair in interaction_pmid.keys():
                        pmid = interaction_pmid[node_pair]
                    else:
                        # dummy PMID
                        pmid = "XXXXXXXX"
                    output += node_pair + "\t" + pmid + "\t" + publication_date
                    counter += 1
                    if counter < 3:
                        output += "\t"

                output += "\n"

                # make sure there are no duplicate PMIDs
                if publication_dates[0] != publication_dates[1] and publication_dates[1] != publication_dates[2] and publication_dates[0] != publication_dates[2]:
                    if output not in already_out:
                        already_out.add(output)
                        f_out.write(output)
                        output_counter += 1
                output = ""

# do the same now but starting with genes
output = ""
genes = interactions_gene_disease.keys()
for gene in genes:
    diseases = []
    if gene in interactions_gene_disease.keys():
        diseases = interactions_gene_disease[gene]
    chemicals = []
    if gene in interactions_gene_chemical.keys():
        chemicals = interactions_gene_chemical[gene]
    if chemicals != [] and diseases != []:
        for chemical in chemicals:
            for disease in diseases:
                publication_dates = []
                node_pairs = []

                node_pair = str(gene) + "\t" + str(disease)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])

                node_pair = str(chemical) + "\t" + str(gene)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])

                node_pair = str(chemical) + "\t" + str(disease)
                node_pairs.append(node_pair)


                interact_date = "999999"
                if chemical in interactions_chemical_disease.keys():
                    diseases1 = interactions_chemical_disease[chemical]
                    if disease in diseases1:
                        interact_date = interaction_date[node_pair]
                        output_counter_triplets += 1
                publication_dates.append(interact_date)

                zipped = zip(node_pairs, publication_dates)
                sorted_zipped = sorted(zipped, key=lambda x: x[1])

                output = ""
                counter = 0
                for node_pair, publication_date in sorted_zipped:
                    if node_pair in interaction_pmid.keys():
                        pmid = interaction_pmid[node_pair]
                    else:
                        pmid = "XXXXXXXX"
                    #print(node_pair + "\t" + pmid + "\t" + publication_date)
                    output += node_pair + "\t" + pmid + "\t" + publication_date
                    counter += 1
                    if counter < 3:
                        output += "\t"

                output += "\n"
                if publication_dates[0] != publication_dates[1] and publication_dates[1] != publication_dates[2] and publication_dates[0] != publication_dates[2]:
                    if output not in already_out:
                        already_out.add(output)
                        f_out.write(output)
                        output_counter += 1
                output = ""

# do the same now but starting with diseases
output = ""
diseases = interactions_disease_chemical.keys()
for disease in diseases:
    chemicals = []
    if disease in interactions_disease_chemical.keys():
        chemicals = interactions_disease_chemical[disease]
    genes = []
    if disease in interactions_disease_gene.keys():
        genes = interactions_disease_gene[disease]
    if genes != [] and chemicals != []:
        for gene in genes:
            for chemical in chemicals:
                publication_dates = []
                node_pairs = []

                node_pair = str(chemical) + "\t" + str(disease)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])

                node_pair = str(gene) + "\t" + str(disease)
                node_pairs.append(node_pair)
                publication_dates.append(interaction_date[node_pair])

                node_pair = str(chemical) + "\t" + str(gene)
                node_pairs.append(node_pair)
                interact_date = "999999"
                if gene in interactions_gene_chemical.keys():
                    chemicals1 = interactions_gene_chemical[gene]
                    if chemical in chemicals1:
                        interact_date = interaction_date[node_pair]
                        output_counter_triplets += 1
                publication_dates.append(interact_date)

                zipped = zip(node_pairs, publication_dates)
                sorted_zipped = sorted(zipped, key=lambda x: x[1])

                counter = 0
                for node_pair, publication_date in sorted_zipped:
                    if node_pair in interaction_pmid.keys():
                        pmid = interaction_pmid[node_pair]
                    else:
                        pmid = "XXXXXXXX"
                    
                    output += node_pair + "\t" + pmid + "\t" + publication_date
                    counter += 1
                    if counter < 3:
                        output += "\t"

                output += "\n"
                if publication_dates[0] != publication_dates[1] and publication_dates[1] != publication_dates[2] and publication_dates[0] != publication_dates[2]:
                    if output not in already_out:
                        already_out.add(output)
                        f_out.write(output)
                        output_counter += 1
                output = ""

 
print("Tuplets and triplets identified: " + str(output_counter))
print("Triplets identified: " + str(output_counter_triplets))                



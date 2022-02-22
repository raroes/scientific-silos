# The impact of research silos in biomedicine

Author: Raul Rodriguez-Esteban

Reference: Rodriguez-Esteban R. The speed of information propagation in the scientific network distorts biomedical research. PeerJ. 2022 Jan 10;10:e12764.
 
Paper Link: https://peerj.com/articles/12764/

Below you can find a brief description of some of the files in this repository.

#### Download data files:

* *download_citations.sh*: download citations from the Open Citation Index
* *download_gene2pubmed.sh*: download the gene2pubmed database
* *download_CTD.sh*: download datasets from the Comparative Toxicogenomics Database (CTD)
* *download_pmid_doi_mapping.sh*: download the PMID-PMC-DOI mappings from EBI
* *download_mesh_tree.sh*: download MeSH tree structure

#### Processing data files:

* *parse_medline_for_mesh.py*: list all MeSH major topic annotations in MEDLINE
* *parse_medline_for_dates.py*: list all MEDLINE PMIDs and their publication dates
* *read_gene_annotations_gene2pubmed.py*: process gene2pubmed MEDLINE gene annotations for human genes
* *read_mesh_annotations.py*: process MeSH annotations from the MEDLINE 2020 baseline
* *parse_CTD.py*: parse files from the CTD to create facts
* *find_co-occurrence.py*: create facts based on annotation co-occurrence
* *filter_earliest_discovered.py*: filter duplicate facts based on date of publication

#### For the CTD and co-occurrence analysis:

* *create_tuplets.py*: create all combinatorially possible pairs of facts
* *shortest_path.py*: compute citation distance by finding the shortest path between two nodes (articles) in the citation network
* *run_model.py*: apply the discovery model to all pairs of facts and the citation distance computed

#### Additional files:

* *map_doi_citations_to_pmid.py*: map citation pairs in DOI format to PMID using the EBI mapping data
* *create_shuffled_network.py*: shuffle nodes in the citation network while maintaining the network topology
* *decimate_citations.py*: randomly delete citations from the citation network

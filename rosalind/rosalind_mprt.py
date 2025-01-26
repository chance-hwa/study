import subprocess
from utils import parse_args, read_fasta

def fetch_uniprot_protein(protein_accession):
    protein_id = protein_accession.split("_")[0]
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.fasta"
    response = subprocess.run(["curl", "-s", url], stdout=subprocess.PIPE)
    output = response.stdout.decode("utf-8").split("\n")

    protein_seq = ""
    for row in output:
        if row.startswith(">"):
            continue
        protein_seq += row

    return protein_seq

def find_n_glycosylation_motif(protein_seq):
    #motif = N{P}[ST]{P}

    n_glycosylation_motif_locations = list()

    for i in range(len(protein_seq) - 4):
        if protein_seq[i] == 'N' and protein_seq[i+1] != 'P' and protein_seq[i+2] in ['S', 'T'] and protein_seq[i+3] != 'P':
            n_glycosylation_motif_locations.append(i+1)
    
    return " ".join(map(str, n_glycosylation_motif_locations))

def main():
    args = parse_args()
    protein_accessions = read_fasta(args.input)

    id2motifs = dict()
    for protein_accession in protein_accessions:
        protein_seq = fetch_uniprot_protein(protein_accession)
        n_glycosylation_motif_locations = find_n_glycosylation_motif(protein_seq)

        if n_glycosylation_motif_locations:
            id2motifs[protein_accession] = n_glycosylation_motif_locations
    
    for protein_accession, n_glycosylation_motif_locations in id2motifs.items():
        print(protein_accession + " ")
        print(n_glycosylation_motif_locations)

if __name__ == "__main__":
    main()


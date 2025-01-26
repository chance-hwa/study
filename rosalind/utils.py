import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file path", required=True)
    return parser.parse_args()

def read_fasta(fasta_file_path):
    sequences = list()

    with open(fasta_file_path) as fasta_file:
        for row in fasta_file:
            row = row.strip()
            sequences.append(row)

    return sequences

def read_fasta_with_id(fasta_file_path):
    id2seq = dict()

    with open(fasta_file_path) as fasta_file:
        for row in fasta_file:
            row = row.strip()
            if row.startswith('>'):
                seq_id = row[1:]
                id2seq[seq_id] = ''
            else:
                id2seq[seq_id] += row

    return id2seq


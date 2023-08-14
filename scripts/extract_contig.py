#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd
from Bio import SeqIO

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-info', metavar='TXT', 
        help='target taxonomy file', required=True)
    parser.add_argument('-i', metavar='FASTA', 
        help='original contig fasta file', required=True)
    parser.add_argument('-o', metavar='FASTA', 
        help='output contig fasta file', required=True)
    argv = vars(parser.parse_args())
    return argv

def extract(info_file, input_file, output_file):
    df = pd.read_csv(info_file, sep = '\t')
    contig_names = df.loc[:,"Contig"].tolist()
    
    taxon_contigs = []
    for rec in SeqIO.parse(input_file, "fasta"):
        if rec.id in contig_names:
            taxon_contigs.append(rec)
    
    SeqIO.write(taxon_contigs, output_file, "fasta-2line")

def main():
    argv = argparse_line()
    extract(argv['info'], argv['i'], argv['o'])

if __name__ == '__main__':
    main()

#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', nargs='+',
        help='different software taxonomy files', required=True)
    parser.add_argument('-o', metavar='PNG',
        help='{taxon}.compare_software.venn.png', required=True)
    argv = vars(parser.parse_args())
    return argv

def compare(input_files, output_file):
    unclassified_family = {}
    for file_name in input_files:
        software = file_name.split('/')[-1].split('.')[1].split('_')[0]
        sample_name = file_name.split('/')[-1].split('.')[0]
        df = pd.read_csv(file_name, sep='\t')
        contig_id = df[df['family_name'].isnull()]['Contig'].apply(lambda x: f"{sample_name}_" + x).tolist()
        if software not in unclassified_family:
            unclassified_family[software] = set(contig_id)
        else:
            unclassified_family[software] |= set(contig_id)
   
    software_labels = list(unclassified_family.keys())
    contig_ids = tuple(unclassified_family[software] for software in software_labels)
    venn = venn3(contig_ids, set_labels=software_labels)
    plt.title("Venn Diagram of Unclassified Family Contigs")
    plt.savefig(output_file)


def main():
    argv = argparse_line()
    compare(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

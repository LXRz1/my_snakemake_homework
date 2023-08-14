#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', 
        help='{sample}.diamond_{taxon}.add_quality.txt', required=True)
    parser.add_argument('-c', metavar='TXT', 
        help='{sample}_{taxon}.compare_software.txt', required=True)
    parser.add_argument('-o', metavar='TXT', 
        help='{sample}.UnclassifiedFamily.txt', required=True)
    argv = vars(parser.parse_args())
    return argv

def extract(input_file, compare_file, output_file):
    raw_df = pd.read_csv(input_file, delimiter='\t')
    compare_df = pd.read_csv(compare_file, delimiter='\t')
    filtered_df = compare_df[
        (compare_df['checkv_quality'].isin(['Complete', 'High-quality'])) & \
        (compare_df.iloc[:, 2:-2].eq('Unclassified_family').all(axis=1))
        ]
    matching_df = raw_df[raw_df['Contig'].isin(filtered_df['Contig'])]
    matching_df.to_csv(output_file, sep='\t', index=False)

def main():
    argv = argparse_line()
    extract(argv['i'], argv['c'], argv['o'])

if __name__ == '__main__':
    main()

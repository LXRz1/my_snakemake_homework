#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--target', metavar='TXT', 
        help='{sample}.{software}_{target_taxon}.txt', required=True)
    parser.add_argument('--checkv', metavar='TSV', 
        help='quality_summary.tsv', required=True)
    parser.add_argument('--output', metavar='TXT',
        help='{sample}.{software}_{target_taxon}.quality_summary.txt', 
        required=True)
    argv = vars(parser.parse_args())
    return argv

def extract(target_file, checkv_file, output_file):
    target_df = pd.read_csv(target_file, sep='\t')
    checkv_df = pd.read_csv(checkv_file, sep='\t')
    checkv_df = checkv_df[['contig_id', 'checkv_quality']]
    merged_df = target_df.merge(checkv_df, left_on="Contig", 
                                right_on="contig_id", how="left")
    merged_df.drop(columns=["contig_id"], inplace=True)
    merged_df.to_csv(output_file, sep='\t', index=False)

def main():
    argv = argparse_line()
    extract(argv['target'], argv['checkv'], argv['output'])

if __name__ == '__main__':
    main()

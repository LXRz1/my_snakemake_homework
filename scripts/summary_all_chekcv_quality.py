#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', nargs='+', 
        help='quality_summary.tsv', required=True)
    parser.add_argument('-o', metavar='TXT', 
        help='AllContigs_chekcv_quality.tsv', required=True)
    argv = vars(parser.parse_args())
    return argv

def process_file(file_path):
    file_name = file_path.split('/')[-2]
    df = pd.read_csv(file_path, delimiter='\t')
    counts = df['checkv_quality'].value_counts().to_dict()
    all_counts = {'Sample':file_name, 'Complete': 0,
                  'High-quality': 0, 'Medium-quality': 0,
                  'Low-quality': 0, 'Not-determined': 0}
    all_counts.update(counts)
    
    return all_counts

def summary(input_file, output_file):

    result_dfs = []

    for file_path in input_file:
        counts = process_file(file_path)
        result_dfs.append(pd.DataFrame(counts, index=[0]))

    result_df = pd.concat(result_dfs, ignore_index=True)
    result_df.to_csv(output_file, sep='\t', index=False)

def main():
    argv = argparse_line()
    summary(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

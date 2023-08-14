#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd
from functools import reduce

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', nargs='+',
        help='different software taxonomy files', required=True)
    parser.add_argument('-o', metavar='TXT',
        help='{sample}_{taxon}.compare_software.txt', required=True)
    argv = vars(parser.parse_args())
    return argv

def count_unique_values(row):
    unique_values = set(row.values)
    return len(unique_values)

def compare(input_files, output_file):
    data_frames_list = []
    softwares = []
    contig_quality_dict = {}
    for file_name in input_files:
        software = file_name.split('/')[-1].split('.')[1].split('_')[0]
        softwares.append(software)
        df = pd.read_csv(file_name, sep='\t')
        df = df.sort_values(by='Contig')
        df = df.groupby('Contig').first().reset_index()
        if software == 'diamond':
            for index, row in df.iterrows():
                contig = row["Contig"]
                quality = row["checkv_quality"]
                contig_quality_dict[contig] = quality
        df['family_name'].fillna('Unclassified_family', inplace=True)
        df = df[['Contig', 'family_name']]
        df.rename(columns={'family_name':software}, inplace=True)
        data_frames_list.append(df)
    
    merge_df = reduce(lambda x, y: pd.merge(x, y, on='Contig', how='outer'),
                      data_frames_list)
    merge_df.insert(1, "checkv_quality",
                    merge_df["Contig"].map(contig_quality_dict))
    merge_df.set_index('Contig', inplace=True)
    merge_df.fillna('Unclassified_family', inplace=True)
    merge_df['inconsistent_number'] = merge_df[softwares].apply(
        count_unique_values, axis=1)
    merge_df.to_csv(output_file, sep='\t')

def main():
    argv = argparse_line()
    compare(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

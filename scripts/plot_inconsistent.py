#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', nargs='+', 
        help='{sample}_{taxon}.compare_software.txt', required=True)
    parser.add_argument('-o', metavar='PNG', 
        help='{taxon}.compare_software.inconsistent.png', required=True)
    argv = vars(parser.parse_args())
    return argv

def plot_hist(input_files, output_file):
    all_data = pd.DataFrame()
    for file_name in input_files:
        data = pd.read_csv(file_name, delimiter='\t')
        all_columns = data.columns.tolist()
        software = all_columns[2:-1]
        all_data = pd.concat([all_data, data])

    inconsistent_number_counts = \
            all_data['inconsistent_number'].value_counts()

    inconsistent_number_counts = inconsistent_number_counts.sort_index()

    plt.bar(inconsistent_number_counts.index, 
            inconsistent_number_counts.values)

    plt.xlabel('Inconsistent number')
    plt.ylabel('Contig number')
    plt.xticks(list(inconsistent_number_counts.index))
    for index, value in enumerate(inconsistent_number_counts.values):
        plt.text(inconsistent_number_counts.index[index], 
                 value + 1, str(value), ha='center', va='bottom')
    plt.title(' vs '.join(software))
    plt.savefig(output_file)

def main():
    argv = argparse_line()
    plot_hist(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

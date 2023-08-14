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
        help='{sample}.UnclassifiedFamily.txt', required=True)
    parser.add_argument('-o', metavar='txt', 
        help='AllSoftware.UnclassifiedFamilyContig.txt', required=True)
    argv = vars(parser.parse_args())
    return argv

def summary(input_files, output_file):
    result_dfs = []
    for file_name in input_files:
        df = pd.read_csv(file_name, delimiter='\t')
        if len(df) > 0:
            sample_name = file_name.split('/')[-1].split('.')[0]
            df.insert(0, 'Sample', sample_name)
            result_dfs.append(df)

    result_df = pd.concat(result_dfs, ignore_index=True)
    result_df.to_csv(output_file, sep='\t', index=False)

def main():
    argv = argparse_line()
    summary(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

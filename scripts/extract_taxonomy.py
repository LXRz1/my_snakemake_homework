#! /usr/bin/env python3

import sys
import argparse, textwrap
import pandas as pd

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', 
        help='add taxonomy name file', required=True)
    parser.add_argument('-o', metavar='TXT', 
        help='output file', required=True)
    parser.add_argument('-rank', metavar='STRING', 
        help='target rank', required=True)
    parser.add_argument('-taxid', metavar='STRING', 
        help='target taxid', required=True)
    parser.add_argument('-vmr', metavar='XLSX', 
        help='VMR_MSL38_v1.xlsx', required=True)
    argv = vars(parser.parse_args())
    return argv

def extract_target_taxon(input_file, output_file, taxon_rank, 
                         taxon_id, vmr_file):
    
    taxon_df = pd.read_csv(input_file, sep='\t', dtype=object)  
    filtered = taxon_df[taxon_df[taxon_rank] == taxon_id].copy()
    filtered['length'] = \
        filtered['Contig'].str.extract(r'length_(\d+)_cov')
    filtered['coverage'] = \
        filtered['Contig'].str.extract(r'cov_(\d+\.\d+)')

    vmr_df = pd.read_excel(vmr_file)
    vmr_df.dropna(subset=['Family'], inplace=True)
    family_mapping = vmr_df.drop_duplicates(subset='Family')\
                          .set_index('Family')[['Realm', 'Kingdom']].to_dict()  
    filtered['Realm'] = \
        filtered['family_name'].map(family_mapping['Realm'])
    filtered['Kingdom'] = \
        filtered['family_name'].map(family_mapping['Kingdom'])
    filtered.to_csv(output_file, sep='\t', index=False)

def main():
    argv = argparse_line()
    extract_target_taxon(argv['i'], argv['o'], 
                         argv['rank'], argv['taxid'],
                         argv['vmr'])

if __name__ == '__main__':
    main()

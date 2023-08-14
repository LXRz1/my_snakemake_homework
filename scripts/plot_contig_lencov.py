#! /usr/bin/env python3

import sys
import argparse, textwrap
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.lines import Line2D

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', 
        help='extract target taxonomy info file', required=True)
    parser.add_argument('-o', metavar='PNG', 
        help='output png file', required=True)
    parser.add_argument('-vmr', metavar='XLSX',
        help='VMR_MSL38_v1.xlsx', required=True)
    argv = vars(parser.parse_args())
    return argv

def plot_scatter(input_file, output_file, vmr_file):
    vmr_df = pd.read_excel(vmr_file)
    vmr_df.dropna(subset=['Realm'], inplace=True)
    vmr_realms = vmr_df['Realm'].unique()
    num_realms = len(vmr_realms)
    realm_colors = cm.Set3(range(num_realms))
    realm_color_dict = {realm: color for realm,
                        color in zip(vmr_realms, realm_colors)}

    df = pd.read_csv(input_file, sep='\t')
    df['family_name'] = df['family_name'].fillna("Family unknown")

    marker_shapes = itertools.cycle(
        ('o', 'v', '^', '<', '>', '8', 's',
         'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'))
    family_color_dict = {}
    family_shape_dict = {}
    for index, row in df.iterrows():
        realm = row['Realm']
        family_name = row['family_name']
        if realm in realm_color_dict:
            family_color_dict[family_name] = realm_color_dict[realm]
        else:
            if family_name == 'Family unknown':
                family_color_dict[family_name] = 'grey'
            else:
                family_color_dict[family_name] = 'black'
        if family_name not in family_shape_dict:
            family_shape_dict[family_name] = next(marker_shapes)

    plt.figure(figsize=(10, 10))

    for _, row in df.iterrows():
        family_name = row['family_name']
        marker = family_shape_dict[family_name]
        color = family_color_dict[family_name]
        plt.scatter(row['length'], row['coverage'],
                    c=np.array([color]), marker=marker,
                    s=50)

    legend_elements = [plt.Line2D([0], [0],
                       marker=family_shape_dict[family],
                       color=family_color_dict[family],
                       markerfacecolor=family_color_dict[family],
                       label=family)
                       for family in df['family_name'].unique()]
    legend_elements.sort(key=lambda x: cm.colors.rgb2hex(x.get_color()))

    plt.legend(handles=legend_elements, title='Virus Family',
               loc='upper right')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Contig Length(log scale)')
    plt.ylabel('Coverage(log scale)')
    plt.title('Scatter Plot of Contig Length vs Coverage')
    plt.savefig(output_file)

def main():
    argv = argparse_line()
    plot_scatter(argv['i'], argv['o'], argv['vmr'])

if __name__ == '__main__':
    main()

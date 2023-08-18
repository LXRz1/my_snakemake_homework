#! /usr/bin/env python3

import sys
import argparse, textwrap
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT', nargs='+', 
        help='{sample}.{software}_{taxon}.add_quality.txt', required=True)
    parser.add_argument('-o', metavar='PNG', 
        help='{software}_{taxon}.FamilyQualityNum.heatmap.png', required=True)
    argv = vars(parser.parse_args())
    return argv

def summary(input_files, output_file):
    data_frames_list = []
    for file_name in input_files:
        df = pd.read_csv(file_name, sep='\t')
        data_frames_list.append(df)
    
    combined_df = pd.concat(data_frames_list, ignore_index=True)
    combined_df['family_name'].fillna('Unclassified_family', inplace=True)

    checkv_quality_categories = ['Complete', 'High-quality', 
                                 'Medium-quality', 'Low-quality', 
                                 'Not-determined']
    combined_df['checkv_quality'] = pd.Categorical(
            combined_df['checkv_quality'], 
            categories=checkv_quality_categories, ordered=True)

    family_checkv_count = combined_df.groupby(
            ['family_name', 'checkv_quality']).size().reset_index(
                    name='count')
    df = family_checkv_count.pivot(index='family_name', 
                                   columns='checkv_quality', 
                                   values='count').fillna(0)
    
    df = np.log(df)
    df = df.replace([np.inf, -np.inf], 0)

    plt.figure(figsize=(40, 30))
    ax = sns.heatmap(df, 
                     cmap=sns.color_palette("rocket_r", 20),
                     linewidths=0.05,
                     linecolor='white',
                     cbar_kws={'label': 'Contigs Number(log scale)'})
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=30)
    ax.figure.axes[-1].yaxis.label.set_size(30)
    ax.set(xlabel="", ylabel="")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', 
                       fontsize=30)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=30)
    ax.set_title('Distribution of Contig counts at the Family Rank', 
                 fontsize=30)
    plt.yticks(rotation=0)
    plt.savefig(output_file)

def main():
    argv = argparse_line()
    summary(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

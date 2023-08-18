#! /usr/bin/env python3

import sys
import argparse
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def argparse_line():
    parser = argparse.ArgumentParser(description='',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--target', metavar='TXT', nargs='+',
        help='{sample}.{software}_{target_taxon}.txt', required=True)
    parser.add_argument('--output', metavar='PNG',
        help='{software}_{target_taxon}.ContigNumber.png', required=True)
    argv = vars(parser.parse_args())
    return argv

def process_file(file_path):
    df = pd.read_csv(file_path, delimiter='\t')
    df['family_name'].fillna('Unclassified_family', inplace=True)
    family_counts = df['family_name'].value_counts()

    return family_counts

def plot(target_files, output):
    all_samples = {}
    for file_name in target_files:
        sample_name = file_name.split('/')[-1].split('.')[0]
        family_counts = process_file(file_name)
        all_samples[sample_name] = family_counts

    df = pd.DataFrame(all_samples).fillna(0)

    df = np.log(df)
    df = df.replace([np.inf, -np.inf], 0)

    plt.figure(figsize=(70, 30))
    ax = sns.heatmap(df,
                     cmap=sns.color_palette("rocket_r", 20),
                     linewidths=0.05,
                     linecolor='white',
                     cbar_kws={'label': 'Contigs Number(log scale)'})
    
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=30)
    ax.figure.axes[-1].yaxis.label.set_size(30)

    ax.set(xlabel="", ylabel="")
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=15, 
                       rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=30)
    ax.set_title('Distribution of Contig counts at the Family Rank', 
                 fontsize=30)
    plt.yticks(rotation=0)
    plt.savefig(output)

def main():
    argv = argparse_line()
    plot(argv['target'], argv['output'])

if __name__ == '__main__':
    main()

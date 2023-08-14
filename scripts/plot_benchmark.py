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
        help='*.benchmark.txt', required=True)
    parser.add_argument('-o', metavar='PNG', 
        help='benchmark.png', required=True)
    argv = vars(parser.parse_args())
    return argv

def plot_hist(input_files, output_file):
    run_time = {}
    memory = {}
    cpu_load = {}
    for file_path in input_files:
        software = file_path.split('/')[2]
        df = pd.read_csv(file_path, sep='\t')
        run_time_minutes = df['s'].mean()/60
        memory_gb = df['max_uss'].mean()/1024
        mean_cpu = df['mean_load'].mean()
        if software not in run_time:
            run_time[software] = []
            run_time[software].append(run_time_minutes)
        else:
            run_time[software].append(run_time_minutes)
        if software not in memory:
            memory[software] = []
            memory[software].append(memory_gb)
        else:
            memory[software].append(memory_gb)
        if software not in cpu_load:
            cpu_load[software] = []
            cpu_load[software].append(mean_cpu)
        else:
            cpu_load[software].append(mean_cpu)

    labels = list(run_time.keys())
    run_time_data = [run_time[software] for software in labels]
    memory_data = [memory[software] for software in labels]
    cpu_load_data = [cpu_load[software] for software in labels]

    #################################################################
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 15))
    bplot1 = ax1.boxplot(run_time_data,
                         labels=labels, vert=True, patch_artist=True)
    ax1.set_ylabel('minutes')
    ax1.set_yscale('log')
    ax1.set_title('Time')
    #################################################################
    bplot2 = ax2.boxplot(memory_data,
                         labels=labels, vert=True, patch_artist=True)
    ax2.set_ylabel('Gigabytes')
    ax2.set_yscale('log')
    ax2.set_title('Memory')
    #################################################################
    bplot3 = ax3.boxplot(cpu_load_data,
                         labels=labels, vert=True, patch_artist=True)
    ax3.set_ylabel('Avg # Cpus Utilized')
    ax3.set_title('CPU Load')
    #################################################################
    # fill with colors
    colors = ['pink', 'lightblue', 'lightgreen']
    for bplot in (bplot1, bplot2, bplot3):
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
    
    # adding horizontal grid lines
    for ax in [ax1, ax2, ax3]:
        ax.yaxis.grid(True)
    #################################################################
    plt.subplots_adjust(hspace=0.5)
    plt.savefig(output_file)

def main():
    argv = argparse_line()
    plot_hist(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

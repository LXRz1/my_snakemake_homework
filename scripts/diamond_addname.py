#! /usr/bin/env python3

import sys
import argparse, textwrap
import re

def argparse_line():
    parser = argparse.ArgumentParser(description='', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TSV', 
        help='*_contigs_taxonomy_info.tsv', required=True)
    parser.add_argument('-o', metavar='TSV', 
        help='*_contigs_taxonomy_info_addnames.tsv', required=True)
    parser.add_argument('-dmp', metavar='TXT', 
        help='NCBI names.dmp', required=True)
    argv = vars(parser.parse_args())
    return argv

def add_name(input_file, output_file, dmp_file):
    names = {}
    with open(dmp_file, 'r') as handle:
        for line in handle:
            newline = line.split('\t|\t')
            if "scientific name" in newline[3]:
                names[newline[0]] = newline[1]

    with open(output_file, 'w') as output:
        output.write('Contig\tDiamond Hit TaxID\t'
                     'LCA\tLCA_name\tsuperkingdom\tsuperkingdom_name\t'
                     'phylum\tphylum_name\tclass\tclass_name\t'
                     'order\torder_name\tfamily\tfamily_name\t'
                     'subfamily\tsubfamily_name\tgenus\tgenus_name\n')
        with open(input_file, 'r') as handle:
            for line in handle:
                if re.match('Contig', line):
                    continue
                newline = line.strip().split('\t')
                outputline = newline[:2]
                for taxid in newline[2:]:
                    outputline.append(taxid)
                    outputline.append(names.get(taxid, 'N/A'))
                output.write('{0}\n'.format('\t'.join(outputline)))

def main():
    argv = argparse_line()
    add_name(argv['i'], argv['o'], argv['dmp'])

if __name__ == '__main__':
    main()

#! /usr/bin/env python3

import sys
import argparse, textwrap
#import taxoniq
import re
from Bio import Entrez
from retrying import retry

Entrez.email = '2812743l@alpha2.cvr.gla.ac.uk'

def argparse_line():
    parser = argparse.ArgumentParser(description='',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', metavar='TXT',
        help='blast format 6 file', required=True)
    parser.add_argument('-o', metavar='TXT',
        help='add taxid and taxonomy name file', required=True)
    argv = vars(parser.parse_args())
    return argv

def taxoniq_get_taxid(accession_id):
    info = {}
    try:
        t1 = taxoniq.Taxon(accession_id=accession_id)
        for i in t1.lineage:
            rank = i.rank.name
            taxid = i.tax_id
            scientific_name = i.scientific_name
            info[rank] = {}
            info[rank]['taxid'] = str(taxid)
            info[rank]['name'] = scientific_name
    except KeyError:
        return info

    return info

@retry(stop_max_attempt_number=10)
def entrez_get_taxid(accession_id):
    info = {}
    handle = Entrez.efetch(db='Nucleotide', id=accession_id,
            rettype="gb", retmode="text")
    pattern = r'/db_xref="taxon:(\d+)"'
    for i in handle:
        match = re.search(pattern, i)
        if match:
            taxid = match.group(1)
            break
    if taxid:
        handle = Entrez.efetch(db = "Taxonomy", id = taxid)
        records = Entrez.read(handle)
        if 'LineageEx' in records[0]:
            for rank in records[0]['LineageEx']:
                info[rank['Rank']] = {}
                info[rank['Rank']]['taxid'] = rank['TaxId']
                info[rank['Rank']]['name'] = rank['ScientificName']
        else:
            return info
    else:
        return info

    return info

def add_name(input_file, output_file):
    total_info = {}
    output = open(output_file, 'w')
    output.write('Contig\tAccessonNumber\t'
                 'superkingdom\tsuperkingdom_name\t'
                 'phylum\tphylum_name\t'
                 'class\tclass_name\t'
                 'order\torder_name\t'
                 'family\tfamily_name\t'
                 'subfamily\tsubfamily_name\t'
                 'genus\tgenus_name\n')
    all_rank = ['superkingdom', 'phylum', 'class', 'order',
                'family', 'subfamily', 'genus']
    with open(input_file, 'r') as handle:
        for line in handle:
            newline = line.strip().split('\t')
            contig_id = newline[0]
            accession_id = newline[1]
            output_list = [contig_id, accession_id]
            if accession_id not in total_info:
                tax_info = entrez_get_taxid(accession_id)
                total_info[accession_id] = tax_info
            else:
                tax_info = total_info[accession_id]
            for rank in all_rank:
                if rank in tax_info:
                    taxid = tax_info[rank]['taxid']
                    name = tax_info[rank]['name']
                else:
                    taxid = 'N/A'
                    name = 'N/A'
                output_list.append(taxid)
                output_list.append(name)
            output.write('{0}\n'.format('\t'.join(output_list)))
    output.close()

def main():
    argv = argparse_line()
    add_name(argv['i'], argv['o'])

if __name__ == '__main__':
    main()

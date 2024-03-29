# Rodent Samples Virus Classification and Comparison
A collection of scripts and pipelines is used to process Spades-assembled contigs and Diamond classification results from rodent samples collected in Sierra Leone. In this case, the pipeline was used to identify all virus sequences present in the samples.

## Dependencies
### Software
* [snakemake](https://github.com/snakemake/snakemake) v7.26.0
* [hs-blastn](https://github.com/chenying2016/queries/tree/master/hs-blastn-src) v2.0.0
* [blastn](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) v2.14.0+
* [checkv](https://bitbucket.org/berkeleylab/checkv/src/master/) v1.0.1
### R package
* [taxonomizr](https://cran.r-project.org/web/packages/taxonomizr/index.html)

### Database
#### CheckV Database
If you install CheckV using conda or pip you will need to download the database:

`checkv download_database ./`

#### NT Database
Download nt fasta:
* [nt fasta](https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz)

And build blastn index(hs-blastn does not require building an index beforehand. Only need to provide the FASTA sequences):

`gunzip nt.gz`

`makeblastdb -in nt -dbtype nucl`

#### SQLite Database
If you install the taxonomizr R package, you need to prepare an SQLite database for mapping accession to taxonomy ID:

`library(taxonomizr)`

`prepareDatabase('accessionTaxa.sql')`

#### Other files
##### NCBI taxonomy
* [taxdump.tar.gz](https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz)

Unzip: `tar zxvf taxdump.tar.gz`
And we need the `names.dmp` file.

##### ICTV Virus Metadata Resource spreadsheet
* [VMR_MSL38_v1.xlsx](https://ictv.global/vmr/current)

## Usage
This pipeline does not involve additional manual steps, such as contig assembly and Diamond alignment.You need to complete sequence assembly and Diamond alignment in advance. These are the required input files for the pipeline. The file format for Contig sequences is: `{sample_name}_contigs.fasta`, and the file format for Diamond alignment results is: `{sample_name}_contigs_taxonomy_info.tsv`.

Additionally, you need to configure the `config.yaml` file by replace the absolute paths for the required software or databases.

These are the paths that must be modified in the `config.yaml`：

| Path                  | Description                                |
|-----------------------|--------------------------------------------|
| `contigs_path`        | Contigs for all samples                    |
| `diamond_path`        | Diamond alignment result for all samples   |
| `accession2taxadb`    | accessionTaxa.sql                          |
| `names_dmp`           | names.dmp                                  |
| `vmr_file`            | VMR_MSL38_v1.xlsx                          |
| `scripts`             | absolute paths to the `scripts`            |
| `hsblastn`            |                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`path` | absolute paths to the hs-blastn            |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`index`| absolute paths to the nt fasta             |
| `megablastn`          |                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`path` | absolute paths to the blastn               |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`index`| absolute paths to the nt fasta             |
| `checkv`              |                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`path` | absolute paths to the checkv               |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`database`| absolute paths to the CheckV Database   |

When you have prepared the input files and the `config.yaml`, execute the following command to run the pipeline:

`snakemake --configfile config.yaml --snakefile Snakefile --cores {threads}`

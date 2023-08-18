# Rodent Sample Virus Classification and Comparison
A collection of scripts and pipelines is used to process Spades-assembled contigs and Diamond classification results from rodent samples collected in Sierra Leone. In this case, the pipeline was used to identify all virus sequences present in the samples.

## Dependencies
### Software
* [snakemake](https://github.com/snakemake/snakemake) v7.26.0
* [hs-blastn](https://github.com/chenying2016/queries/tree/master/hs-blastn-src) v2.0.0
* [blastn](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) v2.14.0+
* [checkv](https://bitbucket.org/berkeleylab/checkv/src/master/) v1.0.1
### R package
* [taxonomizr](https://cran.r-project.org/web/packages/taxonomizr/index.html)

## Database
### CheckV Database
If you install CheckV using conda or pip you will need to download the database:

`checkv download_database ./`

### NT Database
Download nt fasta:
* [nt fasta](https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz)

And build blastn index:

`gunzip nt.gz`

`makeblastdb -in nt -dbtype nucl`

### SQLite Database
If you install the taxonomizr R package, you need to prepare an SQLite database for mapping accession to taxonomy ID:

`library(taxonomizr)`

`prepareDatabase('accessionTaxa.sql')`

### Other files
Download:

* [taxdump.tar.gz](https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz)

Unzip it:

`tar zxvf taxdump.tar.gz`

And we need the `names.dmp` file.


# Rodent Sample Virus Classification and Comparison
A collection of scripts and pipelines is used to process Spades-assembled contigs and Diamond classification results from rodent samples collected in Sierra Leone. In this case, the pipeline was used to identify all virus sequences present in the samples.

### Dependencies
#### Software
* [snakemake](https://github.com/snakemake/snakemake)
* [hs-blastn](https://github.com/chenying2016/queries/tree/master/hs-blastn-src)
* [blastn](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
* [checkv](https://bitbucket.org/berkeleylab/checkv/src/master/)

#### Database
##### CheckV Database
If you install CheckV using conda or pip you will need to download the database:

`checkv download_database ./`

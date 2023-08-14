library(argparse)
library(taxonomizr)

parser <- argparse::ArgumentParser(description = "Add Taxonomy for blast6fmt")

parser$add_argument("-i", "--input", dest = "input_file", 
                    help = "blast6fmt file", type = "character")

parser$add_argument("-o", "--output", dest = "output_file", 
                    help = "add taxonnomy file", type = "character")

parser$add_argument("-db", "--database", dest = "database_file", 
                    help = "accessionTaxa.sql", type = "character")

args <- parser$parse_args()

if (is.null(args$input_file) || is.null(args$output_file) ||is.null(args$database_file)) {
  stop("Please use the -h parameter to see the help.")
}

my_dataframe <- data.frame(Contig=character(0),
                           AccessonNumber=character(0),
                           superkingdom=character(0),
                           superkingdom_name=character(0),
                           phylum=character(0),
                           phylum_name=character(0),
                           class=character(0),
                           class_name=character(0),
                           order=character(0),
                           order_name=character(0),
                           family=character(0),
                           family_name=character(0),
                           subfamily=character(0),
                           subfamily_name=character(0),
                           genus=character(0),
                           genus_name=character(0)
)

if (file.info(args$input_file)$size != 0){
  input_data <- read.csv(args$input_file, sep="\t", header=FALSE)
  database <- args$database_file
  
  for (i in 1:nrow(input_data)) {
      contig_name <- input_data[i, 1]
      accession <- input_data[i, 2]
      taxid <- accessionToTaxa(accession, database)
      lineage <- getTaxonomy(taxid, database, 
                             desiredTaxa = c("superkingdom", "phylum", "class", 
                                             "order", "family", "subfamily", 
                                             "genus"))
      lineage <- as.data.frame(lineage)
      ##################################################
      superkingdom_name <- lineage$superkingdom
      superkingdom <- getId(superkingdom_name, database)
      ##################################################
      phylum_name <- lineage$phylum
      phylum <- getId(phylum_name, database)
      ##################################################
      class_name <- lineage$class
      class <- getId(class_name, database)
      ##################################################
      order_name <- lineage$order
      order <- getId(order_name, database)
      ##################################################
      family_name <- lineage$family
      family <- getId(family_name, database)
      ##################################################
      subfamily_name <- lineage$subfamily
      subfamily <- getId(subfamily_name, database)
      ##################################################
      genus_name <- lineage$genus
      genus <- getId(genus_name, database)
      row <- data.frame(Contig = contig_name,
                        AccessonNumber = accession,
                        superkingdom = superkingdom,
                        superkingdom_name = superkingdom_name,
                        phylum = phylum,
                        phylum_name = phylum_name,
                        class = class,
                        class_name = class_name,
                        order = order,
                        order_name = order_name,
                        family = family,
                        family_name = family_name,
                        subfamily = subfamily,
                        subfamily_name = subfamily_name,
                        genus = genus,
                        genus_name = genus_name
      )
      my_dataframe <- rbind(my_dataframe, row)
  }
  my_dataframe[is.na(my_dataframe)] <- "N/A"
  write.table(my_dataframe, file = args$output_file, 
              sep='\t', quote = FALSE, row.names = FALSE)
} else {
    write.table(my_dataframe, file = args$output_file,
                sep='\t', quote = FALSE, row.names = FALSE)
}

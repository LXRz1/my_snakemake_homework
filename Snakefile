import glob

configfile: "/home3/2812743l/share3/config.yaml"

contigs_path = config['contigs_path']
samples = []
for path in glob.glob(f'{contigs_path}/*_contigs.fasta'):
	samples.append(path.split('/')[-1].split('_contigs.fasta')[0])

softwares = config['software']

rule all:
    input: # all contigs run checkv
           expand("02.AllCheckv/{sample}/quality_summary.tsv",
                  sample=samples),
           "02.AllCheckv/AllContigs_chekcv_quality.tsv",

           # all diamond alignment add taxonomy
           expand("04.AllDiamondAddTaxon/{sample}.diamond_addtaxonomy.txt",
                  sample=samples),
           
           # all diamond extract target taxonomy
           expand("05.AllDiamondExtractTaxon/{taxon}/" \
                  "{sample}.diamond_{taxon}.txt", \
                  sample=samples, taxon=config["target_taxons"]),
           
           # plot diamond families contig number heatmap
           expand("05.AllDiamondExtractTaxon/" \
                  "diamond_{taxon}.FamilyContigNum.heatmap.pdf", \
                  taxon=config["target_taxons"]),
           
           # all diamond extract target taxonomy add checkv quality
           expand("06.AllDiamondExtractTaxonAddQuality/{taxon}/" \
                  "{sample}.diamond_{taxon}.add_quality.txt", \
                  sample=samples, software=softwares,
                  taxon=config["target_taxons"]),
    
           # plot diamond families contig quality number heatmap
           expand("06.AllDiamondExtractTaxonAddQuality/" \
                  "diamond_{taxon}.FamilyQualityNum.heatmap.pdf", \
                  taxon=config["target_taxons"]),
           
           # all diamond extract target taxonomy contig
           expand("07.AllDiamondExtractContig/" \
                  "{taxon}/{sample}.diamond_{taxon}.fasta", \
                  sample=samples, taxon=config["target_taxons"]),
        
           # all diamond plot target taxonomy contig length coverage
           expand("05.AllDiamondExtractTaxon/{taxon}/" \
                  "{sample}.diamond_{taxon}.ContigLenCov.scatter.png", \
                  sample=samples, taxon=config["target_taxons"]),
          
           # all diamond extract target taxonomy contig align
           expand("08.AllDiamondExtractContigAlign/{taxon}/{software}/" \
                  "{sample}.{software}_{taxon}.txt", \
                  sample=samples, software=softwares,
                  taxon=config["target_taxons"]),
           
           # plot different alignment softwares benchmark
           "benchmarks/benchmarks.pdf",
         
           # different alignment softwares add taxonomy
           expand("09.AllDiamondExtractContigAlignAddTaxon/{taxon}/" \
                  "{software}/{sample}.{software}_addtaxonomy.txt", \
                  sample=samples, software=softwares,
                  taxon=config["target_taxons"]),

           # compare different software famliy alignment consistent
           expand("10.CompareAlignmentSoftware/" \
                  "{taxon}/{sample}_{taxon}.compare_software.txt", \
                  sample=samples, taxon=config["target_taxons"]),
           
           # plot different software unclassified family contig number venn
           expand("10.CompareAlignmentSoftware/" \
                  "Viruses.compare_software.UnclassifiedFamily.pdf", \
                  taxon=config["target_taxons"]),
           
           # extract all software unclassified family contig
           expand("11.CompareExtractUnclassified/{taxon}/" \
                  "{sample}.UnclassifiedFamily.txt", \
                  sample=samples, taxon=config["target_taxons"]),
           
           # summary all samples unclassified family contig
           "11.CompareExtractUnclassified/" \
           "AllSoftware.UnclassifiedFamilyContig.txt"

rule checkv:
    input:   lambda wildcards: \
             f"{config['contigs_path']}/{wildcards.sample}_contigs.fasta"
    output:  "02.AllCheckv/{sample}/quality_summary.tsv"
    params:  checkv = config['checkv']['path'],
             database = config['checkv']['database']
    log:     stdout = 'logs/checkv/{sample}.checkv.stdout',
             stderr = 'logs/checkv/{sample}.checkv.stderr'
    threads: config['checkv']['threads']
    shell:   "{params.checkv} end_to_end "
             "-d {params.database} "
             "{input} "
             "02.AllCheckv/{wildcards.sample} "
             "-t {threads} "
             "1> {log.stdout} "
             "2> {log.stderr}"

rule summary_all_chekcv_quality:
    input:  expand("02.AllCheckv/{sample}/quality_summary.tsv", \
            sample=samples)
    output: "02.AllCheckv/AllContigs_chekcv_quality.tsv"
    params: scripts = config['scripts']
    log:    stdout = 'logs/checkv/summary_all_chekcv_quality.stdout',
            stderr = 'logs/checkv/summary_all_chekcv_quality.stderr' 
    shell:  "python3 {params.scripts}/summary_all_chekcv_quality.py "
            "-i {input} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_add_taxonomy_name:
    input:  "03.AllDiamond/{sample}_contigs_taxonomy_info.tsv"
    output: "04.AllDiamondAddTaxon/{sample}.diamond_addtaxonomy.txt"
    params: names_dmp = config["names_dmp"],
            scripts = config['scripts'],
            accession2taxadb = config['accession2taxadb']
    log:    stdout = 'logs/diamond_add_taxonomy_name/{sample}.stdout',
            stderr = 'logs/diamond_add_taxonomy_name/{sample}.stderr'
    shell:
            "python3 {params.scripts}/diamond_addname.py "
            "-i {input} -o {output} -dmp {params.names_dmp}  "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_extract_taxon:
    input:  "04.AllDiamondAddTaxon/{sample}.diamond_addtaxonomy.txt"
    output: "05.AllDiamondExtractTaxon/{taxon}/{sample}.diamond_{taxon}.txt"
    params: scripts = config['scripts'],
            vmr_file = config['vmr_file'],
            rank = lambda a: config['target_taxons'][a.taxon]['rank'],
            taxid = lambda a: config['target_taxons'][a.taxon]['taxid']
    log:    stdout = 'logs/diamond_extract_taxon/{taxon}/{sample}.stdout',
            stderr = 'logs/diamond_extract_taxon/{taxon}/{sample}.stderr'
    shell:  "python3 {params.scripts}/extract_taxonomy.py "
            "-i {input} -o {output} "
            "-rank {params.rank} "
            "-taxid {params.taxid} "
            "-vmr {params.vmr_file} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_plot_lencov_scatter:
    input:  "05.AllDiamondExtractTaxon/{taxon}/{sample}.diamond_{taxon}.txt"
    output: "05.AllDiamondExtractTaxon/{taxon}/" \
            "{sample}.diamond_{taxon}.ContigLenCov.scatter.png"
    params: scripts = config['scripts'],
            vmr_file = config['vmr_file']
    log:    stdout = 'logs/diamond_plot_lencov_scatter/' \
                     '{taxon}/{sample}.stdout',
            stderr = 'logs/diamond_plot_lencov_scatter/' \ 
                     '{taxon}/{sample}.stderr'
    shell:  "python3 {params.scripts}/plot_contig_lencov.py "
            "-i {input} -o {output} -vmr {params.vmr_file} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_extract_taxon_contig:
    input:  info = "05.AllDiamondExtractTaxon/" \
                   "{taxon}/{sample}.diamond_{taxon}.txt",
            fasta = lambda wildcards: \
            f"{config['contigs_path']}/{wildcards.sample}_contigs.fasta"
    output: "07.AllDiamondExtractContig/" \
            "{taxon}/{sample}.diamond_{taxon}.fasta"
    params: scripts = config['scripts']
    log:    stdout = 'logs/diamond_extract_taxon_contig/' \
                     '{taxon}/{sample}.stdout',
            stderr = 'logs/diamond_extract_taxon_contig/' \ 
                     '{taxon}/{sample}.stderr'
    shell:  "python3 {params.scripts}/extract_contig.py "
            "-i {input.fasta} -o {output} -info {input.info} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_extract_taxon_contig_align:
    input:   "07.AllDiamondExtractContig/" \
             "{taxon}/{sample}.diamond_{taxon}.fasta"
    output:  "08.AllDiamondExtractContigAlign/{taxon}/{software}/" \
             "{sample}.{software}_{taxon}.txt"
    params:  path = lambda a: config['software'][a.software]['path'],
             index = lambda a: config['software'][a.software]['index'],
             max_hsps = lambda a: config['software'][a.software]['max_hsps'],
             max_target_seqs = \
                 lambda a: config['software'][a.software]['max_target_seqs'],
             evalue = lambda a: config['software'][a.software]['evalue']
    benchmark: "benchmarks/{taxon}/{software}/" \
               "{sample}.{software}.benchmark.txt"
    threads: lambda a: config['software'][a.software]['threads']
    log:     stdout = "logs/diamond_extract_taxon_contig_align/" \
                      "{taxon}/{software}/{sample}.{software}.stdout",
             stderr = "logs/diamond_extract_taxon_contig_align/" \
                      "{taxon}/{software}/{sample}.{software}.stderr"
    run:
        if wildcards.software == 'megablastn':
            shell("{params.path} "
                  "-query {input} "
                  "-db {params.index} "
                  "-out {output} "
                  "-outfmt 6 "
                  "-max_hsps {params.max_hsps} "
                  "-max_target_seqs {params.max_target_seqs} "
                  "-evalue {params.evalue} "
                  "-num_threads {threads} "
                  "1> {log.stdout} "
                  "2> {log.stderr}")
        elif wildcards.software == 'hsblastn':
            shell("{params.path} "
                  "-max_hsps {params.max_hsps} "
                  "-max_target_seqs {params.max_target_seqs} "
                  "-evalue {params.evalue} "
                  "-num_threads {threads} "
                  "-outfmt 6 "
                  "-db_dir 08.AllDiamondExtractContigAlign/"
                  "{wildcards.taxon}/{wildcards.software}/"
                  "{wildcards.sample}_hsblastndb "
                  "-out {output} "
                  "{input} {params.index} "
                  "1> {log.stdout} "
                  "2> {log.stderr}")
        elif wildcards.software == 'usearch':
            shell("{params.path} -ublast {input} "
                  "-db {params.index} "
                  "-strand both "
                  "-maxaccepts {params.max_hsps} "
                  "-evalue {params.evalue} "
                  "-blast6out {output} "
                  "-threads {threads} "
                  "1> {log.stdout} "
                  "2> {log.stderr}")

rule plot_benchmark:
    input:  expand("benchmarks/{taxon}/{software}/" \
                   "{sample}.{software}.benchmark.txt", \
                   sample=samples, software=softwares, \
                   taxon=config["target_taxons"])
    output: "benchmarks/benchmarks.pdf"
    params: scripts = config['scripts']
    log:    stdout = 'logs/plot_benchmark/plot_benchmark.stdout',
            stderr = 'logs/plot_benchmark/plot_benchmark.stderr'
    shell:  "python3 {params.scripts}/plot_benchmark.py "
            "-i {input} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule align_add_taxonomy_name:
    input:  "08.AllDiamondExtractContigAlign/{taxon}/{software}/" \
             "{sample}.{software}_{taxon}.txt"
    output: "09.AllDiamondExtractContigAlignAddTaxon/{taxon}/{software}/" \
            "{sample}.{software}_addtaxonomy.txt"
    params: scripts = config['scripts'],
            accession2taxadb = config['accession2taxadb']
    log:    stdout = "logs/align_add_taxonomy_name/{taxon}/" \
                     "{software}/{sample}.stdout",
            stderr = "logs/align_add_taxonomy_name/{taxon}/" \
                     "{software}/{sample}.stderr"
    shell:  "Rscript {params.scripts}/blast6fmt_addname.R "
            "-i {input} -o {output} -db {params.accession2taxadb} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_family_contig_number_heatmap:
    input:  expand("05.AllDiamondExtractTaxon/" \
                   "{taxon}/{sample}.diamond_{taxon}.txt", \
                   sample=samples, taxon=config["target_taxons"])
    output: "05.AllDiamondExtractTaxon/" \
            "diamond_{taxon}.FamilyContigNum.heatmap.pdf"
    params: scripts = config['scripts']
    log:    stdout = 'logs/diamond_family_contig_number_heatmap/' \
                     '{taxon}/diamond.stdout',
            stderr = 'logs/diamond_family_contig_number_heatmap/' \ 
                     '{taxon}/diamond.stderr'
    shell:  "python3 {params.scripts}/plot_TaxonContigNum_heatmap.py "
            "--target {input} --output {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_extract_taxon_add_quality:
    input:  target = "05.AllDiamondExtractTaxon/" \
                     "{taxon}/{sample}.diamond_{taxon}.txt",
            quality_summary = "02.AllCheckv/{sample}/quality_summary.tsv"
    output: "06.AllDiamondExtractTaxonAddQuality/{taxon}/"
            "{sample}.diamond_{taxon}.add_quality.txt"
    params: scripts = config['scripts']
    log:    stdout = 'logs/diamond_extract_taxon_add_quality/' \
                     '{taxon}/{sample}.stdout',
            stderr = 'logs/diamond_extract_taxon_add_quality/' \
                     '{taxon}/{sample}.stderr'
    shell:  "python3 {params.scripts}/taxonomy_add_checkv.py "
            "--target {input.target} --checkv {input.quality_summary} "
            "--output {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule diamond_family_quality_number_heatmap:
    input:  expand("06.AllDiamondExtractTaxonAddQuality/{taxon}/" \
                   "{sample}.diamond_{taxon}.add_quality.txt", \
                   sample=samples, taxon=config["target_taxons"])
    output: "06.AllDiamondExtractTaxonAddQuality/" \
            "diamond_{taxon}.FamilyQualityNum.heatmap.pdf"
    params: scripts = config['scripts']
    log:    stdout = 'logs/diamond_family_quality_number_heatmap/' \
                     '{taxon}/diamond.stdout',
            stderr = 'logs/diamond_family_quality_number_heatmap/' \ 
                     '{taxon}/diamond.stderr'
    shell:  "python3 {params.scripts}/plot_TaxonQualityNum_heatmap.py "
            "-i {input} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule compare_different_align_software:
    input:  diamond = expand("06.AllDiamondExtractTaxonAddQuality/{taxon}/" \
                             "{sample}.diamond_{taxon}.add_quality.txt", \
                             sample=samples, taxon=config["target_taxons"]),
            other = expand("09.AllDiamondExtractContigAlignAddTaxon/{taxon}/"\
                           "{software}/{sample}.{software}_addtaxonomy.txt", \
                           sample=samples, taxon=config["target_taxons"], \
                           software=softwares),
    output: "10.CompareAlignmentSoftware/" \
            "{taxon}/{sample}_{taxon}.compare_software.txt"
    params: scripts = config['scripts']
    log:    stdout = 'logs/compare_different_align_software/' \
                     '{taxon}/{sample}.stdout',
            stderr = 'logs/compare_different_align_software/' \ 
                     '{taxon}/{sample}.stderr'
    run:
        all = input.diamond + input.other
        samples = []
        for sample in all:
            sample_name = sample.split('/')[-1].split('.')[0]
            if sample_name == wildcards.sample:
                samples.append(sample)
        input_files = ' '.join(samples)
        shell("python3 {params.scripts}/compare_different_software.py "
              "-i {input_files} -o {output} "
              "1> {log.stdout} "
              "2> {log.stderr}")

rule plot_unclassified_family_venn:
    input:  diamond = expand("06.AllDiamondExtractTaxonAddQuality/{taxon}/" \
                             "{sample}.diamond_{taxon}.add_quality.txt", \
                             sample=samples, taxon=config["target_taxons"]),
            other = expand("09.AllDiamondExtractContigAlignAddTaxon/{taxon}/"\
                           "{software}/{sample}.{software}_addtaxonomy.txt", \
                           sample=samples, taxon=config["target_taxons"], \
                           software=softwares),
    output: "10.CompareAlignmentSoftware/" \
            "{taxon}.compare_software.UnclassifiedFamily.pdf"
    params: scripts = config['scripts']
    log:    stdout = 'logs/plot_unclassified_family_venn/{taxon}.stdout',
            stderr = 'logs/plot_unclassified_family_venn/{taxon}.stderr'
    shell:  "python3 {params.scripts}/plot_venn.py "
            "-i {input.diamond} {input.other} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule compare_extract_unclassified:
    input:  all = "06.AllDiamondExtractTaxonAddQuality/{taxon}/" \
                  "{sample}.diamond_{taxon}.add_quality.txt",
            unclassified = "10.CompareAlignmentSoftware/" \
                           "{taxon}/{sample}_{taxon}.compare_software.txt"
    output: "11.CompareExtractUnclassified/{taxon}/" \
            "{sample}.UnclassifiedFamily.txt"
    params: scripts = config['scripts']
    log:    stdout = 'logs/compare_extract_unclassified/{taxon}/' \
                     '{sample}.stdout',
            stderr = 'logs/compare_extract_unclassified/{taxon}/' \
                     '{sample}.stderr'
    shell:  "python3 {params.scripts}/compare_extract_taxonomy.py "
            "-i {input.all} -c {input.unclassified} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"

rule summary_compare_extract_unclassified:
    input:  expand("11.CompareExtractUnclassified/{taxon}/" \
                   "{sample}.UnclassifiedFamily.txt", \
                   sample=samples, taxon=config["target_taxons"])
    output: "11.CompareExtractUnclassified/" \
            "AllSoftware.UnclassifiedFamilyContig.txt"
    params: scripts = config['scripts']
    log:    stdout = 'logs/summary_compare_extract_unclassified/' \
                     'summary.stdout',
            stderr = 'logs/summary_compare_extract_unclassified/' \
                     'summary.stderr'
    shell:  "python3 {params.scripts}/summary_compare_extract_taxonomy.py "
            "-i {input} -o {output} "
            "1> {log.stdout} "
            "2> {log.stderr}"


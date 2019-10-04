# parallel-arrays-profiling-and-benchmarking
Homework 4: Parallel Arrays, Profiling, and Benchmarking

This tool plots gene expression data collected by the Genotype-Tissue-Expression
(GTEx) project, a ongoing effort to build a comprehensive public database to
study tissue-specific gene expression and regulation. Given an input
GTEx gzip data file and the corresponding sample identification txt file, this
tool creates a box plot displaying gene count data for a target gene.

## How to use

The main script, plot_gtex.py, is designed to be run on the command line using
input arguments managed by argparse. The main function requires 5 input
arguments:

--gene_reads_file : A GTEx_Analysis file ending in '.gct.gz'. Contains
measured gene expression level by tissue type. Input as a string.
ex. 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz'
<https://github.com/swe4s/lectures/blob/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz?raw=true>

--sample_input_file : A txt file containing sample identification
information, corresponding to data in the .gz file. Input as a string.
ex. 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
<https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt>


--group_data_by : Data is displayed by tissue, and can be sorted by
tissue groups (SMTS) or tissue types (SMTSD). Input either 'SMTS' or
'SMTSD' as a string.

--target_gene : The gene of interest to plot. Input as a string. A full
list of available genes can be found here:
<https://github.com/swe4s/lectures/blob/master/data_integration/gtex/acmg_genes.txt>

--output_file_name: File name to save the output plot. Input as a string
with the extension .png.

For example:
```
$ python plot_gtex.py --gene_reads_file 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz' --sample_info_file 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt' --group_data_by 'SMTS' --target_gene 'ACTA2' --output_file_name 'ACTA2_plot.png'
```

## How to Install

    - wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    - bash Miniconda3-latest-Linux-x86_64.sh -b
    - . /home/travis/miniconda3/etc/profile.d/conda.sh
    - conda update --yes conda
    - conda config --add channels r
    - conda create --yes -n test
    - conda activate test
    - conda install -y pycodestyle
    - conda install --yes python=3.6
    - conda install -y matplotlib

## Summary of Profiling and Benchmarking Results

The script plot_gtex.py initially used the linear_search function for all
searches, which iterates through each element in a list from the beginning
when searching for a desired key. cProfile revealed that the linear search
function accounted for a significant proportion of overall script run time.
Compared to the entire run time of the Main() function, calling linear script
accounted for 98.6% of run time.
cProfile results:
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 45904   30.489    0.001   30.495    0.001 plot_gtex.py:8(linear_search)
 28724    0.210    0.000    0.210    0.000 {method 'split' of 'str' objects}
     1    0.165    0.165   30.932   30.932 plot_gtex.py:28(main)

Based on these results, the binary search function was substituted for linear
search when searching through the gzip gene expression data file.

GNA time with linear search:
35.24 elapsed time in seconds	139400 maximum memory usage in kilobytes

GNU time with binary search:
8.28 elapsed time in second     170040 maximum memory usage in kilobytes

This demonstrates that using binary search is faster and more efficient than
linear search.

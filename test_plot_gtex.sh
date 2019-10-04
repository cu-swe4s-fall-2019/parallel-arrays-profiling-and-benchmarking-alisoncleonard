#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest
source ssshtest

pycodestyle plot_gtex.py

run test_find_file python plot_gtex.py --gene_reads_file 'GTEx_Analysis-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz' --sample_info_file 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt' --group_data_by 'SMTS' --target_gene 'ACTA2' --output_file_name 'ACTA2_plot.png'
assert_no_stdout
assert_exit_code 1

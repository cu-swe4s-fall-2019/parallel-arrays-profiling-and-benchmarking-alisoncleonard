"""
Script to import gzip files containing GTEx genomic expression data and plot
the gene counts for a chosen gene.
"""

import data_viz
import gzip
import sys
import time
import argparse
import importlib
sys.path.insert(1, './hash-tables-alisoncleonard')
import hash_tables as ht

def linear_search(key, L):
    """Searches a list for a key using the linear search method

    Parameters
    -----------
    key : string or int of interest, used to search list

    L : list to search

    Returns
    --------

    If the key is found in the list, returns the list index containing the key
    """
    hit = -1
    for i in range(len(L)):
        curr = L[i]
        if key == curr:
            return i
    return -1


def binary_search(key, D):
    """Searches a list for a key using the binary search method

    Parameters
    -----------
    key : string or int of interest, used to search list

    D : list to search

    Returns
    --------

    If the key is found in the list, returns the list index containing the key
    """

    lo = -1
    hi = len(D)
    print(lo)
    print(hi)
    while (hi - lo > 1):
        mid = (hi + lo) // 2

        if key == D[mid][0]:
            return D[mid][1]

        if (key < D[mid][0]):
            hi = mid
        else:
            lo = mid

    return -1


def main():
    """Creates box plots of gene expression data from GTEx analysis

    Parameters
    -----------
    --gene_reads_file : A GTEx_Analysis file ending in '.gct.gz'. Contains
    measured gene expression level by tissue type. Input as a string.
    ex. 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz'

    --sample_input_file : A txt file containing sample identification
    information, corresponding to data in the .gz file. Input as a string.
    ex. 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'

    --group_data_by : Data is displayed by tissue, and can be sorted by
    tissue groups (SMTS) or tissue types (SMTSD). Input either 'SMTS' or
    'SMTSD' as a string.

    --target_gene : The gene of interest to plot. Input as a string. A full
    list of available genes can be found here: https://github.com/swe4s/
    lectures/blob/master/data_integration/gtex/acmg_genes.txt

    --output_file_name: File name to save the output plot. Input as a string
    with the extension .png.

    Returns
    --------

    Function returns a box plot of expression data, saved in the local
    directory as output_file_name.

    """

    parser = argparse.ArgumentParser(description='plot gene expression data '
                                     'from gtex files', prog='plot_gtex.py')

    parser.add_argument('--gene_reads_file', type=str, help='Name of gene'
                        'count input file', required=True)

    parser.add_argument('--sample_info_file', type=str, help='Name of sample'
                        'info input file', required=True)

    parser.add_argument('--group_data_by', type=str, help='Select either'
                        'tissue groups (SMTS) or tissue types (SMTSD)',
                        required=True)

    parser.add_argument('--target_gene', type=str, help='Gene of interest to '
                        'plot', required=True)

    parser.add_argument('--output_file_name', type=str, help='Name for saved'
                        'output graph', required=True)

    args = parser.parse_args()

    try:
        # file with gene read counts for each sample
        data_file_name = args.gene_reads_file
        # file with informational headers for each sample
        sample_info_file_name = args.sample_info_file
    except FileNotFoundError:
        print('Could not find input data file')
        sys.exit(1)
    except PermissionError:
        print('Could not open input data file')
        sys.exit(1)

    # plot gene expression of tissue groups (SMTS) or tissue types (SMTSD)
    # choice stored in variable 'tissue_selection'
    group_col_name = args.group_data_by

    # gene of interest to plot
    gene_name = args.target_gene

    sample_to_count_map = ht.ChainedHash(1000000, ht.hash_functions.h_rolling)

    version = None
    dim = None
    data_header = None

    gene_name_col = 1

    for l in gzip.open(data_file_name, 'rt'):

        if version == None:
            version = l
            continue

        if dim == None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        if data_header == None:
            data_header = l.rstrip().split('\t')
            continue

        # remove first and second items from list (not sample ids)
        data_header.pop(0)
        data_header.pop(0)
        sample_ids = data_header

        A = l.rstrip().split('\t')
        print(A[gene_name_col])

        for sample_i in range(len(sample_ids)):
            if A[gene_name_col] == gene_name:
                sample_to_count_map.add(sample_ids[sample_i], A[sample_i])

    samples_to_tissues_map = ht.ChainedHash(1000000, ht.hash_functions.h_rolling)

    # in new hash table, SAMPID is from column 0, SMTS column 5, SMTSD column

    tissues_list = []

    for l in open(sample_info_file_name):
        line_split = l.rstrip().split('\t')
        if group_col_name == 'SMTS':
            if line_split[5] not in tissues_list:
                tissues_list.append(line_split[5])
            samples_to_tissues_map.add(line_split[0], line_split[5])
        if group_col_name == 'SMTSD':
            if line_split[5] not in tissues_list:
                tissues_list.append(line_split[5])
            samples_to_tissues_map.add(line_split[0], line_split[6])

    tissues_list.pop(0)  # remove SMTS or SMTSD from list

    group_counts = []

    for tissue in tissues_list:
        counts = []
        for sample in sample_ids:
            if samples_to_tissues_map.search(sample) == tissue:
                counts.append(int(sample_to_count_map.search(sample)))
        group_counts.append(counts)

    # ploting with data_viz.py module
    # code will output a list of lists containing gene data for tissue type,
    # and a list of names corresponding to each list of data to box plot

    saved_plot_name = args.output_file_name
    title = str(gene_name)
    x_label = group_col_name
    y_label = "Gene read counts"
    data = group_counts
    x_ticks = tissues_list

    data_viz.boxplot(saved_plot_name, title, x_label, y_label, data, x_ticks)


if __name__ == '__main__':
    main()

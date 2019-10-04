"""
Script to import gzip files containing GTEx genomic expression data and plot
the gene counts for a chosen gene.
"""

import data_viz
import gzip
import sys
import time
import argparse


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

    # file with gene read counts for each sample
    data_file_name = args.gene_reads_file
    # file with informational headers for each sample
    sample_info_file_name = args.sample_info_file

    # plot gene expression of tissue groups (SMTS) or tissue types (SMTSD)
    # choice stored in variable 'tissue_selection'
    group_col_name = args.group_data_by

    # gene of interest to plot
    gene_name = args.target_gene

    # pull sample id numbers
    sample_id_col_name = 'SAMPID'

    samples = []
    sample_info_header = None
    for l in open(sample_info_file_name):
        if sample_info_header is None:
            sample_info_header = l.rstrip().split('\t')
        else:
            samples.append(l.rstrip().split('\t'))

    # linear search to find indices of target group in sample_info_header
    group_col_idx = linear_search(group_col_name, sample_info_header)
    # linear search to pull sample id indices from sample_info_header
    sample_id_col_idx = linear_search(sample_id_col_name, sample_info_header)

    groups = []  # pull list of sample names, use as xtick labels when plotting
    members = []

    for row_idx in range(len(samples)):
        sample = samples[row_idx]
        # check if could pull list of sample names from here
        sample_name = sample[sample_id_col_idx]
        curr_group = sample[group_col_idx]

        curr_group_idx = linear_search(curr_group, groups)

        if curr_group_idx == -1:
            curr_group_idx = len(groups)
            groups.append(curr_group)
            members.append([])

        members[curr_group_idx].append(sample_name)

    version = None
    dim = None
    data_header = None

    gene_name_col = 1

    group_counts = [[] for i in range(len(groups))]

    for l in gzip.open(data_file_name, 'rt'):  # 'rt' needed for gzip file
        if version is None:
            version = l
            continue

        if dim is None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        t0_sort = time.time()
        if data_header is None:
            data_header = []
            i = 0
            for field in l.rstrip().split('\t'):
                data_header.append([field, i])
                i += 1
            data_header.sort(key=lambda tup: tup[0])
            continue
        t1_sort = time.time()

        A = l.rstrip().split('\t')

        t0_search = time.time()
        if A[gene_name_col] == gene_name:
            for group_idx in range(len(groups)):
                for member in members[group_idx]:
                    member_idx = binary_search(member, data_header)
                    if member_idx != -1:
                        group_counts[group_idx].append(int(A[member_idx]))
            break
        t1_search = time.time()

    sort_time = t1_sort - t0_sort
    search_time = t1_search - t0_search

    # ploting with data_viz.py module
    # code will output a list of lists containing gene data for tissue type,
    # and a list of names corresponding to each list of data to box plot

    saved_plot_name = args.output_file_name
    title = str(gene_name)
    x_label = group_col_name
    y_label = "Gene read counts"
    data = group_counts
    x_ticks = groups

    data_viz.boxplot(saved_plot_name, title, x_label, y_label, data, x_ticks)


if __name__ == '__main__':
    main()

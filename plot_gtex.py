import data_viz
import gzip
import sys
import time
import argparse


def linear_search(key, L):
    """
    When iterating through a for loop, returns the index of the key if the
    key is in the list
    """
    hit = -1
    for i  in range(len(L)):
        curr =  L[i]
        if key == curr:
            return i
    return -1


def binary_serach(key, L):
    """
    document code
    """
    pass


def main():
    """
    document code
    """

    # our file name: 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz'
    # our sample info: 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
    # if you want to read normally, try opening as excel file, specify txt is tab delineated

    #python plot_gtex.py --gene_reads_file 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz' --sample_info_file 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt' --group_data_by 'SMTS' --target_gene 'ACTA2' --output_file_name '_test_plot.png'

    parser = argparse.ArgumentParser(description= 'plot gene expression data '
                                    'from gtex files', prog='plot_gtex.py')

    parser.add_argument('--gene_reads_file', type=str, help='Name of gene count'
                        'infofile', required=True)

    parser.add_argument('--sample_info_file', type=str, help='Name of sample info'
                        'input file', required=True)

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

    # plot gene expression across either tissue groups (SMTS) or tissue types (SMTSD)
    # choice stored in variable 'tissue_selection'
    group_col_name = args.group_data_by

    # gene of interest to plot
    gene_name = args.target_gene

    # pull sample id numbers
    sample_id_col_name = 'SAMPID'

    samples = []
    sample_info_header = None
    for l in open(sample_info_file_name):
        if sample_info_header == None:
            sample_info_header = l.rstrip().split('\t')
        else:
            samples.append(l.rstrip().split('\t'))

    # linear search to find indices of target group in sample_info_header
    group_col_idx = linear_search(group_col_name, sample_info_header)
    # linear search to pull sample id indices from sample_info_header
    sample_id_col_idx = linear_search(sample_id_col_name, sample_info_header)

    groups = [] # pull list of sample names, use as xtick labels when plotting
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

    group_counts = [ [] for i in range(len(groups)) ]

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

        A = l.rstrip().split('\t')

        if A[gene_name_col] == gene_name:
            for group_idx in range(len(groups)):
                for member in members[group_idx]:
                    member_idx = linear_search(member, data_header)
                    if member_idx != -1:
                        group_counts[group_idx].append(int(A[member_idx]))
            break


    # ploting with data_viz.py module
    # code will output a list of lists containing gene data for a specific tissue type,
    # and a list of names corresponding to each list of data to box plot

    plot_name = str(gene_name) + str(args.output_file_name)
    plot_title = str(gene_name) + "_plot"
    x_axis_label = group_col_name
    y_axis_label = "Gene read counts"
    data = group_counts
    x_ticks = groups

    data_viz.boxplot(plot_name, plot_title, x_axis_label, y_axis_label, data, x_ticks)







if __name__ == '__main__':
    main()

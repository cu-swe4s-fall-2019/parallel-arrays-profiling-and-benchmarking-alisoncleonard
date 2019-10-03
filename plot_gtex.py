import data_viz
import gzip
import sys
import time
import argparse


def linear_search_by_line(key, L):
    """
    When iterating through a for loop, returns the index of the key if the
    key is in the list
    """
    for i in range(len(L)):
        if key == L[i]:
            return i

def linear_search(key, L):
    """
    returns a list containing all indices where the key occurs
    """
    hit = []
    for i in range(len(L)):
        if key == L[i]:
            hit.append(i)
    return hit


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

    #python plot_gtex.py --gene_reads_file 'GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz' --sample_info_file 'GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt' --group_data_by 'SMTS' --target_gene 'ACTA2' --output_file_name 'ACTA2_graph'

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
    data_group = args.group_data_by

    # gene of interest to plot
    gene_name = args.target_gene

    sample_id_data = []
    sample_info = None

    for l in open(sample_info_file_name, 'r'):
        if sample_info == None:
            sample_info = l.rstrip().split('\t')
            continue

            data_group_idx = linear_search_by_line(data_group, sample_info)
            sample_id_idx = linear_search_by_line('SAMPID', sample_info)

            sample_id_data.append(sample_info[sample_id_idx])

    print(sample_id_data)


            #sample_IDs.append(l.rstrip().split('\t'))

    # linear search for tissue data type (SMTS or SMTSD) in sample_info_header
    # returns list of all indices with that column name
    #data_type_idx = linear_search(tissue_data_type, sample_info_header)






    #print(sample_IDs)
    #print(sample_info_header)
    #print(sample_id_idx)


    version = None
    dim = None
    rna_header = None


    for l in gzip.open(data_file_name, 'rt'):
        if version == None:
            version = l
            continue

        if dim == None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        if rna_header == None:
            rna_header = l.rstrip().split('\t')
            continue

        # sorting list array for binary search
        # data_header_plus_index = []
        # for i in rangle(len(data_header)):
        #     # first position in pair has value, second has its old position
        #     # for use in binary search
        #     data_header_plus_index.append(data_header[i], i)

        rna_counts = l.rstrip().split('\t')

        # do we need to look for all types of tissue and plat each one?
        description_idx = linear_search('Description', rna_header)

        # test that description is in header
        if description_idx == -1:
            sys.exit('Description not found in header')
        # description is too generic - we need the actual sample types (example blood,
        # brain) to get the rna counts for each sample type
        # the sample names will be in the sample data spreadsheet - extract along with index?
        #if rna_counts[Description]





        # code will output a list of lists containing gene data for a specific tissue type,
        # and a list of names corresponding to each list of data to box plot

        #plot_name = args.output_file_name
        # plot_tile = str(gene_name) + "_plot.png"
        # x_axis_label = tissue_data_type
        # y_axis_label = "Gene read counts"
        #
        # boxplot(plot_name, plot_title, x_axis_label, y_axis_label, lists, x_ticks)




if __name__ == '__main__':
    main()

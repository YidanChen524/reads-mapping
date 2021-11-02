import sys
import helpers
from classes.suffix_tree import SuffixTree


def search_st(refs, reads):
    for ref_key, ref_val in refs.items():
        st = SuffixTree(ref_val)
        for read_key, read_val in reads.items():
            positions = st.find(read_val)
            if positions != -1:
                for pos in positions:
                    helpers.print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                      CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))


if __name__ == '__main__':
    # read in the fasta and fastq files
    refs = helpers.parse_fa(sys.argv[1])
    reads = helpers.parse_fq(sys.argv[2])
    # run the naive st search algorithm and print the output in SAM format
    search_st(refs, reads)

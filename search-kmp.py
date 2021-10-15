import sys
import utils


def search_kmp(refs, reads):
    """
    searches exact match of reads in refs using the kmp algorithm and prints the output in SAM format
    based on the idea of border arrays.
    If a mismatch happens, move the read to a position where we can skip matching the prefix

    Args:
         refs: a dict storing the names and content of sequences in the fasta file
         reads: a dict storing the names and content of sequences in the fastq file
    """
    for read_key, read_val in reads.items():
        for ref_key, ref_val in refs.items():
            n = len(ref_val)
            m = len(read_val)
            # construct a border array for the read
            ba = utils.border_array(read_val)

            i = j = 0
            while j < n:
                # if a position matches, increment both indices
                while i < m and j < n and ref_val[j] == read_val[i]:
                    j += 1
                    i += 1
                # if reach the end of a read, print the match in SAM format
                if i == m:
                    utils.print_sam(QNAME=read_key, RNAME=ref_key, POS=j - m + 1,
                                    CIGAR=f'{str(m)}M', SEQ=read_val, QUAL='~' * m)
                # mismatch happens at the very first position of the read, move to next position in the ref
                if i == 0:
                    j += 1
                # mismatch happens at position greater than 0, decrement i to the index of its longest border
                else:
                    i = ba[i - 1]


if __name__ == '__main__':
    # read in the fasta and fastq files
    refs = utils.parse_fa(sys.argv[1])
    reads = utils.parse_fq(sys.argv[2])
    # run the naive search algorithm and print the output in SAM format
    search_kmp(refs, reads)

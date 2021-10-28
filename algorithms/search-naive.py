import sys
import helpers


def search_naive(refs: dict[str, str], reads: dict[str, str]) -> None:
    """
    searches exact match of reads in refs using the naive search algorithm and prints the output in SAM format
    for every read and every reference, check every position in the reference to see if there is a exact match

    Args:
         refs: a dict storing the names and content of sequences in the fasta file
         reads: a dict storing the names and content of sequences in the fastq file
    """
    for read_key, read_val in reads.items():
        for ref_key, ref_val in refs.items():
            n = len(ref_val)
            m = len(read_val)
            for j in range(n - m + 1):
                for i in range(m):
                    if read_val[i] != ref_val[j + i]:
                        break
                else:
                    helpers.print_sam(QNAME=read_key, RNAME=ref_key, POS=j + 1,
                                      CIGAR=f'{str(m)}M', SEQ=read_val, QUAL='~'*m)


if __name__ == '__main__':
    # read in the fasta and fastq files
    refs = helpers.parse_fa(sys.argv[1])
    reads = helpers.parse_fq(sys.argv[2])
    # run the naive search algorithm and print the output in SAM format
    search_naive(refs, reads)

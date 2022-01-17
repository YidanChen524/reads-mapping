import os
import sys
import helpers
from classes.suffix_tree import SuffixTree
from classes.suffix_tree_from_lcp import SuffixTreeFromLCP
from gen_lcp import traverse, write_to_file


def search_st2(refs, reads):
    for ref_key, ref_val in refs.items():
        # build a suffix tree
        st = SuffixTree(ref_val)
        # construct sa and lcp
        sa, lcp = traverse(st)
        # build a suffix tree from sa and lcp
        st2 = SuffixTreeFromLCP(ref_val, sa, lcp)
        # search for patterns and print in SAM
        for read_key, read_val in reads.items():
            positions = st2.find(read_val)
            if positions != -1:
                for pos in positions:
                    helpers.print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                      CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))


def search_st2_with_preprocess(fname, refs, reads):
    with open(fname, "r") as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        if lines[i]:
            ref_key = lines[i].strip("\n")
            ref_val = refs[ref_key]
            sa = [int(i) for i in lines[i+1].strip("[|]\n").split(",")]
            lcp = [int(i) for i in lines[i+2].strip("[|]\n").split(",")]
        # build a suffix tree from sa and lcp
        st2 = SuffixTreeFromLCP(ref_val, sa, lcp)
        # search for patterns and print in SAM
        for read_key, read_val in reads.items():
            positions = st2.find(read_val)
            if positions != -1:
                for pos in positions:
                    helpers.print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                      CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))


if __name__ == '__main__':
    # parse arguments
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    # read in the fasta
    refs = helpers.parse_fa(args[0])
    # if option -p is present, generate a file containing sa and lcp
    if "-p" in opts:
        fname = args[0] + ".lcp"
        write_to_file(refs, fname)
    # if both fa and fq files present, run the search algorithm
    if len(args) == 2:
        reads = helpers.parse_fq(args[1])
        # when preprocess file available
        if "-p" in opts:
            search_st2_with_preprocess(fname, refs, reads)
        else:
            search_st2(refs, reads)

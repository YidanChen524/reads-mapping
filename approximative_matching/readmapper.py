from suffix_tree import SuffixTree
from helpers import *
import sys


def preprocess(filename, refs):
    """generate sa and lcp array and store them in filename"""
    with open(filename, "w") as f:
        for ref_name, ref_val in refs.items():
            sa = suffix_array(ref_val)
            lcp = lcp_array(ref_val, sa)
            f.write(ref_name)
            f.write("\n")
            f.write(str(sa))
            f.write("\n")
            f.write(str(lcp))
            f.write("\n\n")


def read_from_preprocess(filename):
    """read from preprocess file and return a dictionary containing sa and lcp information for each ref"""
    with open(filename, "r") as f:
        lines = f.readlines()
    preprocess_info = {}
    for i in range(0, len(lines), 4):
        if lines[i]:
            ref_key = lines[i].strip("\n")
            sa = [int(i) for i in lines[i+1].strip("[|]\n").split(",")]
            lcp = [int(i) for i in lines[i+2].strip("[|]\n").split(",")]
            preprocess_info[ref_key] = [sa, lcp]
    return preprocess_info


def mapping(refs, reads, preprocess_info, edits):
    """map reads to reference and print output in sam format"""
    for ref_key, ref_val in refs.items():
        sa, lcp = preprocess_info[ref_key]
        st = SuffixTree(ref_val, sa, lcp)
        for read_key, read_val in reads.items():
            positions, cigars = st.find_approx(read_val, edits)
            for i in range(len(positions)):
                print_sam(QNAME=read_key, RNAME=ref_key, POS=positions[i]+1,
                          CIGAR=cigars[i], SEQ=read_val, QUAL='~'*len(read_val))


if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if "-p" in opts:
        # preprocess
        refs = parse_fa(args[0])
        filename = args[0] + ".preprocess"
        preprocess(filename, refs)
    else:
        # read from preprocess file
        if len(args) == 2:
            d = 0
            refs = parse_fa(args[0])
            reads = parse_fq(args[1])
            # read from preprocess file
            filename = args[0] + ".preprocess"
            preprocess_info = read_from_preprocess(filename)
        elif len(args) == 3:
            d = int(args[0])
            refs = parse_fa(args[1])
            reads = parse_fq(args[2])
            filename = args[1] + ".preprocess"
            preprocess_info = read_from_preprocess(filename)
        # run the search algorithm
        mapping(refs, reads, preprocess_info, d)

import sys
from helpers import suffix_array, parse_fq, parse_fa, print_sam


def compare(x, suffix, p):
    """
    compare whether the suffix is lexicographically smaller than the pattern
    if suffix is smaller, return -1. if suffix is greater, return 1. if there is a match, return 0
    """
    for i in range(len(p)):
        if x[suffix+i] == "$" and p[i] != "$":
            return -1
        elif x[suffix+i] < p[i]:
            return -1
        elif x[suffix+i] > p[i]:
            return 1
    else:
        return 0


def find_lower(x, l, r, p, sa):
    """find the lower bound recursively"""
    if compare(x, sa[l], p) == 0 or r - l <= 1:
        return l
    else:
        mid = l + int((r - l)/2)
        if compare(x, sa[mid], p) == -1:
            return find_lower(x, mid, r, p, sa)
        else:
            return find_lower(x, l, mid, p, sa)


def find_upper(x, l, r, p, sa):
    """find the upper bound recursively"""
    if compare(x, sa[r], p) == 0 or r - l <= 1:
        return r
    else:
        mid = l + int((r - l)/2)
        if compare(x, sa[mid], p) == -1:
            return find_upper(x, mid, r, p, sa)
        else:
            return find_upper(x, l, mid, p, sa)


def search_bs(x, p, sa=None):
    if not sa:
        sa = suffix_array(x)
    x = x + "$"
    l, r = 0, len(sa) - 1
    if r - l > 1:
        lower = find_lower(x, l, r, p + "$", sa)
        upper = find_upper(x, l, r, p + "~", sa)
    else:
        lower, upper = l, r
    positions = []
    for i in range(lower, upper+1):
        if compare(x, sa[i], p) == 0:
            positions.append(sa[i])
    return positions


def preprocess(fname, refs):
    with open(fname, "w") as f:
        for ref_name, ref_val in refs.items():
            sa = suffix_array(ref_val)
            f.write(ref_name)
            f.write("\n")
            f.write(str(sa))
            f.write("\n\n")


def read_from_preprocess(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    preprocess_info = {}
    for i in range(0, len(lines), 3):
        if lines[i]:
            key = lines[i].strip("\n")
            sa = [int(i) for i in lines[i+1].strip("[|]\n").split(",")]
        preprocess_info[key] = sa
    return preprocess_info


if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    # read in the fasta
    refs = parse_fa(args[0])
    # if option -p is present, generate a file containing sa
    if "-p" in opts:
        fname = args[0] + ".bs"
        preprocess(fname, refs)
    # if both fa and fq files present, run the search algorithm
    if len(args) == 2:
        reads = parse_fq(args[1])
        # when preprocess file available
        if "-p" in opts:
            preprocess_info = read_from_preprocess(fname)
            for ref_key, ref_val in refs.items():
                for read_key, read_val in reads.items():
                    positions = search_bs(ref_val, read_val, preprocess_info[ref_key])
                    for pos in positions:
                        print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                  CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))
        else:
            for ref_key, ref_val in refs.items():
                for read_key, read_val in reads.items():
                    positions = search_bs(ref_val, read_val)
                    for pos in positions:
                        print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                  CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))




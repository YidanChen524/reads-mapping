import sys
from helpers import suffix_array, parse_fq, parse_fa, print_sam


def burrows_wheeler_transform(x: str, sa: list[int]) -> list[str]:
    """return the bwt array given string x and its suffix array"""
    x = x + "$"
    return [x[sa[i]-1] if sa[i] > 0 else "$" for i in range(len(sa))]


def bucket_positions(x: str, sa: list[int]) -> dict[str, int]:
    """return a dict contains indices of first occurrences of all characters based on sa"""
    x = x + "$"
    c = {}
    for i in range(len(sa)):
        if x[sa[i]] not in c:
            c[x[sa[i]]] = i
    return c


def occ(bwt: str) -> dict[str, list[int]]:
    """return the occ table where o[i, a] is the number of a's in bwt before index i"""
    o = {}
    for i in range(1, len(bwt)+1):
        if bwt[i-1] not in o:
            o[bwt[i-1]] = [0] * (len(bwt) + 1)
        for key in o.keys():
            if key == bwt[i-1]:
                o[key][i] = o[key][i-1] + 1
            else:
                o[key][i] = o[key][i-1]
    return o


def fm_index_search(p: str, c: dict[str, int], o: dict[str, list[int]]):
    l, r = 0, len(o["$"]) - 1
    for i in range(len(p)-1, -1, -1):
        if l == r:
            break
        a = p[i]
        l = c[a] + o[a][l]
        r = c[a] + o[a][r]
    return [l, r]


def search_bw(x, p, sa=None, c=None, o=None):
    if not sa:
        sa = suffix_array(x)
    if not o:
        bwt = burrows_wheeler_transform(x, sa)
        o = occ(bwt)
    if not c:
        c = bucket_positions(x, sa)
    l, r = fm_index_search(p, c, o)
    return sa[l:r]


def preprocess(fname, refs):
    with open(fname, "w") as f:
        for ref_name, ref_val in refs.items():
            sa = suffix_array(ref_val)
            bwt = burrows_wheeler_transform(ref_val, sa)
            c = bucket_positions(ref_val, sa)
            o = occ(bwt)
            f.write(ref_name)
            f.write("\n")
            f.write(str(sa))
            f.write("\n")
            f.write(str(c))
            f.write("\n")
            f.write(str(o))
            f.write("\n\n")


def read_from_preprocess(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    preprocess_info = {}
    for i in range(0, len(lines), 5):
        if lines[i]:
            key = lines[i].strip("\n")
            sa = [int(i) for i in lines[i+1].strip("[|]\n").split(",")]
            c = {}
            arr = [s.split(": ") for s in lines[i+2].strip("{|}\n").split(",")]
            for a in arr:
                c[a[0].strip(" '")] = int(a[1])
            o = {}
            arr = [s.split("[") for s in lines[i+3].strip("{|}\n").split("]")]
            for a in arr:
                if len(a) == 2:
                    o[a[0].strip(", ': ")] = [int(i) for i in a[1].split(",")]
        preprocess_info[key] = [sa, c, o]
    return preprocess_info


if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    # read in the fasta
    refs = parse_fa(args[0])
    # if option -p is present, generate a file containing sa, c, and o
    if "-p" in opts:
        fname = args[0] + ".bwt"
        preprocess(fname, refs)
    # if both fa and fq files present, run the search algorithm
    if len(args) == 2:
        reads = parse_fq(args[1])
        # when preprocess file available
        if "-p" in opts:
            preprocess_info = read_from_preprocess(fname)
            for ref_key, ref_val in refs.items():
                for read_key, read_val in reads.items():
                    positions = search_bw(ref_val, read_val, *preprocess_info[ref_key])
                    for pos in positions:
                        print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                  CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))
        else:
            for ref_key, ref_val in refs.items():
                for read_key, read_val in reads.items():
                    positions = search_bw(ref_val, read_val)
                    for pos in positions:
                        print_sam(QNAME=read_key, RNAME=ref_key, POS=pos+1,
                                  CIGAR=f'{str(len(read_val))}M', SEQ=read_val, QUAL='~'*len(read_val))

"""
Helper functions
"""


def parse_fa(fname: str) -> dict[str, str]:
    """parse fasta file and return a dictionary"""
    with open(fname, 'r') as f:
        lines = f.readlines()
    refs = {}
    for i in range(len(lines)):
        if lines[i][0] == '>':
            ref_name = lines[i][1:].strip('\n')
            ref_val = ""
            while i < len(lines) - 1 and lines[i + 1][0] != '>':
                ref_val += lines[i + 1].strip('\n')
                i += 1
            refs[ref_name] = ref_val
    return refs


def parse_fq(fname: str) -> dict[str, str]:
    """parse fastq file and return a dictionary"""
    with open(fname, 'r') as f:
        lines = f.readlines()
    reads = {}
    for i in range(len(lines)):
        if lines[i][0] == '@':
            reads[lines[i][1:].strip('\n')] = lines[i + 1].strip('\n')
            i += 4
    return reads


def print_sam(QNAME: str = '', FLAG: int = 0, RNAME: str = '',
              POS: int = -1, MAPQ: int = 0, CIGAR: str = '',
              RNEXT: str = '*', PNEXT: int = 0, TLEN: int = 0,
              SEQ: str = '', QUAL: str = '') -> None:
    """print in SAM format for a single match"""
    print(QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, QUAL, sep='\t')


def compress_cigar(cigar: str):
    """compress the cigar string"""
    new_cigar = ""
    count = 1
    for i in range(1, len(cigar)):
        if cigar[i] == cigar[i-1]:
            count += 1
        else:
            new_cigar = "".join([new_cigar, f"{count}{cigar[i-1]}"])
            count = 1
    else:
        new_cigar = "".join([new_cigar, f"{count}{cigar[len(cigar)-1]}"])
    return new_cigar


def suffix_array(x: str) -> list[int]:
    """return the suffix array of string x"""
    x += "$"
    sa = sorted(range(len(x)), key=lambda k: x[k:])
    return sa


def lcp_array(x: str, sa: list[int]) -> list[int]:
    """return the lcp array given the suffix array"""
    x += "$"
    n = len(x)
    lcp = [0] * n
    for i in range(1, n):
        for j in range(min(n-sa[i-1], n-sa[i])):
            if x[sa[i-1]+j] != x[sa[i]+j]:
                break
            else:
                lcp[i] += 1
    return lcp


if __name__ == "__main__":
    x = "helllo"
    sa = suffix_array(x)
    lcp = lcp_array(x, sa)
    print(sa, lcp)
    for i in sa:
        print((x+"$")[i:])

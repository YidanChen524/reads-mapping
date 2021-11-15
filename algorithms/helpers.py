"""
Helper functions
"""


def parse_fa(fname: str) -> dict[str, str]:
    """parse fasta file

    Args:
        fname: the name of the fasta file
    Returns:
        a dictionary where each entry is (sequence name, sequence content)
    """
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
    """parse fastq file

    Args:
        fname: the name of the fastq file
    Returns:
        a dictionary where each entry is (sequence name, sequence content)
    """
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
    """prints in SAM format for a single match"""
    QNAME = QNAME
    FLAG = FLAG
    RNAME = RNAME
    POS = POS
    MAPQ = MAPQ
    CIGAR = CIGAR
    RNEXT = RNEXT
    PNEXT = PNEXT
    TLEN = TLEN
    SEQ = SEQ
    QUAL = QUAL

    print(QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, QUAL, sep='\t')


def cigar():
    pass


def border_array(x: str) -> list[int]:
    """
    helper function that constructs a border array for a given string.
    a border of string x is any proper prefix (not the full string) that equals a suffix of x.
    a border array ba of string x is an integer array where ba[i] is the length of the longest border of x[0:i+1].

    Args:
        x: input string
    Returns:
        an integer list which is the border array of x
    """
    ba = [0] * len(x)
    # starts from position 1, see if we can find ba[i] by tryinG to extend the longest border of i-1
    for i in range(1, len(x)):
        b = ba[i - 1]
        while b > 0 and x[b] != x[i]:
            # if cannot extend the longest border of i-1
            # try extending the longest border of the longest border of i-1, recursively until the border is empty
            b = ba[b - 1]
        # now b is either the length of the longest border (including empty border) we can extend
        # or it reached 0 because no borders were found
        # update the value respectively
        ba[i] = b + 1 if x[b] == x[i] else 0
    return ba

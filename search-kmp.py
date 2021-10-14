import sys

# FASTA parser
refs = {}

with open(sys.argv[1],'r') as f:
    lst = f.readlines()

for i in range(len(lst)):
    if lst[i][0] == '>':
        ref_name = lst[i][1:].strip('\n')
        ref_val = ""
        while i < len(lst) - 1 and lst[i+1][0] != '>':
            ref_val += lst[i+1].strip('\n')
            i += 1
        refs[ref_name] = ref_val


# FASTQ parser
reads = {}

with open(sys.argv[2], 'r') as f:
    lst = f.readlines()

for i in range(len(lst)):
    if lst[i][0] == '@':
        reads[lst[i][1:].strip('\n')] = lst[i+1].strip('\n')
        i += 4


# helper functions that construct border arrays
def border_array(s):
    ba = [0] * len(s)
    for i in range(1, len(s)):
        b = ba[i - 1]
        while b > 0 and s[b] != s[i]:
            b = ba[b - 1]
        ba[i] = b + 1 if s[b] == s[i] else 0
    return ba


# maps
for read_key, read_val in reads.items():
    for ref_key, ref_val in refs.items():
        n = len(ref_val)
        m = len(read_val)
        ba = border_array(read_val)

        i = j = 0
        while j < n:
            while i < m and j < n and ref_val[j] == read_val[i]:
                j += 1
                i += 1
            if i == m:
                QNAME = read_key
                FLAG = 0
                RNAME = ref_key
                POS = j - m + 1
                MAPQ = 0
                CIGAR = f'{str(m)}M'
                RNEXT = '*'
                PNEXT = 0
                TLEN = 0
                SEQ = read_val
                QUAL = '~' * m
                print(QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, QUAL)
            if i == 0:
                j += 1
            else:
                i = ba[i-1]

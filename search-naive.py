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


# maps
for read_key, read_val in reads.items():
    for ref_key, ref_val in refs.items():
        n = len(ref_val)
        m = len(read_val)
        for j in range(n-m+1):
            for i in range(m):
                if read_val[i] != ref_val[j+i]:
                    break
            else:
                QNAME = read_key
                FLAG = 0
                RNAME = ref_key
                POS = j+1
                MAPQ = 0
                CIGAR = f'{str(m)}M'
                RNEXT = '*'
                PNEXT = 0
                TLEN = 0
                SEQ = read_val
                QUAL = '~' * m
                print(QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, QUAL)


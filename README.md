# Readmappers
Programs that search patterns in sequences, map short reads to reference sequences

## Exact Matching

### search one pattern at a time
- Naive algorithm (search_naive.py)
- Knuth-Morris-Pratt (search_kmp.py)

### search multiple patterns at a time
- Suffix tree 
  - Naive algorithm (search_st.py)
  - constructed from suffix array and lcp array (search_st2.py)
- Suffix array
  - Binary search (search_bs.py)
  - Burrows-Wheelers algorithm (search_bw.py)
  
## Approximative Matching

- Suffix tree

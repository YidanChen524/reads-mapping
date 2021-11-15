import sys
from helpers import parse_fa
from classes.suffix_tree import SuffixTree


def traverse(tree):
    """ construct sa and lcp arrays by traversing the suffix tree"""
    global sa, lcp, count
    sa = [0] * tree.len
    lcp = [0] * tree.len
    count = 0
    traverse_recursive(tree.root)
    return sa, lcp


def traverse_recursive(node):
    """traverse the suffix tree recursively and edit the sa and lcp array"""
    global sa, lcp, count
    if not node.next:
        # reach a leaf, modified corresponding entry in sa
        sa[count] = node.leaves[0]
        count += 1
    else:
        # for all leaves(except the first) under current subtree
        # increase its lcp value by the length of the current node
        for i in range(1, len(node.leaves)):
            lcp[count+i] += node.end - node.start
        # sort the following nodes and traverse
        for key in sorted(node.next):
            traverse_recursive(node.next[key])


def write_to_file(refs, fname):
    """write the sa and lcp to file for sequences in fasta file"""
    with open(fname, "w") as f:
        for ref_name, ref_val in refs.items():
            st = SuffixTree(ref_val)
            sa, lcp = traverse(st)
            f.write(ref_name)
            f.write("\n")
            f.write(str(sa))
            f.write("\n")
            f.write(str(lcp))
            f.write("\n\n")


if __name__ == "__main__":
    # read in the fasta file
    refs = parse_fa(sys.argv[1])
    # generate the file containing sa and lcp
    write_to_file(refs, sys.argv[1]+".lcp")

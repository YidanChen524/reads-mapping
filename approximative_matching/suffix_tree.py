"""
A Suffix tree built from string, suffix array and lcp array
"""
from helpers import compress_cigar


class SuffixTree:
    class Node:
        """a class for constructing tree nodes"""
        def __init__(self, start, end, parent=None, leaf=None):
            self.start = start
            self.end = end
            self.next = {}
            self.parent = parent
            self.leaf = leaf

    def __init__(self, x, sa, lcp):
        """initialize suffix tree with x, suffix array and lcp array"""
        self.x = x + "$"
        self.len = len(self.x)
        self.root = self.Node(0, 0)
        self.sa = sa
        self.lcp = lcp
        for i in range(self.len):
            self.add_suffix(i)

    def __str__(self, level=0, node=None):
        """print the suffix tree"""
        if not node:
            ret = f'string: {self.x} \nsuffix tree: \n\"'
            node = self.root
        else:
            ret = " " + "      " * (level - 1) + "|__: \""
        ret += self.x[node.start:node.end] + "\""
        if node.leaf is not None:
            ret += f" {node.leaf}"
        ret += "\n"
        for _, child in node.next.items():
            ret += self.__str__(level + 1, child)
        return ret

    def add_suffix(self, i):
        """add the ith suffix to the tree"""
        if self.lcp[i] == 0:
            new_node = self.Node(self.sa[i], self.len, self.root, self.sa[i])
            self.root.next[self.x[self.sa[i]]] = new_node
        else:
            steps = 0
            cur = self.root
            nxt = cur.next[self.x[self.sa[i - 1] + steps]]
            while nxt.end - nxt.start + steps < self.lcp[i]:
                steps += nxt.end - nxt.start
                cur = nxt
                nxt = cur.next[self.x[self.sa[i - 1] + steps]]
            if self.lcp[i] - steps == nxt.end - nxt.start:
                nxt.next[self.x[self.sa[i] + self.lcp[i]]] = self.Node(self.sa[i] + self.lcp[i], self.len, nxt, self.sa[i])
            else:
                new_node = self.Node(nxt.start, nxt.start + self.lcp[i] - steps, cur)
                new_node.next[self.x[self.sa[i] + self.lcp[i]]] = self.Node(self.sa[i] + self.lcp[i], self.len,
                                                                            new_node, self.sa[i])
                nxt.start = nxt.start + self.lcp[i] - steps
                new_node.next[self.x[new_node.end]] = nxt
                nxt.parent = new_node
                cur.next[self.x[new_node.start]] = new_node

    @staticmethod
    def get_leaves(node):
        """return all the leaves under current node"""
        def _get_leaves(current_node):
            # find all leaves under the node recursively and append it to leaves
            nonlocal leaves
            if not current_node.next:
                leaves.append(current_node.leaf)
            else:
                for child in current_node.next.values():
                    _get_leaves(child)
        # find all leaves under the node
        leaves = []
        _get_leaves(node)
        return leaves

    def find_approx(self, p, edits):
        """find match positions for p with no more than certain edit distance"""
        def _find_approx_recursive(current, i, j, cigar, d):
            if j == len(p) and d >= 0:
                if cigar.startswith("D") or cigar.endswith("D"):
                    return
                leaves = self.get_leaves(current)
                positions.extend(leaves)
                cigars.extend([compress_cigar(cigar)] * len(leaves))
                return
            if d < 0:
                return
            if i == current.end:
                for child in current.next.values():
                    _find_approx_recursive(child, child.start, j, cigar, d)
                return
            if self.x[i] == p[j]:
                _find_approx_recursive(current, i+1, j+1, "".join([cigar, "M"]), d)
                _find_approx_recursive(current, i+1, j, "".join([cigar, "D"]), d-1)
                _find_approx_recursive(current, i, j+1, "".join([cigar, "I"]), d-1)
            else:
                _find_approx_recursive(current, i+1, j+1, "".join([cigar, "M"]), d-1)
                _find_approx_recursive(current, i+1, j, "".join([cigar, "D"]), d-1)
                _find_approx_recursive(current, i, j+1, "".join([cigar, "I"]), d-1)
        positions = []
        cigars = []
        _find_approx_recursive(self.root, 0, 0, "", edits)
        return positions, cigars


if __name__ == "__main__":
    x = "agtt"
    sa, lcp = [4, 0, 1, 3, 2], [0, 0, 0, 0, 1]
    st = SuffixTree(x, sa, lcp)
    print(st)
    print(st.find_approx("aggt", 1))

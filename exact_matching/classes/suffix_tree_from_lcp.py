class SuffixTreeFromLCP:
    class Node:
        def __init__(self, start, end, leaf=None):
            self.start = start
            self.end = end
            self.next = {}
            self.leaf = leaf

    def __init__(self, x, sa, lcp):
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
        if node.leaf:
            ret += f" {node.leaf}"
        ret += "\n"
        for _, child in node.next.items():
            ret += self.__str__(level + 1, child)
        return ret

    def add_suffix(self, i):
        if self.lcp[i] == 0:
            new_node = self.Node(self.sa[i], self.len, self.sa[i])
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
                nxt.next[self.x[self.sa[i] + self.lcp[i]]] = self.Node(self.sa[i] + self.lcp[i], self.len, self.sa[i])
            else:
                new_node = self.Node(nxt.start, nxt.start + self.lcp[i] - steps)
                new_node.next[self.x[self.sa[i] + self.lcp[i]]] = self.Node(self.sa[i] + self.lcp[i], self.len,
                                                                            self.sa[i])
                nxt.start = nxt.start + self.lcp[i] - steps
                new_node.next[self.x[new_node.end]] = nxt
                cur.next[self.x[new_node.start]] = new_node

    def get_leaves(self, node, leaves=[]):
        """find all leaves under the node"""
        leaves = []
        self.get_leaves_recursive(node, leaves)
        return leaves

    def get_leaves_recursive(self, node, leaves):
        if not node.next:
            leaves.append(node.leaf)
        else:
            for child in node.next.values():
                self.get_leaves_recursive(child, leaves)

    def find_recursive(self, p, p_ind, current):
        """
        if p finds a match in the current node, return the position
        if there is a mismatch, return -1
        else continue the search in the next node
        """
        m, n = len(p) - p_ind, current.end - current.start
        for i in range(min(m, n)):
            if p[p_ind+i] != self.x[current.start+i]:
                return -1
        else:
            if m <= n:
                return self.get_leaves(current)
            else:
                if p[p_ind+n] in current.next:
                    return self.find_recursive(p, p_ind+n, current.next[p[p_ind+n]])
                else:
                    return -1

    def find(self, p):
        return self.find_recursive(p, 0, self.root)


if __name__ == "__main__":
    x = "helllo"
    sa = [6, 1, 0, 2, 3, 4, 5]
    lcp = [0, 0, 0, 0, 2, 1, 0]
    st = SuffixTreeFromLCP(x, sa, lcp)
    print(st)
    print(st.find("l"))

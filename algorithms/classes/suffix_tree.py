class SuffixTree:
    class Node:
        def __init__(self, start, end, leaf=None):
            self.start = start
            self.end = end
            self.next = {}
            self.leaves = []
            if leaf is not None:
                self.leaves.append(leaf)

    def __init__(self, x):
        self.x = x + "$"
        self.len = len(self.x)
        self.root = self.Node(0, self.len, 0)
        # construct the suffix tree by adding each suffix one by one starts from position 1
        for i in range(1, self.len):
            self.root = self.add_suffix(i, self.root, i)

    def __str__(self, level=0, node=None):
        """print the suffix tree"""
        if not node:
            ret = f'string: {self.x} \nsuffix tree: \n\"'
            node = self.root
        else:
            ret = " " + "      " * (level-1) + "|__: \""
        ret += self.x[node.start:node.end] + "\""
        ret += f" {node.leaves}"
        ret += "\n"
        for _, child in node.next.items():
            ret += self.__str__(level+1, child)
        return ret

    def add_suffix(self, i, current, leaf):
        """
        match suffix start from index i to the label stored in current node
        if there is a mismatch or reaching the end, create a new node
        """
        m = min(self.len - i, current.end - current.start)
        for j in range(m):
            if self.x[i+j] != self.x[current.start+j]:
                new_node = self.Node(current.start, current.start+j)
                current.start = current.start + j
                new_node.next[self.x[current.start]] = current
                new_node.next[self.x[i+j]] = self.Node(i+j, self.len, leaf)
                new_node.leaves += [*current.leaves, leaf]
                return new_node
        else:
            if self.x[i+m] in current.next:
                current.next[self.x[i+m]] = self.add_suffix(i + m, current.next[self.x[i + m]], leaf)
                current.leaves.append(leaf)
                return current
            else:
                current.next[self.x[i+m]] = self.Node(i+m, self.len, leaf)
                current.leaves.append(leaf)
                return current

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
                return current.leaves
            else:
                if p[p_ind+n] in current.next:
                    return self.find_recursive(p, p_ind+n, current.next[p[p_ind+n]])
                else:
                    return -1

    def find(self, p):
        return self.find_recursive(p, 0, self.root)


if __name__ == "__main__":
    st = SuffixTree("hello")
    print(st)

    # print(st.find("ssippi"))

class SuffixTree:
    class Node:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.next = {}

    def __init__(self, x):
        self.x = x + "$"
        self.len = len(self.x)
        self.root = self.Node(0, 0)
        # construct the suffix tree by adding each suffix one by one starts from position 1
        for i in range(1, self.len):
            self.root = self.match(i, self.root)

    def __str__(self, level=0, node=None):
        """print the suffix tree"""
        if not node:
            ret = f'string: {self.x} \nsuffix tree: \n\"'
            node = self.root
        else:
            ret = " " + "      " * (level-1) + "|__: \""
        ret += self.x[node.start:node.end] + "\"\n"
        for _, child in node.next.items():
            ret += self.__str__(level+1, child)
        return ret

    def match(self, i, current):
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
                new_node.next[self.x[i+j]] = self.Node(i+j, self.len)
                return new_node
        else:
            if self.x[i+m] in current.next:
                current.next[self.x[i+m]] = self.match(i+m, current.next[self.x[i+m]])
                return current
            else:
                current.next[self.x[i+m]] = self.Node(i+m, self.len)
                return current

    def find(self, p, current):
        j = 0
        if len(p) == 0 or current is None:
            return [-1]
        for i in range(current.end - current.start):
            if i == len(p):
                return [current.start + i - len(p) + 1]
            if self.x[current.start + i] != p[i]:
                return [-1]
        else:
            p = p[current.end:]
            if len(p) == 0:
                pos = []
                for node in current.next.values():
                    pos.append(node.start - len(p))
                return pos
            if p[0] not in current.next:
                return [-1]
            current = current.next[p[0]]
            return self.find(p, current)


if __name__ == "__main__":
    st = SuffixTree("hello")
    print(st)

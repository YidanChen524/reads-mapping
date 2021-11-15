import time
import matplotlib.pyplot as plt
from algorithms.classes.suffix_tree import SuffixTree
from algorithms.classes.suffix_tree_from_lcp import SuffixTreeFromLCP
from importlib import import_module
from algorithms.gen_lcp import traverse

# worst case running time for construct suffix tree from lcp
n = []
running_time = []
for i in range(1, 100):
    x = 'A' * i
    st1 = SuffixTree(x)
    sa, lcp = traverse(st1)

    start = time.time()
    st2 = SuffixTreeFromLCP(x, sa, lcp)
    end = time.time()

    n.append(i)
    running_time.append(end - start)

average_slope = 0
for i in range(1, len(running_time)):
    average_slope += running_time[i]/running_time[i-1]
average_slope /= len(running_time) - 1

plt.figure(1)
plt.plot(n, running_time)
plt.xlabel("n: the length of x")
plt.ylabel("worst-case running time")
plt.title("constructing suffix tree from sa and lcp, average slope: " + str(average_slope))
plt.savefig("running_time_building_st_from_lcp")


# worst case running time for searching
m = []
running_time = []
for i in range(1, 100):
    x = 'A' * 5 * i
    p = 'A' * i
    st1 = SuffixTree(x)
    sa, lcp = traverse(st1)
    st2 = SuffixTreeFromLCP(x, sa, lcp)

    start = time.time()
    st2.find(p)
    end = time.time()

    m.append(i)
    running_time.append(end - start)

average_slope = 0
for i in range(1, len(running_time)):
    average_slope += running_time[i]/running_time[i-1]
average_slope /= len(running_time) - 1

plt.figure(2)
plt.plot(m, running_time)
plt.xlabel("m: the length of p")
plt.ylabel("worst-case running time")
plt.title("searching suffix tree, average slope: " + str(average_slope))
plt.savefig("running_time_search_st2")

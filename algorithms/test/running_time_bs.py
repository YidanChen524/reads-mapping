import time
import matplotlib.pyplot as plt
from algorithms.helpers import suffix_array
from algorithms.search_bs import search_bs
import math

# search-bs with worse case scenario
mlogn = []
running_time = []
for m in range(1, 100):
    n = m * 10
    x = 'A' * n
    p = 'A' * m
    sa = suffix_array(x)
    start = time.time()
    search_bs(x, p, sa)
    end = time.time()
    mlogn.append(m*math.log(n, 2))
    running_time.append(end - start)

plt.plot(mlogn, running_time)
plt.xlabel("mlogn")
plt.ylabel("running time")
plt.title("search_bs algorithm (worst case scenario)")
plt.savefig("running_time_search_bs")


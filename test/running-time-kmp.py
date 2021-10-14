import time
import matplotlib.pyplot as plt


# helper functions that construct border arrays
def border_array(s):
    ba = [0] * len(s)
    for i in range(1, len(s)):
        b = ba[i - 1]
        while b > 0 and s[b] != s[i]:
            b = ba[b - 1]
        ba[i] = b + 1 if s[b] == s[i] else 0
    return ba


# running time experiment
mn = []
running_time = []
for m in range(1, 100):
    n = m * 10
    x = 'A' * n
    p = 'A' * m

    start = time.time()

    ba = border_array(p)
    i = j = 0
    while j < n:
        while i < m and j < n and x[j] == p[i]:
            j += 1
            i += 1
        if i == m:
            pass
        if i == 0:
            j += 1
        else:
            i = ba[i-1]

    end = time.time()

    mn.append(m + n)
    running_time.append(end - start)

plt.plot(mn, running_time)
plt.xlabel("m+n")
plt.ylabel("running time")
plt.title("kmp algorithm (worst case scenario)")
plt.savefig("running_time_kmp")


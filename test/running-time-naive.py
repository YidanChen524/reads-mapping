import time
import matplotlib.pyplot as plt

# naive algorithm with worse case scenario
mn = []
running_time = []
for m in range(1, 100):
    n = m * 10
    x = 'A' * n
    p = 'A' * m
    start = time.time()
    for j in range(n-m+1):
        for i in range(m):
            if p[i] != x[j+i]:
                break
        else:
            pass
    end = time.time()
    mn.append(m*n)
    running_time.append(end - start)

plt.plot(mn, running_time)
plt.xlabel("m*n")
plt.ylabel("running time")
plt.title("naive algorithm (worst case scenario)")
plt.savefig("running_time_naive")


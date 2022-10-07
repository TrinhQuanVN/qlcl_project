from cProfile import label
import matplotlib.pyplot as plt
import numpy as np

rng = np.arange(50)
rnd = np.random.randint(1,10,size=(3,rng.size))
yrs = rng + 1950
print(rnd)
fig, ax = plt.subplots(figsize=(10, 3))
ax.stackplot(yrs,rnd + rnd, labels=['Eas','Eur','Oce'])
ax.set_title('Combined')
ax.legend(loc = 'upper left')
ax.set_ylabel('Total')
ax.set_xlim(xmin=yrs[0],xmax=yrs[-1])
fig.tight_layout()


plt.show()
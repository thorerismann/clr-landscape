import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns

datadir = "/home/tge/dev/rust-model/clr-landscape/data" 
figdir = "/home/tge/dev/rust-model/clr-landscape/figures"

fig1 = np.genfromtxt(F'{datadir}/map-0.csv', delimiter=',')
fig2 = np.genfromtxt(F'{datadir}/map-120.csv', delimiter=',')
fig3 = np.genfromtxt(F'{datadir}/map-240.csv', delimiter=',')
fig4 = np.genfromtxt(F'{datadir}/map-360.csv', delimiter=',')
#fig9 = np.genfromtxt('/home/tge/dev/clr-landscape/data/365.csv', delimiter=',')

figs = [fig1,fig2,fig3,fig4]

# Make classified colour map
cmapClas = mpl.colors.ListedColormap(['#8dd3c7', '#ffffb3', '#bebada'])
bounds=[-1,0.9,1.9,2.9]
norm = mpl.colors.BoundaryNorm(bounds, cmapClas.N)

fig, axs = plt.subplots(4, 1)
axs[0].imshow(figs[0], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
axs[0].set_yticklabels([])
axs[0].set_xticklabels([])
axs[1].imshow(figs[1], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
axs[1].set_yticklabels([])
axs[1].set_xticklabels([])
axs[2].imshow(figs[2], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
axs[2].set_yticklabels([])
axs[2].set_xticklabels([])
axs[3].imshow(figs[3], interpolation='none', aspect=1, cmap=cmapClas, norm=norm)
axs[3].set_yticklabels([])
axs[3].set_xticklabels([])
plt.savefig(F'{figdir}/infection_progression.png')
plt.show()

a = pd.read_csv(F"{datadir}/results.csv")
a.set_index("day",inplace=True)

a = a[['infection_score', 'infected_cells', 'infected_plants']]

sns.lineplot(data = a, x = a.index,y = "infected_cells")
plt.savefig(F'{figdir}/infected-cells.png')
plt.show()
sns.lineplot(data = a, x= a.index,y = "infection_score")
plt.savefig(F'{figdir}/infection-score.png')
plt.show()
sns.lineplot(data = a, x= a.index,y = "infected_plants")
plt.savefig(F'{figdir}/infected-plants.png')
plt.show()
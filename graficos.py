import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv("data/slr.csv", sep=";", encoding="utf-8", quoting=2, keep_default_na=False, dtype={"N": np.int32, 'Code': np.int32, 'Year': np.int32})

years = df['Year'].value_counts().sort_index()
#
# plt.plot(pd.to_datetime(df['Year']), df['N'], color='skyblue')


# df=pd.DataFrame({'x': range(1,11), 'y': np.random.randn(10) })
#
# # df_plot = pd.DataFrame({'x': df['Year'], 'y': df['N']})
# plt.plot('x', 'y', data=df, color='skyblue')

x = years.index.values.tolist()
xi = [i for i in range(0, len(x))]
y = years.values.tolist()


plt.plot(years,marker='o', linestyle='--', color='b')
# plt.title("Year of publication for the selected techniques")
plt.xlabel("Year of publication")
plt.ylabel("Number of publications")
# plt.xticks(xi, x)
plt.legend()
plt.savefig('data/publication.png', bbox_inches='tight')
plt.show()

float(sum(y)) / max(len(y), 1)

import matplotlib.pyplot as plt
x = [0.00001,0.001,0.01,0.1,0.5,1,5]
# create an index for each tick position
xi = [i for i in range(0, len(x))]
y = [0.945,0.885,0.893,0.9,0.996,1.25,1.19]
plt.ylim(0.8,1.4)
# plot the index for the x-values
plt.plot(xi, y, marker='o', linestyle='--', color='r', label='Square')
plt.xlabel('x')
plt.ylabel('y')
plt.xticks(xi, x)
plt.title('compare')
plt.legend()
plt.show()
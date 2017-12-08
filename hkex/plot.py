import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print("usage: plot.py input.json output.png")
json_handle = sys.argv[1]
png_handle = sys.argv[2]
stock_data = pd.read_json(json_handle)
y = stock_data['stock_percent'].T.values
print(y)
print(len(y))
x = range(0, len(y))
plt.plot(x, y, '')
plt.savefig(png_handle)

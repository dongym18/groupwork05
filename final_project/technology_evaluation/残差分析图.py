import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r'E:\pythonTest\predict.csv')
X = df['tree_y']#X-axis在文件中指定列的名称
Y = df['true_y - tree_y']#Y-axis在文件中指定列的名称
plt.scatter(X, Y)
plt.xlabel('Predicted Y')
plt.ylabel('Residual')
plt.show()
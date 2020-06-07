import numpy as np
from matplotlib import pyplot as plt
source = "Data/"
files = ["320.txt", "325.txt", "330.txt", "335.txt", "340.txt", "345.txt", "350.txt", "355.txt"]
# files = [ str(i) + ".txt" for i in range(320, 360, 5)]    # или для краткости так

display = True      # выводить  ли графики

absShift = np.loadtxt('absShift.txt')

data = []
for f in files:
    data.append(np.loadtxt(source+f))

res = [0]*(int(absShift[0][-1]) + len(data[-1]))
count = [0]*(int(absShift[0][-1]) + len(data[-1]) + 1)  # считаем, сколько кусочков перекрываются в этой точке
for i in range(len(data)):
    for j in range(len(data[i])):
        res[j+int(absShift[0][i])] += data[i][j]+absShift[1][i]
    count[int(absShift[0][i])] += 1
    count[int(absShift[0][i])+len(data[i])] -= 1
c = 0
for i in range(len(count)):
    c += count[i]
    count[i] = c
for i in range(len(res)):
    res[i] /= count[i]

a = min(res)
res = [x-a for x in res]        # опускаем значения минимумом в ноль
if display:
    plt.plot(res)
    plt.show()

np.savetxt('connected.txt', res)

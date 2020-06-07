import numpy as np
from matplotlib import pyplot as plt
source = "Data/"
files = ["320.txt", "325.txt", "330.txt", "335.txt", "340.txt", "345.txt", "350.txt", "355.txt"]

# soundV = 1800   # скорость звука в материале
# deltaT = 5e-6   # промежутки времени между сигналами в секундах
tsh = 100       # теоретический сдвиг между сигналами
err = 50        # максимальное допустимое отклонение от теоретического сдвига

data = []
for f in files:
    data.append(np.loadtxt(source+f))

a = 4
shifting = [48, 100]
core = np.loadtxt(source+files[a])
near = np.loadtxt(source+files[a+1])


plt.plot(core)
for i in range(len(shifting)):
    plt.plot(np.arange(shifting[i], shifting[i]+len(near)), near)
plt.show()


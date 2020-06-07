import numpy as np
from matplotlib import pyplot as plt
source = "Data/"
files = ["320.txt", "325.txt", "330.txt", "335.txt", "340.txt", "345.txt", "350.txt", "355.txt"]
# files = [ str(i) + ".txt" for i in range(320, 360, 5)]    # или для краткости так

display = True      # выводить  ли графики

'''
soundV = 1800   # скорость звука в материале
deltaT = 5e-6   # промежутки времени между сигналами в секундах
X = 0.000083    # размер пикселя в метрах
tsh = int(soundV*deltaT/X)       # теоретический сдвиг между сигналами
err = tsh*0.3        # максимальное допустимое отклонение от теоретического сдвига
'''

tsh = 108       # теоретический сдвиг между сигналами
err = 60        # максимальное допустимое отклонение от теоретического сдвига


data = []       # исходные массивы
for f in files:
    data.append(np.loadtxt(source+f))
prefs = []
for m in data:
    sum = 0
    prefs.append([0])
    for x in m:
        sum += x
        prefs[-1].append(sum)

relShift = [[], []]
# сдвиг каждого следующего куска относительно предыдущего. [[ по горизонтали вправо ], [по вертикали вверх]]

for a in range(len(data)-1):
    core = data[a]
    corepref = prefs[a]
    near = data[a+1]
    nearpref = prefs[a+1]
    result = [[], [], []]       # sh, сумма квадратов отклонений, отклонение по вертикали

    for sh in range(tsh - err, tsh + err):       # sh - сдвиг начала near относительно саамй левой позиции
        # выясняем ращницу по вертикали
        diff = (corepref[len(core)] - corepref[sh] - nearpref[len(core) - sh])/(len(core) - sh)
        # разница между средним на промежутке для core и near (сдвиг по вертикали)
        distSq = 0  # переменная с суммой квадратов
        for i in range(len(core) - sh):
            distSq += (near[i] - diff - core[i + sh]) ** 2
        result[0].append(sh)
        result[1].append(distSq)
        result[2].append(diff)
    # if a == 4:
    #     plt.plot(result[0], result[1])
    #     plt.show()


    minV = result[1][0]
    minI = 0
    for i in range(1, len(result[0])):
        if result[1][i] < result[1][minI]:
            minI = i
    relShift[0].append(result[0][minI])
    relShift[1].append(result[2][minI])
    # print(result[0][minI])

absShift = [[0], [0]]  # абсолютные значения сдвига относительно начальной кривой
for i in range(len(relShift[0])):
    absShift[0].append(absShift[0][-1] + relShift[0][i])
    absShift[1].append(absShift[1][-1] + relShift[1][i])

if display:     # графики в нахлест
    for i in range(len(absShift[0])):
        plt.plot(np.arange(absShift[0][i], len(data[i]) + absShift[0][i]), data[i] + absShift[1][i])

    plt.show()

np.savetxt('absShift.txt', absShift)
np.savetxt('relShift.txt', relShift)


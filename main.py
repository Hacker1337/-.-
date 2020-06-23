import numpy as np
from matplotlib import pyplot as plt
import os


outputPlace = "output/"     # папка для склеенных массивов
if not os.path.exists(outputPlace):
    os.makedirs(outputPlace)
dirs = ["Data", "Data2", "Data3"]
# массив с массивами файлов, которые нужно объединить в один график

# files = ["320.txt", "325.txt", "330.txt", "335.txt", "340.txt", "345.txt", "350.txt", "355.txt"]
# # files = [ str(i) + ".txt" for i in range(320, 360, 5)]    # или для краткости так
display = True      # выводить  ли графики

soundV = 3000   # скорость звука в материале
X = 0.000083    # размер пикселя в метрах
tsh = []        # int(soundV*deltaT/X)       # теоретический сдвиг между сигналами
relErr = 0.8        # максимальное допустимое отклонение от теоретического сдвига


# for files in groupsOfFiles:
for dir in dirs:
    data = []       # исходные массивы
    files = os.listdir(dir)
    detectionTimes = []
    for f in files:
        if f[-3:] == 'txt':
            data.append(np.loadtxt(os.path.join(dir, f)))
            detectionTimes.append(int(f[:f.find('.')]))
    for i in range(len(detectionTimes)-1):
        tsh.append(int(soundV*(detectionTimes[i+1]-detectionTimes[i])*1e-6/X))
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
        for sh in range(int(tsh[a]*(1-relErr)), int(tsh[a]*(1+relErr))):       # sh - сдвиг начала near относительно саамй левой позиции
            # выясняем разницу по вертикали
            diff = (corepref[len(core)] - corepref[sh] - nearpref[len(core) - sh])/(len(core) - sh)
            # разница между средним на промежутке для core и near (сдвиг по вертикали)
            distSq = 0  # переменная с суммой квадратов
            for i in range(len(core) - sh):
                distSq += (near[i] + diff - core[i + sh]) ** 2
            result[0].append(sh)
            result[1].append(distSq/(len(core) - sh))
            result[2].append(diff)

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
    np.savetxt(os.path.join(outputPlace, f"relShift{dir}.txt"), relShift)
    np.savetxt(os.path.join(outputPlace, f"absShift{dir}.txt"), absShift)

    if display:     # графики в нахлест
        for i in range(len(absShift[0])):
            plt.plot(np.arange(absShift[0][i], len(data[i]) + absShift[0][i]), data[i] + absShift[1][i])

        plt.show()

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

    np.savetxt(outputPlace+f'connected{dir}.txt', res)

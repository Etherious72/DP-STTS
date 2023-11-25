import re
import datetime
import pandas as pd
from parameters import Parameter
from removeTime import removeTime


def trans(dataset, epsilon, cellH, numtimeInterval, h, times):
    # 获取数据条件
    left = para.left
    right = para.right
    bottom = para.bottom
    top = para.top

    width = para.cellW
    height = para.cellH
    cellheight = (top - bottom) / height
    cellwidth = (right - left) / width

    with open('./data/parameters/time.txt') as input:
        content = input.readlines()
        array = content[0].split(" ")
        fixedtime = array[0]
        starttime = array[1][:8]
        array = content[1].split(" ")
        endtime = array[1]

    output = open('./data/output/' + dataset + '_' + cellH + '_' + numtimeInterval + '_maxLevel' + h + '_totalBudget'
                  + str(epsilon) + '_' + times + '.txt', 'w')
    #    print("start transformation")
    with open('./data/output/writeTra-our.txt') as input:
        content = input.readlines()
    i = 0
    while i < len(content):
        if i % 2 == 0:
            fixedcontent = content[i]
            output.write(fixedcontent)
            output.write(">0:")
        else:
            array = re.split('[>:,;]', content[i])

            j = 4
            while j < len(array):
                if array[j] == '-2' or array[j] == '\n':
                    break
                else:
                    rowindex = int(int(array[j]) / width)
                    columnindex = int(int(array[j]) % width)
                    lat = float(bottom + rowindex * cellheight + cellheight / 2)
                    lon = float(left + columnindex * cellwidth + cellwidth / 2)
                    output.write(str(lon) + ",")
                    output.write(str(lat) + ",")
                    time = float(para.startTime.second / 60) + para.timestep * float(array[j + 1]) + para.timestep / 2
                    time = para.startTime + datetime.timedelta(seconds=time * 60)

                    output.write(str(time) + ";")

                    j = j + 2
            output.write('\n')
        i += 1
    output.close()


para = Parameter()


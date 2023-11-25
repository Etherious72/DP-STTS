import math
import re
from datetime import datetime, timedelta
import pandas as pd
from parameters import Parameter


def CellIndex(longitude, latitude):
    """
    get cell index
    :param longitude:
    :param latitude:
    :return:
    """
    incre = 0.0005
    longitude = float(longitude)
    latitude = float(latitude)
    height = float((para.top - para.bottom) / para.cellH)
    width = float((para.right - para.left) / para.cellW)
    rowIndex = int(math.floor((latitude - para.bottom) / height))
    columnIndex = int(math.floor((longitude - para.left) / width))
    rowIndex1 = int(math.floor((latitude - para.bottom - incre) / height))
    columnIndex1 = int(math.floor((longitude - para.left - incre) / width))
    rowIndex2 = int(math.floor((latitude - para.bottom + incre) / height))
    columnIndex2 = int(math.floor((longitude - para.left + incre) / width))
    if math.fabs(rowIndex * height + para.bottom - latitude) < pow(10, -6):
        rowIndex -= 1
    if math.fabs(columnIndex * width + para.left - longitude) < pow(10, -6):
        columnIndex -= 1
    if rowIndex1 != rowIndex2:
        if rowIndex1 < 0:
            rowIndex = rowIndex2
            latitude += incre
        else:
            rowIndex = rowIndex1
            latitude -= incre
    if columnIndex1 != columnIndex2:
        if columnIndex1 < 0:
            columnIndex = columnIndex2
            longitude += incre
        else:
            columnIndex = columnIndex1
            longitude -= incre

    if rowIndex < 0:
        rowIndex = 0
    if columnIndex < 0:
        columnIndex = 0
    if rowIndex >= para.cellH:
        rowIndex = para.cellH - 1
    if columnIndex >= para.cellW:
        columnIndex = para.cellW - 1
    cellIndex = rowIndex * para.cellW + columnIndex
    if cellIndex >= para.cellH * para.cellW:
        print('something is wrong \n')
    return cellIndex


def TimeIndex(time):
    """
    :param time:
    :return: timeIndex
    """
    start = datetime.combine(time.date(), para.startTime.time())
    delta = (time - start).seconds / 60
    timeIndex = int(delta / para.timestep)
    if (time - (timedelta(minutes=(timeIndex * para.timestep)) + start)).seconds < pow(10, -5):
        timeIndex -= 1
    if timeIndex < 0:
        timeIndex = 0
    return timeIndex


def getTimeRange():
    t_boundary = open('./data/parameters/time.txt', "r")
    lines = t_boundary.readlines()
    data = []
    for Data in lines:
        Data = Data.replace('\n', '')
        data.append(Data)
    time_boundary = pd.to_datetime(data)
    start_hour = str(time_boundary[0])
    end_hour = str(time_boundary[1])
    start = start_hour.split(' ')
    end = end_hour.split(' ')
    startTime = datetime.strptime(start[1], '%H:%M:%S')
    endTime = datetime.strptime(end[1], '%H:%M:%S')
    t_boundary.close()
    return startTime, endTime


def CutTrajectories():
    print("start cutting")
    startTime = getTimeRange()[0]
    endTime = getTimeRange()[1]
    add_seconds = timedelta(seconds=15)
    print(startTime)
    print(endTime)
    outputfile = './data/output/TestData.txt'
    inputfile = './data/raw_data/Original.txt'

    boundary = './data/parameters/boundary.txt'

    with open(boundary) as input:
        content = input.readline()
        array = content.split(" ")
        left = float(array[0])
        right = float(array[1])
        bottom = float(array[2])
        top = float(array[3])

    output = open(outputfile, 'w')
    with open(inputfile) as input:
        content = input.readlines()
    i = 1
    id = 0
    while i < len(content):

        flag = 0
        arrayT = content[i][3:]
        array = re.split('[,;]', arrayT)
        j = 0

        if i % 10000 == 0:
           print(i)

        if len(array) < 4:
            i = i + 2
            continue

        numP = 0
        while j < len(array):
            if array[j] == '\n':
                break
            else:

                lon = float(array[j])
                j = j + 1
                lat = float(array[j])
                j = j + 1
                temp_u = datetime.strptime(array[j], "%Y-%m-%d %H:%M:%S")
                j = j + 1
                if left <= lon <= right and bottom <= lat <= top and startTime <= temp_u <= endTime:
                    if flag == 0:
                        flag = 1
                        output.write("#")
                        output.write(str(id))
                        output.write(":\n")
                        output.write('>0:')
                        id = id + 1
                    if numP == 0:
                        cellA = CellIndex(lon, lat)
                        cellPre = cellA

                        timePre = temp_u
                    else:
                        cellA = CellIndex(lon, lat)

                    if cellA != cellPre:
                        cellPre = cellA
                        timePre = temp_u
                    t = (temp_u - timePre).seconds/60
                    if not (cellA == cellPre and (temp_u - timePre).seconds/60 > para.numstep * para.timestep):
                        output.write(str(lon) + ",")
                        output.write(str(lat) + ",")
                        output.write(str(temp_u) + ";")
                        numP += 1
                    else:
                        break

                else:
                    if flag == 1:
                        break
        if flag == 1:
            output.write("\n")
        i = i + 2

    output.close()
    print('cutting is done')


para = Parameter()
# CutTrajectories()












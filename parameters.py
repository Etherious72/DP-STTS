import math
import os
import sys
from datetime import datetime
import pandas as pd

sys.setrecursionlimit(6000)  # 修改默认的递归深度


def boundary():
    f_boundary = open('./data/parameters/boundary.txt', "r")
    if f_boundary is None:
        print("Can not open boundary file\n")
        return
    lines = f_boundary.readlines()
    data = []
    for Data in lines:
        Data = Data.split(' ')
        data.append(Data)
    global left, right, bottom, top
    left = float(data[0][0])
    right = float(data[0][1])
    bottom = float(data[0][3])
    top = float(data[0][2])
    f_boundary.close()
    return left, right, bottom, top


def time():
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


def TimeStep():
    f_timeInterval = open('./data/parameters/timeStep.txt', "r")
    if f_timeInterval is None:
        print("Can not open timeInterval file\n")
        return
    lines = f_timeInterval.readlines()
    data = []
    for l in lines:
        data.append(l)
    global numTimeInterval
    numTimeInterval = int(data[0])
    f_timeInterval.close()
    return numTimeInterval


def cellSize():
    f_cellSize = open('./data/parameters/cellSize.txt', "r")
    if f_cellSize is None:
        print("Can not open cellSize file\n")
        return
    lines = f_cellSize.readlines()
    data = []
    for Data in lines:
        Data = Data.split(' ')
        data.append(Data)
    global cellH, cellW
    cellH = int(data[0][0])
    cellW = int(data[0][1])
    f_cellSize.close()
    return cellH, cellW


def neighborFile():
    n_boundary = open('data/parameters/neighborFile_' + str(cellSize()[0]) + '.txt', 'a+')
    p = 'data/parameters/neighborFile_' + str(cellSize()[0]) + '.txt'
    if not os.path.getsize(p):
        print('@@@@@@@@@@@@@@@@@@@@@@@@  Wait for file generation  @@@@@@@@@@@@@@@@@@@@@@@@')
    else:
        n_boundary.close()
        n_boundary = open('data/parameters/neighborFile_' + str(cellSize()[0]) + '.txt', 'r')
        if n_boundary is None:
            print("Can not open file\n")
            return
        # lines = n_boundary.read().splitlines()
        lines = n_boundary.readlines()
        neighbor = []

        for Data in lines:
            count = 0
            data = []
            Data = Data.split(' ')
            while count < 9:
                data.append(int(Data[count]))
                count += 1
            neighbor.append(data)
        return neighbor


class Parameter(object):
    def __init__(self):
        self.left = boundary()[0]
        self.right = boundary()[1]
        self.top = boundary()[2]
        self.bottom = boundary()[3]
        self.neighbor = neighborFile()
        self.startTime = time()[0]
        self.endTime = time()[1]
        self.cellH = cellSize()[0]
        self.cellW = cellSize()[1]
        self.timestep = TimeStep()
        self.numtimeInterval = math.ceil((self.endTime - self.startTime).seconds / 60 / self.timestep)
        self.cellCount = self.cellW * self.cellH
        self.numstep = 2
        self.maxTLen = 125
        self.maxLevel = 1
        self.tmaxLevel = 2  # 2 <= tmaxLevel <= maxLevel
        self.startSign = -1
        self.endSign = -2
        self.aSign = -3
        self.oSign = -6
        self.incre = -4
        self.noIncre = -5
        self.epsilon = 1.0
        self.epsilonPrefix = 0.5
        self.sensitivity = 1
        self.count = 0

    def show(self):
        print('-------------------- The parameters : -------------------')
        print('--------------------   Cell Attribute ---------------------')
        print('left : %f' % self.left)
        print('right : %f' % self.right)
        print('top : %f' % self.top)
        print('bottom : %f' % self.bottom)
        print('cellH : %d' % self.cellH)
        print('cellW : %d' % self.cellW)
        print('cellCount : %d' % self.cellCount)
        print('--------------------   Time Attribute ---------------------')
        print('startTime : %s' % self.startTime)
        print('endTime : %s' % self.endTime)
        print('numtimeInterval : %d' % self.numtimeInterval)
        print('timestep : %d' % self.timestep)
        # print('maxTLen : %s' % self.maxTLen)
        print('--------------------  Other Attribute ---------------------')
        print('maxTLen : %d' % self.maxTLen)
        print('maxLevel : %d' % self.maxLevel)
        print('startSign : %d' % self.startSign)
        print('endSign : %d' % self.endSign)
        print('aSign : %d' % self.aSign)
        print('epsilon : %s' % self.epsilon)


para = Parameter()
para.show()
